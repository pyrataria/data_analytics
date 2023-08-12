# ESTUDO DESCRITIVO - SPOTIFY
Neste conjunto de dados existem 10000 registros sobre as canções mais populares que dominaram o cenário músical entre os anos de 1960 aos dias atuais. Seu conteúdo é baseado em dados da ARIA (Australian Recording Industry Association) e Billboard.
A representação musical no conjunto de dados é abrangente, portanto, dele, podem ser extraídas informações valiosas acerca da evolução musical.

**<u>Projeto</u>**  
A respeito do estudo, o mesmo tem como objetivo mostrar principalmente a distribuição de frequências a respeito de de determinadas variáveis. Além disso, será verificado se há correlação entre as variáveis, no que diz respeito as "qualidades" das músicas.


<u>Descrição das variáveis</u>:  
**Explicit**: indica se a música têm linguagem pesada como palavrões, citações ao uso e/ou nome de drogas, xingamentos e violência.  
**Popularity**: popularidade de uma faixa, com valores entre 0 e 100, sendo 100 o mais popular.  
**Danceability**: critério descreve quão dançante é a faixa. Quanto mais perto de 0.0, menos dançável a canção é, e quanto mais dançável, mais perto de 1.0.  
**Energy**: percentual de intensidade e atividade da música. Seus valores variam entre 0 e 1. Uma música com alto valor dessa variável provavelmente será rápida e até considerada “barulhenta”.  
**Key:** notas ou a escala da música que forma a base de uma música. Os 12 tons variam entre 0 e 11.  
**Loudness**: diz o quão alto ou silencioso é o volume médio de uma música. Músicas com valores de "loudness" mais baixos tendem a ser mais suaves e calmas, enquanto aquelas com valores mais altos podem ser mais energéticas e barulhentas.  
**Mode:** as músicas podem ser classificadas como maiores e menores. 1,0 representa o modo principal e 0 representa o secundário.  
**Speechiness**: detecta a presença de palavras faladas em uma faixa.  
**Acousticness**: descreve o quão acústica é uma música. Uma pontuação de 1,0 significa que é mais provável que a música seja acústica.  
**Instrumentalness**: representa a quantidade de vocais na música. Quanto mais próximo de 1,0, mais instrumental é a música.  
**Liveness**: descreve a probabilidade de a música ter sido gravada com uma audiência ao vivo.  
**Valence**: descreve a positividade musical transmitida por uma faixa.  
**Tempo**: representa a velocidade ou ritmo da música.  
**Time Signature**: convenção de notação para especificar quantas batidas há em cada compasso.

# PREPARAÇÃO, ORGANIZAÇÃO E ESTRUTURAÇÃO DOS DADOS

```python
import pandas as pd
```

```python
pd.set_option("display.max_columns", 35)
```

```python
df = pd.read_csv("/content/drive/MyDrive/programacao/datasets/spotify/top_10000_1960-now.csv")
df.head()
```

```python
df.shape
```

> (9999, 35)

O dataset possui um total de 9999 registros e 35 variáveis.

```python
df.dtypes
```

> Track URI                object  
> Track Name               object  
> Artist URI(s)            object  
> Artist Name(s)           object  
> Album URI                object  
> Album Name               object  
> Album Artist URI(s)      object  
> Album Artist Name(s)     object  
> Album Release Date       object  
> Album Image URL          object  
> Disc Number               int64  
> Track Number              int64  
> Track Duration (ms)       int64  
> Track Preview URL        object  
> Explicit                   bool  
> Popularity                int64  
> ISRC                     object  
> Added By                 object  
> Added At                 object  
> Artist Genres            object  
> Danceability            float64  
> Energy                  float64  
> Key                     float64  
> Loudness                float64  
> Mode                    float64  
> Speechiness             float64  
> Acousticness            float64  
> Instrumentalness        float64  
> Liveness                float64  
> Valence                 float64  
> Tempo                   float64  
> Time Signature          float64  
> Album Genres            float64  
> Label                    object  
> Copyrights               object  
> dtype: object  

O tipo dos dados está no padrão para correto, portanto, não será necessária nenhuma alteração.
## Extração e limpeza de dados
<u>Verificando valores nulos</u>

```python
df.isnull().sum()
```

> Track URI                  0  
> Track Name                 1  
> Artist URI(s)              2  
> Artist Name(s)             1  
> Album URI                  2  
> Album Name                 1  
> Album Artist URI(s)        2  
> Album Artist Name(s)       2  
> Album Release Date         2  
> Album Image URL            4  
> Disc Number                0  
> Track Number               0  
> Track Duration (ms)        0  
> Track Preview URL       2897  
> Explicit                   0  
> Popularity                 0  
> ISRC                       3  
> Added By                   0  
> Added At                   0  
> Artist Genres            550  
> Danceability               2  
> Energy                     2  
> Key                        2  
> Loudness                   2  
> Mode                       2  
> Speechiness                2  
> Acousticness               2  
> Instrumentalness           2  
> Liveness                   2  
> Valence                    2  
> Tempo                      2  
> Time Signature             2  
> Album Genres            9999  
> Label                      6  
> Copyrights                24  
> dtype: int64  

<u>Removendo variáveis e registros</u>  
A variável *Album Genres* possui apenas valores nulos, assim, se torna inútil aos estudos, portanto, deve ser excluída. As demais variáveis, também não serão necessárias à estatística descritiva.

```python
df.drop(columns=["Album Genres", "Track URI", "Artist URI(s)", "Album URI",
                 "Added By", "Album Artist URI(s)", "Album Image URL",
                 "Track Preview URL", "Copyrights", "Added At", "Disc Number",
                 "Track Number"], inplace=True)
```

```python
df.shape
```

> (9999, 23)

Com isso, as variáveis foram reduzidas para 23.  
Além das colunas, foi possível perceber que, alguns registros se encontram com valor(es) nulo(s). Sendo eles em menor porporção, será feita a remoção.

```python
i_drop = df[df.drop("Artist Genres", axis=1).isnull().any(axis=1)].index
```

```python
df.drop(i_drop, axis=0, inplace=True)
```

```python
df.shape
```

> (9993, 23)

Com isso, alguns registros foram removidos.

```python
df.isnull().sum()
```

> Track Name                0  
> Artist Name(s)            0  
> Album Name                0  
> Album Artist Name(s)      0  
> Album Release Date        0  
> Track Duration (ms)       0  
> Explicit                  0  
> Popularity                0  
> ISRC                      0  
> Artist Genres           547  
> Danceability              0  
> Energy                    0  
> Key                       0  
> Loudness                  0  
> Mode                      0  
> Speechiness               0  
> Acousticness              0  
> Instrumentalness          0  
> Liveness                  0  
> Valence                   0  
> Tempo                     0  
> Time Signature            0  
> Label                     0  
> dtype: int64  

Observando a tabela, se percebe que na coluna de gêneros artísticos há valores nulo, porém, não será removida.
# ESTATÍSTICA DESCRITIVA
Com a estatística descritiva, é possível ver a organização, descrição e representação dos dados.

## Distribuição de Frequências
Para uma primeira demonstração, serão visualizadas as tendências de ocorrências em determinadas datas registradas.

```python
chaves = ["Data", "Hit(s)"]

# valores para as chaves
count_data = df["Album Release Date"].value_counts()
```

```python
dados_datas = {chaves[i]: valores for i, valores in enumerate([list(count_data.index),
                                                               list(count_data.values)])}
```

```python
df_datas = pd.DataFrame(dados_datas).sort_values(by="Data")
```

Existem 3331 registros, distribuídos entre 1956-03-23 e 2023-06-30. Com isso, é possível visualizar de forma objetiva as tendências por data em um gráfico de linhas.

```python
import plotly.graph_objects as go
import plotly.express as px
```

```python
tema = px.colors.qualitative.Light24
```

```python
hit_sazonal = go.Scatter(x=df_datas.Data, y=df_datas["Hit(s)"], mode="lines",
                         line=dict(color=tema[2]))

layout_hits = go.Layout(title=dict(text="ESCALA DE HITS ENTRE 1956 E 2023",
                                   x=0.5, font_size=22),
                        xaxis=dict(title="Data"), yaxis=dict(title="Hit (s)"),
                        height=600)

graf_hits = go.Figure(data=hit_sazonal, layout=layout_hits)

graf_hits.update_layout(xaxis_range=["1990", "2020"], plot_bgcolor="#F9F9F9")

graf_hits.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
graf_hits.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                       rangeslider_visible=True)
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_hits.png)

Com isso, é possível notar uma crescente nos registros entre o período de 2005 a 2014, com picos em datas específicas.  
É de suma importância saber quais gêneros musicais foram os mais ouvidos, segundo a pesquisa.

```python
df["Artist Genres"].nunique()
```

> 2815

Há um total de 2815 gêneros ou combinações de gêneros registrados, porém, serão visualizados apenas os 10 mais ouvidos.

```python
top_generos = df["Artist Genres"].value_counts()[:10].index
```

```python
df_top_gen = df[df["Artist Genres"].isin(top_generos)][["Artist Genres",
                                                        "Explicit"]]
df_top_gen.head()
```

Uma visualização no gráfico de barras pode ajudar a compreender a frequência absoluta dos dados.

```python
graf_top_gen = px.histogram(df_top_gen, x="Artist Genres", width=900,
                            height=600, text_auto=True, color="Artist Genres",
                            color_discrete_sequence=tema)

graf_top_gen.update_layout(font_size=12,
                           yaxis=dict(title="Quantidade"),
                           title=dict(text="TOP GÊNEROS MAIS OUVIDOS",
                                      x=0.5, font_size=22), showlegend=False,
                           plot_bgcolor="rgb(250, 250, 250)")

graf_top_gen.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                          categoryorder="total descending", title=None)

graf_top_gen.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_top_gen.png)

Mesmo entre o Top Gêneros ouvidos, dance pop, australian rock e pop despontam dos demais. Além disso, seria interessante verificar o nível de explicicidade entre os gêneros mais ouvidos.

```python
labels = df_top_gen["Explicit"].value_counts().index
values = df_top_gen["Explicit"].value_counts().values
```

```python
graf_explicit = go.Figure(go.Pie(labels=labels, values=values,
                                 texttemplate="%{label}<br>%{percent}",
                                 hole=0.25,
                                 marker=dict(colors=[tema[i] for i in [13, 0]])))

graf_explicit.update_layout(width=600, height=550, font_size=12, showlegend=False,
                            title=dict(text="PERCENTUAL DE EXPLICITUDE NAS MÚSICAS",
                                       x=0.5, font_size=22),
                            annotations=[dict(text=f"<b>TOTAL<br>{sum(values)}</b>",
                                              x=0.5, y=0.5, font_size=14,
                                              showarrow=False)])
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_explicit.png)

Apenas 3,63% das músicas mais ouvidas são explícitas. Também é possível ver como a explicitude se distribui entre os gêneros.

```python
graf_exp_gen = px.histogram(df_top_gen, x="Artist Genres", width=900,
                            height=600, text_auto=True, color="Explicit",
                            color_discrete_sequence=[tema[i] for i in [13, 0]])

graf_exp_gen.update_layout(font_size=12,
                           yaxis=dict(title="Quantidade"),
                           title=dict(text="TOP GÊNEROS MAIS OUVIDOS - EXPLICITUDE",
                                      x=0.5, font_size=22),
                           plot_bgcolor="rgb(250, 250, 250)", showlegend=False)

graf_exp_gen.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                          categoryorder="total descending", title=None)

graf_exp_gen.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_exp_gen.png)

Com isso, é possível verificar se os Top Artistas estão enquadrados nestas categorias ou não.

```python
df["Artist Name(s)"].nunique()
```

> 4128

Há um total de 4128 artistas, porém, será feita uma visualização acerca dos os 100 mais bem pontuados nas paradas.

```python
top_artistas = df["Artist Name(s)"].value_counts().nlargest(100)
top_artistas
```

```python
import matplotlib.pyplot as plt
from wordcloud import WordCloud
```

```python
wordcloud = WordCloud(width=800, height=400,
                      background_color='white').generate_from_frequencies(top_artistas.to_dict())

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off'); # Remove os eixos
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/wordcloud.png)

Assim, se tem uma visualização "estilosa" dos 100 artistas mais ouvidos, porém, ainda é possível verificar o Top 12 Artistas com um gráfico de barras, por exemplo.

```python
top_12 = top_artistas[:12].index
```

```python
df_top_12 = df[df["Artist Name(s)"].isin(top_12)][["Artist Name(s)",
                                                   "Artist Genres", "Explicit"]]
```

O gráfico de barras ajudará a visualizar os artistas mais ouvidos, bem como seu gênero musical.

```python
graf_top_art_gen = px.histogram(df_top_12, x="Artist Name(s)",
                                width=900, text_auto=True,
                                color="Artist Genres",
                                color_discrete_sequence=tema)

graf_top_art_gen.update_layout(font_size=12, xaxis=dict(title="Categoria"),
                               yaxis=dict(title="Hit (s)"),
                               title=dict(text="TOP 12 ARTISTAS COM MAIS HITS - GÊNERO MUSICAL",
                                          x=0.5, font_size=22),
                               plot_bgcolor="rgb(250, 250, 250)",
                               showlegend=False)

graf_top_art_gen.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                              categoryorder="total descending", title=None)

graf_top_art_gen.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_top_art_gen.png)

Com isso, vemos que, o gênero pop e dance pop dominam com dois representantes cada. Além disso, seria interessante verificar se os artistas mais populares tem músicas explícitas ou não.

```python
graf_top_art_exp = px.histogram(df_top_12, x="Artist Name(s)", width=900,
                                text_auto=True, color="Explicit",
                                color_discrete_sequence=[tema[i] for i in [13, 0]])

graf_top_art_exp.update_layout(font_size=12, xaxis=dict(title="Categoria"),
                               yaxis=dict(title="Hit (s)"),
                               title=dict(text="TOP 12 ARTISTAS COM MAIS HITS - EXPLICITUDE",
                                          x=0.5, font_size=22),
                               plot_bgcolor="rgb(250, 250, 250)",
                               showlegend=False)

graf_top_art_exp.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                              categoryorder="total descending", title=None)

graf_top_art_exp.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_top_art_exp.png)

Ao olhar o gráfico, se percebe que apenas a artista P!nk aparece com hits explícitos.  
Outra comparação interessante, seria entre as 4 músicas mais populares, para ver se as mesmas encontram similaridade entre si.

```python
df_top_pop = df[["Artist Name(s)", "Track Name", "Artist Genres", "Popularity",
                 "Danceability", "Energy", "Speechiness", "Acousticness",
                 "Instrumentalness", "Liveness",
                 "Valence"]].sort_values(["Popularity"], ascending=False)[:4].reset_index(drop=True)
df_top_pop
```

```python
titulos = df_top_pop["Track Name"]
```

```python
df_top_pop.drop(columns=['Track Name', 'Artist Name(s)', 'Artist Genres',
                         'Popularity'], inplace=True)
```

```python
from plotly.subplots import make_subplots
```

```python
graf_radar = make_subplots(rows=2, cols=2, subplot_titles=titulos,
                           specs=[[{"type": "polar"}, {"type": "polar"}],
                                  [{"type": "polar"}, {"type": "polar"}]])

for i, linha in enumerate(df_top_pop.values):
    trace = go.Scatterpolar(r=linha, theta=df_top_pop.columns, fill="toself")

    graf_radar.add_trace(trace, row=(i // 2) + 1, col=(i % 2) + 1)

    graf_radar.update_polars(radialaxis_range=[0, 1.0], row=(i // 2) + 1,
                             col=(i % 2) + 1)

graf_radar.update_layout(title=dict(text="TOP 4 MÚSICAS MAIS POPULARES", x=0.5,
                                    font_size=22), showlegend=False, width=900,
                         height=750)
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/graf_radar.png)

Olhando para os gráficos, é possível notar que todas as músicas encontram certa similaridade entre Energy e Danceability.  
# ESTATÍSTICA INFERENCIAL

## Regressão e Correlação Linear
Para se saber se há correlação entre as variáveis das músicas, um mapa de calor pode ser utilizado.

```python
df_corr = df.copy()[["Track Duration (ms)", "Popularity", "Danceability",
                     "Energy", "Key", "Loudness", "Mode", "Speechiness",
                     "Acousticness", "Instrumentalness", "Liveness", "Valence",
                     "Tempo", "Time Signature"]].corr(method="pearson")

mapa_calor = px.imshow(df_corr, text_auto=True, height=1000)

mapa_calor.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

mapa_calor.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/mapa_calor.png)

Olhando para o mapa de calor, é possível perceber uma correlação moderada positiva, entre Energy e Loudness e uma negativa, entre Energy e Acousticness. Além disso, a visualização dessas variáveis pode ser vista a partir de um gráfico de dispersão.

```python
corr_positiva = px.scatter(x=df.Energy, y=df.Loudness, width=1000,
                           trendline="ols", trendline_color_override='red')

corr_positiva.update_layout(font_size=12, xaxis=dict(title="Energy"),
                            yaxis=dict(title="Loudness"),
                            title=dict(text="Correlação Linear Positiva Moderada - Energy x Loudness",
                                       x=0.5, font_size=22),
                            plot_bgcolor="rgb(245, 245, 245)")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/corr_positiva.png)

Dessa forma, se percebe que, enquanto a intensidade da música aumenta, há uma certa tendência de que a sonoridade também o faça. Essa correlação implica em músicas consideradas "rápidas e barulhentas", onde podem ser complexas, instrumental e harmonicamente falando.

```python
corr_negativa = px.scatter(x=df.Energy, y=df.Acousticness, width=1000,
                           trendline="ols", trendline_color_override='red')

corr_negativa.update_layout(font_size=12, xaxis=dict(title="Energy"),
                            yaxis=dict(title="Acousticness"),
                            title=dict(text="Correlação Linear Negativa Moderada - Energy x Acousticness",
                                       x=0.5, font_size=22),
                            plot_bgcolor="rgb(245, 245, 245)")
```

![](https://github.com/pyrataria/data_analytics/blob/main/spotipy/resources/images/corr_negativa.png)

Apesar de haver muitos dados fora da curva, esta correlação ainda é considerada moderada e pode sugerir que, à medida que a intensidade e atividade da música aumenta (alta energia), a tendência é que a música seja menos acústica e mais eletrônica (baixa acústica). Assim, isso pode indicar que músicas mais intensas e enérgicas têm uma maior probabilidade de conter elementos eletrônicos e processados digitalmente, em vez de instrumentos acústicos.