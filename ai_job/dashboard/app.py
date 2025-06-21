from wordcloud import WordCloud
import plotly.express as px
import plotly.io as pio
import streamlit as st
import pandas as pd
import os


st.set_page_config(layout="wide")

# Este CSS permite que as colunas das métricas "quebrem a linha" em telas menores
# (como quando a sidebar está aberta), evitando que o conteúdo seja cortado.
st.markdown("""
<style>
    /* Mira o contêiner das colunas do Streamlit */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap;
        gap: 1rem; /* Opcional: Adiciona um espaço vertical quando as métricas quebram a linha */
    }
</style>
""", unsafe_allow_html=True)

pio.templates.default = "plotly_dark"

# monta o caminho completo sempre relativo ao app.py
HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "ai_job_dataset.csv")

@st.cache_data
def load_data(path=DATA_PATH):
    return pd.read_csv(path, parse_dates=['posting_date', 'application_deadline'])

df = load_data()

# Sidebar filters
st.sidebar.header("Filtros")
job_title = st.sidebar.selectbox(
    "Título da Vaga", ["Todas"] + sorted(df['job_title'].unique().tolist())
)
countries = st.sidebar.multiselect(
    "Países", sorted(df['company_location'].unique()), default=[]
)
exp_levels = st.sidebar.multiselect(
    "Nível de Experiência", sorted(df['experience_level'].unique()), default=[]
)
salary_min, salary_max = st.sidebar.slider(
    "Faixa Salarial (USD)",
    int(df['salary_usd'].min()), int(df['salary_usd'].max()),
    (int(df['salary_usd'].quantile(0.05)), int(df['salary_usd'].quantile(0.95)))
)
remote_ratio = st.sidebar.multiselect(
    "Trabalho Remoto (%)", sorted(df['remote_ratio'].unique()), default=[]
)

# Apply filters
df_filtered = df.copy()
if job_title != "Todas":
    df_filtered = df_filtered[df_filtered['job_title'] == job_title]
if countries:
    df_filtered = df_filtered[df_filtered['company_location'].isin(countries)]
if exp_levels:
    df_filtered = df_filtered[df_filtered['experience_level'].isin(exp_levels)]
if remote_ratio:
    df_filtered = df_filtered[df_filtered['remote_ratio'].isin(remote_ratio)]
df_filtered = df_filtered.query("salary_usd >= @salary_min and salary_usd <= @salary_max")

# Metrics Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Vaga", job_title)
col2.metric("Vagas", df_filtered.shape[0])
col3.metric("Média Salarial (USD)", f"${df_filtered['salary_usd'].mean():,.2f}")
col4.metric("Países", len(df_filtered['company_location'].unique()))
col5.metric("Média de Benefícios", f"{df_filtered['benefits_score'].mean():.1f}")

st.divider() # Adiciona uma linha divisória para separar as métricas do conteúdo

# Tabs
tab1, tab2, tab3 = st.tabs(["Mapa", "Distribuições", "Empresas & Skills"])

with tab1:
    salary_by_country = (
        df_filtered.groupby('company_location')['salary_usd']
        .mean()
        .reset_index()
        .rename(columns={'company_location': 'country', 'salary_usd': 'avg_salary'})
    )

    # Criamos 3 colunas para usar a do meio como contêiner principal,
    # limitando a largura e centralizando o conteúdo.
    map_col1, map_col2, map_col3 = st.columns([0.1, 0.8, 0.1])
    with map_col2:
        st.subheader("Choropleth de Salário Médio por País")
        fig = px.choropleth(
            salary_by_country,
            locations='country',
            locationmode='country names',
            color='avg_salary',
            hover_name='country',
            color_continuous_scale=px.colors.sequential.Blues_r,
            labels={'avg_salary':'Salário Médio (USD)'},
            title=f'Média Salarial para {job_title}'
        )
        fig.update_coloraxes(colorbar_title_text="")
        fig.update_geos(
            showcountries=True, countrycolor="gray",
            showsubunits=True, subunitcolor="gray",
            showframe=False, showcoastlines=True, coastlinecolor="gray"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Aplicamos a mesma técnica de colunas para este gráfico.
    top_countries_col1, top_countries_col2, top_countries_col3 = st.columns([0.2, 0.6, 0.2])
    with top_countries_col2:
        st.subheader("Top Países por Salário Médio")
        top10 = salary_by_country.nlargest(10, 'avg_salary')
        fig_top10 = px.bar(
            top10, x='country', y='avg_salary', orientation='v',
            labels={'avg_salary':'Salário Médio (USD)', 'country':'País'}
        )
        fig_top10.update_layout(
            xaxis_title=None, yaxis_title=None,
            margin=dict(l=60, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_top10, use_container_width=True)

with tab2:
    # Esta aba já tem um bom layout com 2 colunas, então não precisa de grandes mudanças.
    st.subheader("Distribuições")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Salário por Nível de Experiência**")
        fig1 = px.box(
            df_filtered, x='experience_level', y='salary_usd', points='outliers',
            hover_data=['company_location','salary_usd'],
            labels={'salary_usd':'Salário (USD)','experience_level':'Experiência'}
        )
        fig1.update_layout(xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.write("**Anos de Experiência**")
        fig2 = px.histogram(
            df_filtered, x='years_experience', nbins=20,
            labels={'years_experience':'Anos de Experiência'}
        )
        fig2.update_layout(xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    skills_counts = (
        df_filtered['required_skills']
        .str.split(',', expand=True)
        .stack()
        .str.strip()
        .value_counts()
    )

    skills_col1, skills_col2, skills_col3 = st.columns([0.2, 0.6, 0.2])
    with skills_col2:
        st.subheader("Top Skills Requeridas")
        top_skills = skills_counts.nlargest(10).reset_index()
        top_skills.columns = ['skill', 'count']
        fig_sk = px.bar(
            top_skills, x='count', y='skill', orientation='h',
            labels={'count':'Ocorrências','skill':'Skill'},
            title=f"Top 10 Skills para {job_title}"
        )
        fig_sk.update_layout(xaxis_title=None, yaxis_title=None, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_sk, use_container_width=True)

    st.divider()

    cloud_col1, cloud_col2, cloud_col3 = st.columns([0.2, 0.6, 0.2])
    with cloud_col2:
        st.subheader("Nuvem de Skills Requeridas")
        # Gerando nuvem apenas se houver skills para evitar erro
        if not skills_counts.empty:
            wc = WordCloud(
                width=800, height=400, background_color='black', colormap='plasma'
            )
            img = wc.generate_from_frequencies(skills_counts.to_dict())
            st.image(img.to_array(), use_container_width=True)
        else:
            st.warning("Não há dados de skills para a seleção atual.")
