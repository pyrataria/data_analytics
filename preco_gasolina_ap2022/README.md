Projeto de análise descritiva, sobre o preço da gasolina comum no ano de 2022, nos postos Automoto - Automóveis do Amapá, com base em 12 conjuntos de dados, disponível na "[Série Histórica de Preços de Combustíveis](https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-por-revenda)", do Portal de Dados Abertos do governo.

# IDENTIFICAÇÃO DA POPULAÇÃO DO ESTUDO E DAS VARIÁVEIS DE INTERESSE
A população de estudo será dada com base nos dados dos postos Automoto no estado do Amapá.

## Manipulação de Dados
A biblioteca para manipulação de dados a ser utilizada neste projeto será o pandas.

### Importação do Pandas e leitura dos dataframes
```python
import pandas as pd
```

Serão utilizados 12 conjuntos de dados para o estudo, que serão concatenados em um único dataframe posteriormente.

```python
df_jan = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-01.csv",
                 sep=';')
df_jan.head()
```

```python
df_fev = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-02.csv",
                 sep=';')
df_mar = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-03.csv",
                 sep=';')
df_abr = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-04.csv",
                 sep=';')
df_mai = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-05.csv",
                 sep=';')
df_jun = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-06.csv",
                 sep=';')
df_jul = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-07.csv",
                 sep=';')
df_ago = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-08.csv",
                 sep=';')
df_set = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-09.csv",
                 encoding="iso-8859-1", sep=';')
df_out = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-10.csv",
                 sep=';')
df_nov = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-11.csv",
                 encoding="iso-8859-1", sep=';')
df_dez = pd.read_csv("/content/drive/MyDrive/estudo_etanol_gasolina_comum2022/precos-gasolina-etanol-12.csv",
                 sep=';')
```

### Organização dos dados
Os quadros de dados serão ordenados pela variável Data da Coleta, que contém a data em que o registro foi feito.

```python
frames = [df_jan, df_fev, df_mar, df_abr, df_mai, df_jun, df_jul, df_ago,
          df_set, df_out, df_nov, df_dez]
```

```python
frames_ord = [frame.sort_values(by="Data da Coleta") for frame in frames]
```

```python
df = pd.concat(frames_ord)
df
```

```python
df.shape
```
> (603015, 16)

O dataframe df contém os dados de todo o Brasil, com um ottal de 603015 registros (linhas) e 16 variáveis (colunas).

### Populaçao de estudo
Será feita uma amostragem, contendo apenas os dados do estado do Amapá.

```python
df_ap = df.copy().rename(columns={"Estado - Sigla": "SIGLA_ESTADO"}).query("SIGLA_ESTADO == 'AP'")
df_ap.head()
```

```python
df_ap.shape
```
> (1391, 16)

O estado do Amapá possui um total de 1391 registros.

#### Renomeando variáveis
As variáveis serão colocadas em caixa-alta e separadas por underline.

```python
df_ap.rename(columns={"Regiao - Sigla": "SIGLA_REGIAO"},
             inplace=True)
```

```python
ajuste_variavel = {i:i.upper().replace(" ", "_") for i in df_ap.columns}
```

```python
df_ap.rename(columns=ajuste_variavel, inplace=True)
```

```python
df_ap.columns
```
> Index(['SIGLA_REGIAO', 'SIGLA_ESTADO', 'MUNICIPIO', 'REVENDA',  
>       'CNPJ_DA_REVENDA', 'NOME_DA_RUA', 'NUMERO_RUA', 'COMPLEMENTO', 'BAIRRO',  
>       'CEP', 'PRODUTO', 'DATA_DA_COLETA', 'VALOR_DE_VENDA', 'VALOR_DE_COMPRA',  
>       'UNIDADE_DE_MEDIDA', 'BANDEIRA'],  
>      dtype='object')

#### Renomeando registros
Os registros do tipo object (texto) serão renomeados, para facilitar a visualização na tabela.

```python
registro_antigo = [[j for j in df_ap[i]] for i in df_ap.columns]
```

```python
ajuste_registro = [[j.title() if isinstance(j, str) else j
                    for j in df_ap[i]] for i in df_ap.columns]
```

```python
for var, i in zip(df_ap.columns, list(range(len(df_ap.columns)))):
    df_ap.replace(registro_antigo[i], ajuste_registro[i], inplace=True)
```

```python
df_ap.head()
```

```python
df_ap.dtypes
```
> SIGLA_REGIAO          object  
> SIGLA_ESTADO          object  
> MUNICIPIO             object  
> REVENDA               object  
> CNPJ_DA_REVENDA       object  
> NOME_DA_RUA           object  
> NUMERO_RUA            object  
> COMPLEMENTO           object  
> BAIRRO                object  
> CEP                   object  
> PRODUTO               object  
> DATA_DA_COLETA        object  
> VALOR_DE_VENDA        object  
> VALOR_DE_COMPRA      float64  
> UNIDADE_DE_MEDIDA     object  
> BANDEIRA              object  
> dtype: object

#### Estratificação da população
A população será estratificada com base na gasolina do tipo comum e na revenda com maior ocorrência de dados.

```python
df_ap.PRODUTO.value_counts()
```
> Gasolina              1163  
> Gasolina Aditivada     183  
> Etanol                  45  
> Name: PRODUTO, dtype: int64

```python
df_ap.REVENDA.value_counts()
```
> Automoto - Automoveis Do Amapa Ltda          331  
> Automoto Combustiveis Do Amapa Ltda          193  
> Sepe Tiaraju Empreendimentos Eireli          115  
> Comercial Grao De Ouro Ltda                  106  
> Posto De Combustiveis Jardins Eireli         102  
> Claudionor Costa Dos Santos                   83  
> Posto Iccar Ltda                              70  
> Grampos Oiapoc Ltda                           64  
> Real Petróleo Ltda                            63  
> J C Da S Farias Eireli                        62  
> Auto Posto Machado Ltda                       62  
> Auto Posto Terceiro Milênio Ltda              38  
> Souza & Cavalcante Comercio Ltda              24  
> Monte & Filhos Ltda                           21  
> Aeroposto Combustiveis Automotivos Ltda       18  
> J. C. S. Guimaraes Ltda                       14  
> Posto Catarinao Eireli                        10  
> Auto Posto Playcenter Ltda                     4  
> Machado & Andrade Ltda                         3  
> Auto Posto Amazonas Stn Ltda                   2  
> R E R Empreendimentos Eireli                   2  
> C G Andrade Nonato                             1  
> Posto Colonial Norte Ltda                      1  
> Postos Gabriel Ii Ltda                         1  
> Concessionaria Rocha Empreendimentos Ltda      1  
> Name: REVENDA, dtype: int64

A revenda com maior ocorrência de dados é a Automoto - Automoveis Do Amapa Ltda.

```python
automoto_atmv = df_ap.copy().query("PRODUTO == 'Gasolina'\
and REVENDA == 'Automoto - Automoveis Do Amapa Ltda'")
automoto_atmv.head()
```

Verificando se há registros vazios na variável VALOR_DE_VENDA.

```python
automoto_atmv.VALOR_DE_VENDA.isnull().value_counts()
```
> False    330  
> Name: VALOR_DE_VENDA, dtype: int64

Serão removidas variáveis que não serão utilizadas nos estudos.

```python
automoto_atmv.SIGLA_REGIAO.value_counts()
```
> N    330  
Name: SIGLA_REGIAO, dtype: int64

```python
automoto_atmv.SIGLA_ESTADO.value_counts()
```
> Ap    330  
> Name: SIGLA_ESTADO, dtype: int64

```python
automoto_atmv.VALOR_DE_COMPRA.isnull().value_counts()
```
> True    330  
> Name: VALOR_DE_COMPRA, dtype: int64

```python
automoto_atmv.drop(columns=["PRODUTO", "REVENDA", "SIGLA_ESTADO",
                            "SIGLA_REGIAO", "VALOR_DE_COMPRA"], inplace=True)
```

```python
automoto_atmv.shape
```
> (330, 11)

Será necessário fazer uma mudança do tipo da variável VALOR_DE_VENDA, suprindo a necessidade de operações numéricas do estudo.

```python
vv_novo = [i.replace(",", ".") for i in automoto_atmv.VALOR_DE_VENDA]
```

```python
automoto_atmv.VALOR_DE_VENDA.replace(automoto_atmv.VALOR_DE_VENDA.values,
                                     vv_novo, inplace=True)
```

```python
automoto_atmv["VALOR_DE_VENDA"] = automoto_atmv.VALOR_DE_VENDA.astype(float)
```

A população a ser utilizada no estudo contemplará os 4 bairros com maior quantidade de dados.

```python
automoto_atmv.BAIRRO.value_counts()
```
> Central           103  
> Pacoval            47  
> Santa Rita         40  
> Buritizal          39  
> Trem               28  
> Novo Horizonte     22  
> Infraero           21  
> Congos             12  
> Novo Buritizal     11  
> Sao Jose            7  

```python
bairros = list(automoto_atmv.BAIRRO.value_counts().index)[:4]
```

```python
automoto_atmv2 = automoto_atmv.copy()[automoto_atmv["BAIRRO"].isin(bairros)]
automoto_atmv2.head()
```

# DESCRIÇÃO DOS DADOS

## Medidas de Tendência Central
Com as Medidas de Tendência Central, o conjunto de dados pode ser representado como um todo, com suas características sendo identificadas.

Tendo em vista que o conjunto de dados é datado ao ano de 2022, será feito um ajuste na data, para facilitar a visualização dos dados.

```python
ajuste_data = [i.replace("/2022", '') for i in automoto_atmv2.DATA_DA_COLETA]
```

```python
automoto_atmv2.DATA_DA_COLETA.replace(automoto_atmv2.DATA_DA_COLETA.values,
                                      ajuste_data, inplace=True)
```

Serão criado 4 subdataframes, para as medidas de tendência central e uso posterior.

```python
atmv_bairro1 = automoto_atmv2[automoto_atmv2.BAIRRO == bairros[0]]
atmv_bairro2 = automoto_atmv2[automoto_atmv2.BAIRRO == bairros[1]]
atmv_bairro3 = automoto_atmv2[automoto_atmv2.BAIRRO == bairros[2]]
atmv_bairro4 = automoto_atmv2[automoto_atmv2.BAIRRO == bairros[3]]
```

**Média:**  
Com a média, têm-se a concentração dos dados.

```python
md_b1 = round(atmv_bairro1.VALOR_DE_VENDA.mean(), 3)
md_b2 = round(atmv_bairro2.VALOR_DE_VENDA.mean(), 3)
md_b3 = round(atmv_bairro3.VALOR_DE_VENDA.mean(), 3)
md_b4 = round(atmv_bairro4.VALOR_DE_VENDA.mean(), 3)
```

**Moda:**  
A moda mostra o valor, ou valores que mais se repetem nos dados.

```python
mod_b1 = list(atmv_bairro1.VALOR_DE_VENDA.mode())
mod_b2 = list(atmv_bairro2.VALOR_DE_VENDA.mode())
mod_b3 = list(atmv_bairro3.VALOR_DE_VENDA.mode())
mod_b4 = list(atmv_bairro4.VALOR_DE_VENDA.mode())
```

**Mediana:**  
Com a mediana obtemos o valor central no dataset.

```python
mdn_b1 = round(atmv_bairro1.VALOR_DE_VENDA.median(), 3)
mdn_b2 = round(atmv_bairro2.VALOR_DE_VENDA.median(), 3)
mdn_b3 = round(atmv_bairro3.VALOR_DE_VENDA.median(), 3)
mdn_b4 = round(atmv_bairro4.VALOR_DE_VENDA.median(), 3)
```

```python
dados_mtc = {"MEDIA": [md_b1, md_b2, md_b3, md_b4],
             "MODA": [mod_b1, mod_b2, mod_b3, mod_b4],
             "MEDIANA": [mdn_b1, mdn_b2, mdn_b3, mdn_b4]}
```

```python
df_mtc = pd.DataFrame(dados_mtc, index=bairros)
df_mtc
```

Apesar de se tratar de 4 postos de vendas diferentes, as medidas de tendência central encontram-se em coesão, pois tratam-se da mesma revenda.

## Visualização dos Dados

### Boxplot
O boxplot representa a distribuição dos dados no conjunto. O mesmo contém os 4 postos com maior quantidade de dados.

```python
import plotly.express as px
```

```python
tema = px.colors.qualitative.Light24
```

```python
boxplot_precos = px.box(automoto_atmv2, y="VALOR_DE_VENDA", color="BAIRRO",
                   points="all", notched=True,
                   color_discrete_sequence=tema)

boxplot_precos.update_layout(width=1000, plot_bgcolor="#F9F9F9",
                        title=dict(text="Automoto - Automoveis Do Amapá\
 Ltda.<br>Preço da Gasolina 2022<br>", x=0.5, y=0.96, font_size=22),
                        legend=dict(title="Bairro", bgcolor="#F9F9F9",
                                    bordercolor="#D0D1D3", borderwidth=1,
                                    font=dict(size=14)))

boxplot_precos.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

boxplot_precos.update_yaxes(title="Valor de Venda", showline=True, linewidth=1,
                            linecolor="lightgrey", tickprefix="R$")
```

![](https://github.com/pyrataria/data_analytics/blob/main/preco_gasolina2022/resources/images/01_boxplot.png)

Com este resultado, é possível perceber que a amplitude escalar do preço da gasolina entre os 4 postos encontra semelhança entre si, bem como a centralidade dos dados nos conjuntos. É possível notar ainda que, entre a mediana e o limite inferior dos dados, há uma dispersão maior no conjunto de dados, enquanto que entre a mediana e o limite superior, os dados estão mais concentrados.

### Escala de preços
A escala de preços em relação a data revela a variação do preço da gasolina comum em determinada data.

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go
```

```python
dados_precos = go.Scatter(x=automoto_atmv2.DATA_DA_COLETA,
                          y=automoto_atmv2.VALOR_DE_VENDA, mode="lines",
                          line=dict(color=tema[0]))

layout_precos = go.Layout(title=dict(text="Escala de Preços 2022 - \
Postos Automoto", x=0.5, font_size=22),
                          xaxis=dict(title="Data"),
                          yaxis=dict(title="Preço"), height=600)

indice_precos = go.Figure(data=dados_precos, layout=layout_precos)

indice_precos.update_layout(xaxis_range=[15, 50], plot_bgcolor="#F9F9F9")

indice_precos.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey",
                           tickprefix="R$")
indice_precos.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                           rangeslider_visible=True)
```

![](https://github.com/pyrataria/data_analytics/blob/main/preco_gasolina2022/resources/images/02_rangeslider.gif)

Com base na representação gráfica, é possível notar que entre o período de 25/04 a 22/06, houve uma consistência no preço da gasolina. Após este período,houve uma decrescente até o dia 28/09.  
Vejamos esta relação, tendo em vista os 4 postos analisados anteriormente, de forma separada.

```python
quadro_precos = make_subplots(rows=2, cols=2, subplot_titles=bairros)

quadro_precos.add_trace(go.Scatter(x=atmv_bairro1.DATA_DA_COLETA,
                         y=atmv_bairro1.VALOR_DE_VENDA,
                         line=dict(color=tema[0]),
                         name=bairros[0]), row=1, col=1)

quadro_precos.add_trace(go.Scatter(x=atmv_bairro2.DATA_DA_COLETA,
                         y=atmv_bairro2.VALOR_DE_VENDA,
                         line=dict(color=tema[1]),
                         name=bairros[1]), row=1, col=2)

quadro_precos.add_trace(go.Scatter(x=atmv_bairro3.DATA_DA_COLETA,
                         y=atmv_bairro3.VALOR_DE_VENDA,
                         line=dict(color=tema[2]),
                         name=bairros[2]), row=2, col=1)

quadro_precos.add_trace(go.Scatter(x=atmv_bairro4.DATA_DA_COLETA,
                         y=atmv_bairro4.VALOR_DE_VENDA,
                         line=dict(color=tema[3]),
                         name=bairros[3]), row=2, col=2)

quadro_precos.update_traces(mode="lines")

quadro_precos.update_layout(height=700, plot_bgcolor="white",
                  title=dict(text="Automoto - Automoveis Do Amapá Ltda.<br>\
Preço da Gasolina 2022<br>", x=0.5, y=0.95, font_size=22),
                  legend=dict(title="Bairros", bgcolor="#F9F9F9",
                              bordercolor="#D0D1D3", borderwidth=1,
                              font=dict(size=14)))

quadro_precos.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                 tickangle=45)
quadro_precos.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey",
                 tickprefix="R$")
```

![](https://github.com/pyrataria/data_analytics/blob/main/preco_gasolina2022/resources/images/03_relacao.png)

Há similaridade quanto a visualização gráfica em relação ao preço da gasolina comum entre os 4 postos.

# SALVANDO O CONJUNTO DE DADOS
É possível salvar o conjunto de dados tratado contendo todos os postos de vendas dos postos Automoto Automóveis do Amapá Ltda. em um arquivo csv.

```python
automoto_atmv.to_csv("gasolina_2022_automoto_atmv.csv", index=False)
```