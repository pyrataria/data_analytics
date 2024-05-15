Este estudo trata-se da relação da quantidade de louças lavadas em determinados dias dos mês de abril e busca averiguar se existe correlação entre as mesmas, quantidade de louças lavadas por categoria no referido mês, entre outros objetivos.  
A principal motivação do estudo, é relatar de forma visual e categórica os dados obtidos.

# COLETA DE DADOS
A coleta de dados foi feita de forma dinâmica, por mim mesmo (autor do estudo), por meio da lavagem da louças durante o mês de abril.

# ORGANIZAÇÃO E ANÁLISE DOS DADOS
Para a manipulação e análise exploratória dos dados, neste estudo, será utilizada a biblioteca *pandas*.

```python
import pandas as pd
```

```python
df = pd.read_csv("https://drive.google.com/uc?id=1uNPUMANzPrH4FSCo0odg5M-CgIgdyg24&export=download")
df.head()
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/img01.png)

```python
df.shape
```
> (17, 11)

O conjunto de dados é composto por 17 registros e 11 variáveis. Os registros representam a quantidade de dias em que foram obtidos os dados, que no caso, são a quantidade absoluta de louças por variável.

## Organizando Variáveis e Registros
Para se modificar o dataframe em uma série temporal, a variável (coluna) *DATA* será transformada em índice.

```python
df.set_index("DATA", inplace=True)
```

```python
df.index.names = [None] # remove o nome da variável transposta em índice
df.head()
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/img02.png)

## Análise dos Dados
**Valores Nulos**  
Primeiramento, será verificado se existem valores ausentes no dataframe.

```python
df.isnull().sum()
```

> TALHER          0  
> PRATO           0  
> TIGELA          0  
> COPO            0  
> XICARA          0  
> VASILHA-POTE    0  
> TAMPA           0  
> PANELA          0  
> OUTRO           0  
> DIA_SEM         0  
> dtype: int64  

Com isso, percebe-se que não existem valores faltantes.  

**Tipos dos Dados**  
É necessário também verificar o tipo dos dados, pois serão feitos cálculos com dados do tipo numérico.

```python
df.dtypes
```
> TALHER           int64  
> PRATO            int64  
> TIGELA           int64  
> COPO             int64  
> XICARA           int64  
> VASILHA-POTE     int64  
> TAMPA            int64  
> PANELA           int64  
> OUTRO            int64  
> DIA_SEM         object  
> dtype: object  

Olhando para o conjunto de dados, vê-se que as variáveis numéricas são do tipo inteiro, portanto não se faz necessário nenhum tipo de mudança no tipo dos dados.  
# ESTATÍTISCA DESCRITIVA
Com a estatística descritiva, serão sintetizados valores de mesma natureza, permitindo dessa forma que se tenha uma visão geral da variação desses valores, organização e descrição dos dados.

## Distribuição de Frequências
A distribuição de frequências se da por um conjunto, no qual os dados estão dispostos em grupos de classes ou categorias, dando assim uma noção da quantidade de ocorrência de determinado valor em sua respectiva classe.

### Frequência absoluta, relativa e percentual relativa
**Frequência Absoluta**  
A frequência absoluta demonstra a quantidade total de vezes que determinada variável ocorreu.

```python
df2 = pd.DataFrame(df.drop(columns=["DIA_SEM"]).sum(), columns=["FREQ_ABS"])
```

```python
df2.loc["TOTAL"] = df2.sum()[0]
```

Asism, temos o número total de ocorrências para cada variável do estudo, com acréscimo da quantidade total de louças lavadas, representado pela variável *TOTAL*.  

**Frequência Relativa**  
Mostra a taxa percentual de vezes que uma resposta aparece em relação ao todo.

```python
df2["FREQ_REL"] = round(df2.FREQ_ABS/df2.FREQ_ABS["TOTAL"], 3)
```

**Frequência Percentual Relativa**  
Demonstra a porcentagem de vezes que determinado aparece em relação ao todo.

```python
df2["FREQ_PERC_REL"] = round((df2.FREQ_ABS/df2.FREQ_ABS["TOTAL"])*100, 2)
df2
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/img03.png)

Com esta operação, vê-se que 34,63% dos itens estão acumulados na variável *TALHER*, com um total de 293 ocorrências, sendo estes a maioria.  
Além disso, ao analisar o registro *TOTAL*, percebe-se que foram lavadas **846** louças durante o mês de abril.  
### Visualização de frequências
**Distribuição por Categoria**  
É possível utilizar o gráfico de setores para visualizar a distribuição de frequências de louças lavadas durante o mês de abril.

```python
import plotly.express as px
import plotly.graph_objs as go
```

```python
tema = px.colors.qualitative.Light24
```

```python
labels = df2["FREQ_ABS"][:-1].index # nome dos setores
values = df2["FREQ_ABS"][:-1].values # valor dos setores
```

```python
# valores que se destacarão no gráfico
index_max = values.max()
index_min = values.min()
```

```python
dist_perc_loucas = go.Figure(go.Pie(labels=labels, values=values,
                                    texttemplate="%{label}<br>%{percent}",
                                    hoverinfo="label+value+percent", hole=0.25,
                                    pull=[0.2 if i in (index_min, index_max)
                                    else 0 for i in values],
                                    marker=dict(colors=tema)))

dist_perc_loucas.update_layout(height=600, width=700, font_size=12, showlegend=False,
                               title=dict(text="DISTRIBUIÇÃO PERCENTUAL DE LOUÇAS LAVADAS",
                                          x=0.5, font_size=22),
                               annotations=[dict(text=f"<b>TOTAL<br>{max(df2['FREQ_ABS'])}</b>",
                                                 x=0.5, y=0.5, font_size=14,
                                                 showarrow=False)])
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/dist_perc_loucas.png)

A categoria TALHER se destaca com o maior percentual de louças lavadas, alcançando 34.6%. Já a categoria *COPO*, é a com menor ocorrência de dados.  
Utilizando o gráfico de barras, é possível ter percepção acerca da quantidade absoluta de louças lavadas.

```python
dist_abs_loucas = px.bar(df2[:-1], y="FREQ_ABS", width=900, orientation='v',
                         text_auto=True, color=df2[:-1].T.columns,
                         color_discrete_sequence=tema,
                         custom_data=["FREQ_ABS", "FREQ_PERC_REL"])

dist_abs_loucas.update_traces(hovertemplate=["TOTAL: %{customdata[0]}<br>\
PORCENTAGEM: %{customdata[1]}%"])

dist_abs_loucas.update_layout(font_size=12, xaxis=dict(title=None),
                              yaxis=dict(title="Quantidade"),
                              title=dict(text="TOTAL DE LOUÇAS LAVADAS", x=0.5,
                                         font_size=22),
                              plot_bgcolor="rgb(245, 245, 245)",
                              showlegend=False)

dist_abs_loucas.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                             categoryorder="total descending")

dist_abs_loucas.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/dist_abs_loucas.png)

Ao se observar o gráfico de barras, fica claro o quanto a categoria *TALHER* se destaca das demais em quantidade de itens. Após ela, a categoria *TIGELA* aparece em maior quantidade, porém, esta não alcança 50% dos itens de TALHER.  

**Distribuição por Dia da Semana**  
Além disso, é possível verificar visualmente a quantidade de louças lavadas por dia da semana, concluindo asism se há um dia com maior "pico" de louça suja.

```python
df3 = df.groupby(["DIA_SEM"]).sum() # dataframe agrupado pelo dia da semana
```

```python
df3.index.names = [None]
df3
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/img04.png)

Agora, é possível verificar a frequência acumulada por dia da semana, fazendo o somatório dos registros.

```python
dist_loucas_sem = px.bar(df3.T.sum(), width=800, orientation='v',
                         text_auto=True, color=["seg", "ter", "qua", "qui",
                                                "sex", "sab"],
                         color_discrete_sequence=tema)

dist_loucas_sem.update_layout(font_size=12, showlegend=False,
                              title=dict(text="TOTAL DE LOUÇAS LAVADAS POR DIA DA SEMANA",
                                         x=0.5, font_size=22),
                              xaxis=dict(title=None, categoryarray=["seg", "ter",
                                                                    "qua", "qui",
                                                                    "sex", "sab"]),
                              yaxis=dict(title="Quantidade"), 
                              plot_bgcolor="rgb(245, 245, 245)")

dist_loucas_sem.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

dist_loucas_sem.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/dist_loucas_sem.png)

A partir desta distribuição, vê-se que o dia da semana (acumulando de todos os dias) que mais se lavou louças foi terça-feira e sábado foi o que menos se lavou. Também é possível notar que, excluindo o sábado, o dia útil da semana que menos se lavou louças foi segunda.  
Essa mesma representação pode ser feita observando as categorias de louça de forma independente.

```python
categorias = df3.keys()
dias = df3.index
```

```python
dist_loucas_cat = go.Figure()

for i, categoria in enumerate(categorias):
    freq_abs = [df3[categoria][dia] for dia in dias]
    dist_loucas_cat.add_trace(go.Bar(x=dias, y=freq_abs, name=categoria,
                                     marker_color=tema[i]))

dist_loucas_cat.update_layout(title=dict(text="TOTAL DE LOUÇAS LAVADAS POR DIA\
DA SEMANA EM CATEGORIAS",
                                         x=0.5, font_size=22),
                              xaxis=dict(categoryarray=["seg", "ter", "qua",
                                                        "qui", "sex", "sab"]),
                              yaxis_title='Quantidade',
                              legend=dict(title="Categoria", bgcolor="#F9F9F9",
                                          bordercolor="#D0D1D3", borderwidth=1,
                                          font=dict(size=14)),
                              plot_bgcolor="rgb(245, 245, 245)")
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/dist_loucas_cat.png)

Com isso, fica ainda mais evidente que a categoria TAHLHER sempre se destaca das demais em quantidade.  

## Medidas de Tendência Central
As medidas de tendência central representam o conjunto de dados como um todo, identificando as características apresentadas pelo conjunto.

```python
import warnings
```

```python
warnings.filterwarnings('ignore') # remove avisos (ignorem)
```

```python
data_df4 = {chave: int(valor) for chave, valor in round(df.mean()).items()}
```

```python
data_df4.update({"TOTAL": sum(data_df4.values())})
```

```python
df4 = pd.DataFrame(data_df4, index=["MÉDIA"]).T
df4
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/img05.png)

Olhando a tabela, percebe-se que em média, se lavou 50 louças por dia no mês de abril.  
Um gráfico de barras pode facilitar o entendimento.

```python
dist_med_loucas = px.bar(df4[:-1], width=900, orientation='v', text_auto=True,
                         color=df4[:-1].T.columns, color_discrete_sequence=tema)

dist_med_loucas.update_layout(font_size=12, xaxis=dict(title=None),
                              yaxis=dict(title="Média"), showlegend=False,
                              plot_bgcolor="rgb(245, 245, 245)",
                              title=dict(text="MÉDIA DE LOUÇAS LAVADAS", x=0.5,
                                         font_size=22))

dist_med_loucas.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                             categoryorder="total descending")

dist_med_loucas.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/dist_med_loucas.png)

É possível notar que o gráfico da média se assemelha bastante ao de frequência absoluta, com isso, podemos inferir que não há outliers (valores discrepantes) nos dados.  

## Estatística Inferencial

### Correlação de Pearson
Demonstra um grau de relação entre duas variáveis quantitativas e exprime o grau de **correlação** através de valores situados entre -1 e 1.
Quando o coeficiente de correlação se aproxima de 1, nota-se um aumento no valor de uma variável quando a outra também aumenta, ou seja, há uma **relação linear positiva**. Quando o coeficiente se aproxima de -1, também é possível dizer que as variáveis são correlacionadas, mas nesse caso quando o valor de uma variável aumenta o da outra diminui. Isso é o que é chamado de **correlação negativa** ou inversa.

```python
df5 = df.copy()
```

Será feita uma análise se há correlação entre as variáveis do estudo.

```python
df5.corr(method="pearson")
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/img06.png)

É possível visualizar esta correlação em um mapa de calor.

```python
mapa_calor = px.imshow(df5.corr(method="pearson"), text_auto=True);

mapa_calor.update_layout(width=800, height=800, plot_bgcolor="rgb(250, 250, 250)",
                         title=dict(text="CORRELAÇÃO ENTRE CATEGORIAS DE LOUÇAS",
                                    x=0.5, font_size=22))

mapa_calor.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

mapa_calor.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```
![](https://github.com/pyrataria/data_analytics/blob/main/loucas_sujas/resources/images/mapa_calor.png)

Com isso, se percebe correlação positiva moderada (acima de 0.50, ou 50%) entre algumas variáveis.  
Uma correlação que chama a atenção (pois já era esperada), é a entre as variáveis PANELA e TAMPA, porém, não é tão forte quanto se poderia imaginar.  
Além disso, é possível visualizar uma correlação moderada negativa entre outras variáveis também.