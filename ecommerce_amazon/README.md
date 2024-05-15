Conjunto de dados com de mais de 1.000 registros, contendo informações sobre produtos relativos ao e-commerce da empresa Amazon. O mesmo é proveniente de terceiros, adquirido por meio da plataforma Kaggle.  

**Sobre o projeto**  
A empresa Amazon.com, Inc. é uma empresa multinacional de tecnologia norte-americana com sede em Seattle, Washington. A companhia trabalha na área do e-commerce, computação em nuvem, streaming e inteligência artificial.
Neste projeto, ao discorrer sobre dados inerentes ao e-commerce da empresa, o observador terá esclarecimento acerca de algumas questões, relativas a compras no âmbito de loja virtual da Amazon. Ao final, serão respondidas algumas perguntas de negócio.

# PREPARAÇÃO, ORGANIZAÇÃO E ESTRUTURAÇÃO DOS DADOS
Para a mabipulação e análise de dados, será utilizada a biblioteca [pandas](https://pandas.pydata.org/).

```python
import pandas as pd

pd.set_option("display.max_columns", 30) # altera o número máximo de colunas a serem exibidas

df = pd.read_csv("/content/drive/MyDrive/projetos/amazon/amazon.csv")
df
```

```python
df.shape
```
> (1465, 16)

Inicialmente, percebe-se o conjunto de dados com uma totalidade de 16 variáveis e 1465 registros.

## Extração e Limpeza de Dados
### Removendo valores nulos
```python
df.isnull().sum()
```

> product_id             0
> product_name           0
> category               0
> discounted_price       0
> actual_price           0
> discount_percentage    0
> rating                 0
> rating_count           2
> about_product          0
> user_id                0
> user_name              0
> review_id              0
> review_title           0
> review_content         0
> img_link               0
> product_link           0
> dtype: int64

Verificando todos os registros, através das variáveis, percebe-se dois valores nulos em rating_count. Os registros contendo os valores nulos (NaN) não serão removidos, tendo em vista que a variável em questão será amplamente utilizada. Assim, estes registros nulos serão posteriormente tratados.

## Renomeando Variáveis e Registros

### Renomeando registros
Os registros da variável rating_count contendo valores nulos serão substituídos pelo valor 0 (zero).

```python
df[df.isnull().any(axis=1)]
```

```python
df.rating_count.fillna("0", inplace=True)
```

```python
df.isnull().sum()
```

> product_id             0
> product_name           0
> category               0
> discounted_price       0
> actual_price           0
> discount_percentage    0
> rating                 0
> rating_count           0
> about_product          0
> user_id                0
> user_name              0
> review_id              0
> review_title           0
> review_content         0
> img_link               0
> product_link           0
> dtype: int64

Com isso, os valores nulos foram substituídos . Podemos verificar essa substituição através do método loc.

```python
df.loc[[282, 324]]
```


### Renomeando variáveis
Todas as variáveis serão renomeadas e postas em caixa-alta, para diferenciação dos registros e melhor entendimento do dataframe.

```python
novas_cols = ["ID_PRODUTO", "NOME_PRODUTO", "CATEGORIA", "DESCONTO",
              "PRECO_REAL", "PORCENTAGEM_DESCONTO", "AVALIACAO",
              "TOTAL_AVALIACOES", "INFORMACOES", "ID_USUARIO", "USUARIO",
              "ID_REVISAO", "TITULO_REVISAO", "REVISAO", "URL_IMAGEM",
              "URL_PRODUTO"]
```

```python
ajuste_var = {df.columns[i]:novas_cols[i] for i in range(len(df.columns))}
ajuste_var
```

> {'product_id': 'ID_PRODUTO',
>  'product_name': 'NOME_PRODUTO',
>  'category': 'CATEGORIA',
>  'discounted_price': 'DESCONTO',
>  'actual_price': 'PRECO_REAL',
>  'discount_percentage': 'PORCENTAGEM_DESCONTO',
>  'rating': 'AVALIACAO',
>  'rating_count': 'TOTAL_AVALIACOES',
>  'about_product': 'INFORMACOES',
>  'user_id': 'ID_USUARIO',
>  'user_name': 'USUARIO',
>  'review_id': 'ID_REVISAO',
>  'review_title': 'TITULO_REVISAO',
>  'review_content': 'REVISAO',
>  'img_link': 'URL_IMAGEM',
>  'product_link': 'URL_PRODUTO'}

```python
df.rename(columns=ajuste_var, inplace=True)
```

```python
df.columns
```
> Index(['ID_PRODUTO', 'NOME_PRODUTO', 'CATEGORIA', 'DESCONTO', 'PRECO_REAL',
>        'PORCENTAGEM_DESCONTO', 'AVALIACAO', 'TOTAL_AVALIACOES', 'INFORMACOES',
>        'ID_USUARIO', 'USUARIO', 'ID_REVISAO', 'TITULO_REVISAO', 'REVISAO',
>        'URL_IMAGEM', 'URL_PRODUTO'],
>       dtype='object')

## Transformação de Dados
### Remoção de caracteres

```python
df.head()
```

Olhando para o conjunto de dados, se percebem alguns caracteres especiais. Sendo assim, faz-se necessário remover estes símbolos, presentes nas variáveis DESCONTO, PRECO_REAL, PORCENTAGEM_DESCONTO e TOTAL_AVALIACOES, para que seja possível efetuar operações matemáticas com as mesmas.

```python
def remove_char(i, *args): # função que remove determinado caracter
    for arg in args:
        i = i.replace(arg, '')

    return i
```

```python
df["DESCONTO"] = df.DESCONTO.apply(remove_char, args=('₹', ','))
```

```python
df["PRECO_REAL"] = df.PRECO_REAL.apply(remove_char, args=('₹', ','))
```

```python
df["PORCENTAGEM_DESCONTO"] = df.PORCENTAGEM_DESCONTO.apply(remove_char, args=('%'))
```

```python
df["TOTAL_AVALIACOES"] = df.TOTAL_AVALIACOES.apply(remove_char, args=(','))
```

### Modificando dados
Os valores da variável PORCENTAGEM_DESCONTO serão passados para a forma decimal, a fim de representar porcentagem na forma decimal.

```python
df["PORCENTAGEM_DESCONTO"] = df.PORCENTAGEM_DESCONTO.apply(lambda i: int(i)/100)
```

Será necessário remover a especificidade dos itens da variável CATEGORIA, fazendo uma generalização, para melhor entendimento e para futuras operações descritivas.

```python
df["CATEGORIA"] = df.CATEGORIA.apply(lambda x: x.split('|')[0])
```

O tipo de algumas variáveis será modificado, para que possam ser realizadas operações matemáticas com as mesmas.

> df.dtypes
> ID_PRODUTO               object
> NOME_PRODUTO             object
> CATEGORIA                object
> DESCONTO                 object
> PRECO_REAL               object
> PORCENTAGEM_DESCONTO    float64
> AVALIACAO                object
> TOTAL_AVALIACOES         object
> INFORMACOES              object
> ID_USUARIO               object
> USUARIO                  object
> ID_REVISAO               object
> TITULO_REVISAO           object
> REVISAO                  object
> URL_IMAGEM               object
> URL_PRODUTO              object
> dtype: object

```python
df["DESCONTO"] = df.DESCONTO.astype("float32") # número com casa decimal
```

```python
df["PRECO_REAL"] = df.PRECO_REAL.astype("float32")
```

```python
df["PORCENTAGEM_DESCONTO"] = df.PORCENTAGEM_DESCONTO.astype("float32")
```

```python
df["TOTAL_AVALIACOES"] = df.TOTAL_AVALIACOES.astype("int32") # número inteiro
```

> df.dtypes
> ID_PRODUTO               object
> NOME_PRODUTO             object
> CATEGORIA                object
> DESCONTO                float32
> PRECO_REAL              float32
> PORCENTAGEM_DESCONTO    float32
> AVALIACAO                object
> TOTAL_AVALIACOES          int32
> INFORMACOES              object
> ID_USUARIO               object
> USUARIO                  object
> ID_REVISAO               object
> TITULO_REVISAO           object
> REVISAO                  object
> URL_IMAGEM               object
> URL_PRODUTO              object
> dtype: object

```python
df
```


# ESTATÍSTICA DESCRITIVA
Com o dataframe tratado, será feita a organização, descrição e representação dos dados, através de métodos estatísticos descritivos.

## Distribuição de Frequências
É importante saber sobre a quantidade de ocorrências de determinados valores no conjunto de dados analisado. Para isso, é possível utilizar a distribuição de frequências.

Ao analisarmos a variável CATEGORIA, é possível ter uma noção sobre a demanda a determinado seguimento.

```python
import plotly.express as px
```

```python
tema = px.colors.qualitative.Light24
```

```python
cont_categoria = px.histogram(df, x="CATEGORIA", width=900, text_auto=True,
                              color_discrete_sequence=tema, color="CATEGORIA")

cont_categoria.update_layout(font_size=12, xaxis=dict(title="Categoria"),
                             yaxis=dict(title="Contagem"),
                             title=dict(text="CONTAGEM DE CATEGORIAS",
                                        x=0.5, font_size=22),
                             plot_bgcolor="rgb(250, 250, 250)",
                             showlegend=False)

cont_categoria.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                            categoryorder="total descending")

cont_categoria.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/ecommerce_amazon/resources/images/cont_categoria.png)

Com isso, percebesse uma quantidade de amostras polarizada.

A quantidade de avaliações acerca de determinado produto demonstra o interesse do consumidor em relatar algo sobre o mesmo. Assim, se faz necessário uma análise acerca disso.

```python
aval_categoria = px.strip(df, x="CATEGORIA", y="TOTAL_AVALIACOES", width=900,
                          color_discrete_sequence=tema, color="CATEGORIA")

aval_categoria.update_layout(font_size=12, xaxis=dict(title="Categoria"),
                             yaxis=dict(title="Contagem"),
                             title=dict(text="TOTAL DE AVALIAÇÕES POR CATEGORIA",
                                        x=0.5, font_size=22),
                             plot_bgcolor="rgb(250, 250, 250)",
                             showlegend=False)

aval_categoria.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

aval_categoria.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/ecommerce_amazon/resources/images/aval_categoria.png)

Ao olharmos para o gráfico, é possível perceber muitos comentários sobre determinados produtos de algumas categorias e alguns despontam em relação a outros da mesma categoria.

## Medidas de Tendência Central
Uma representação da concentração dos valores de determinada variável pode ser obtida com as medidas de tendência central.

Ao se analisar o percentual de desconto nas 4 categorias com maiores volumes de dados, utilizando a técnica do box plot, é possível verificar como os dados do percentual descontado estão distribuídos.

```python
plot_box = df[df.CATEGORIA.isin(df.CATEGORIA.value_counts().index[:4])]

perc_desc_cat = px.box(plot_box, y="PORCENTAGEM_DESCONTO", width=900,
                       color_discrete_sequence=tema, color="CATEGORIA",
                       notched=True)

perc_desc_cat.update_layout(font_size=12, plot_bgcolor="rgb(250, 250, 250)",
                            title=dict(text="PERCENTUAL DE DESCONTO POR CATEGORIA",
                                       x=0.5, font_size=22),
                            legend=dict(title="Categoria", bgcolor="#F9F9F9",
                                        bordercolor="#D0D1D3",
                                        borderwidth=1,
                                        font=dict(size=14)))

perc_desc_cat.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

perc_desc_cat.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey",
                           title="Percentual Descontado")
```

![](https://github.com/pyrataria/data_analytics/blob/main/ecommerce_amazon/resources/images/perc_desc_cat.png)

Ao se analisar o gráfico, nota-se que a centralidade dos dados para as categorias Computers&Accessories e Eletronics gira em torno de 50%. Olhando para a categoria OfficeProducts, percebesse um percentual de desconto baixo, se comparado ao das demais categorias, porém, alguns de seus valores despontaram como outliers, ou seja, valores fora da curva, assumindo até 75% de desconto.

# ESTATÍSTICA INFERENCIAL
A partir dos resultados apresentados, serão feitas análises, com o propósito de se obter o raciocínio necessário para a partir dos dados, se obter uma conclusão geral.

## Correlação Linear
Através da correlação linear, obtém-se relações estatísticas entre as variáveis, úteis para determinar (mensurar) o grau de relacionamento entre duas variáveis.

```python
mapa_calor = px.imshow(df.corr(method="pearson"), text_auto=True)

mapa_calor.update_layout(width=900, plot_bgcolor="rgb(250, 250, 250)",
                         title=dict(text="CORRELAÇÃO ENTRE VARIÁVEIS NUMÉRICAS",
                                    x=0.5, font_size=22))

mapa_calor.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

mapa_calor.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/ecommerce_amazon/resources/images/mapa_calor.png)

Ao olhar para o gráfico de calor, é possível perceber uma correlação positiva muito forte entre as variáveis PRECO_REAL e DESCONTO. Essa correlação pode ser visualizada através de um gráfico de dispersão.

```python
dispersao_precos = px.scatter(df, x="DESCONTO", y="PRECO_REAL", trendline="ols")

dispersao_precos.update_layout(font_size=12, xaxis=dict(title="Desconto"),
                               width=900, yaxis=dict(title="Preços"),
                               title=dict(text="CORRELAÇÃO ENTRE PREÇO REAL E DESCONTO",
                                          x=0.5, font_size=22),
                               plot_bgcolor="rgb(250, 250, 250)",
                               showlegend=False)

dispersao_precos.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey")

dispersao_precos.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")
```

![](https://github.com/pyrataria/data_analytics/blob/main/ecommerce_amazon/resources/images/dispersao_precos.png)

É possível confirmar uma correlação linear positiva em relação as variáveis PRECO_REAL e DESCONTO, ou seja, quando uma aumenta a outra também aumenta. Com isso, se entende que essas duas variáveis estão intimamente ligadas.

## Perguntas de Negócio
As seguintes perguntas de negócio serão respondidas:  

* Um item da categoria OfficeProducts tem quantos por cento de chance de possuir mais de 20% de desconto?
* Qual a chance de um produto da categoria Computers&Accessories não ter mais de 50% de desconto?
* Adquirindo um produto da categoria Electronics que custa mais ou ₹1000 (mil rúpias), qual a probabilidade de ele possuir mais de 60% de desconto?
* Ao se comprar 10 produtos da categoria Computers&Accessories, qual a chance de pelo menos um possuir um desconto maior ou igual a 80%?
* Ao se comprar 5 produtos da categoria Electronics, qual a probabilidade de nenhum possuir um desconto superior ou igual a 50%?  

**1) Um item da categoria OfficeProducts tem quantos por cento de chance de possuir mais de 20% de desconto?**

```python
prob = lambda A, E: round((A / E) * 100, 2) if A < E else False
```

```python
pergunta_1E = df[df.CATEGORIA.isin(["OfficeProducts"])]
pergunta_1A = pergunta_1E.query("PORCENTAGEM_DESCONTO > 0.20")
```

```python
prob(len(pergunta_1A), len(pergunta_1E))
```

> 19.35

A probabilidade de um item da categoria OfficeProducts possuir mais de 20% de desconto é de 19,35%.  

**2) Qual a chance de um produto da categoria Computers&Accessories não ter mais de 50% de desconto?**

```python
prob_nao = lambda A, E: round((1 - (A / E)) * 100, 2) if A < E else False
```

```python
pergunta_2E = df[df.CATEGORIA.isin(["Computers&Accessories"])]
pergunta_2A = pergunta_2E.query("PORCENTAGEM_DESCONTO > 0.50")
```

```python
prob_nao(len(pergunta_2A), len(pergunta_2E))
```

> 37.09

A chance de um produto da categoria Computers&Accessories não ter 50% de desconto (ou mais) é de 37.09%, o que torna uma chance relativamente moderada de possuir desconto superior a faixa indicada. Com isso, se deduz que produtos desta categoria geralmente possuem bons descontos.  

**3) Adquirindo um produto da categoria Electronics que custa mais ou ₹1000 (mil rúpias), qual a probabilidade de ele possuir mais de 60% de desconto?**

```python
pergunta_3E = df.loc[df.CATEGORIA == "Electronics"].query("PRECO_REAL > 1000")
pergunta_3A = pergunta_3E.query("PORCENTAGEM_DESCONTO > 0.60")
```

```python
prob(len(pergunta_3A), len(pergunta_3E))
```

> 36.5

Existe 36.5% de chance de um produto que custa mais de ₹1000 possuir mais de 60% de desconto.  

**4) Ao se comprar 10 produtos da categoria Computers&Accessories, qual a chance de pelo menos um possuir um desconto maior ou igual a 80%?**

```python
from scipy.stats import binom
```

```python
pergunta_4E = pergunta_2E.copy()
pergunta_4A = pergunta_4E.loc[pergunta_4E.PORCENTAGEM_DESCONTO >= 0.80]
p4 = prob(len(pergunta_4A), len(pergunta_4E)) / 100
```

```python
round((1 - binom.pmf(0, 10, p4)) * 100, 2)
```

> 62.2

A probabilidade de pelo menos um produto da categoria Computers&Accessories possuir um desconto maior que 70% é de 62,2%.  

**5) Ao se comprar 5 produtos da categoria Electronics, qual a probabilidade de nenhum possuir um desconto superior ou igual a 50%?**  

Para esta operação utilizaremos a função geom.pmf da biblioteca scipy, porém, será feito um pequeno ajuste, para ela retorna em forma de porcentagem arredondada.  

```python
from scipy.stats import geom
```

```python
geom_pmf = lambda n, p: round(geom.pmf(n, p) * 100, 2)
```

```python
pergunta_5E = df[df.CATEGORIA.isin(["Electronics"])]
pergunta_5A = pergunta_5E.query("PORCENTAGEM_DESCONTO >= 0.50")
p5 = prob(len(pergunta_5A), len(pergunta_5E)) / 100
```

```python
geom_pmf(6, p5)
```

> 0.9

As chances de tal prerrogativa ocorrer é baixíssima, não alcançando 1%. Assim, se entende que é quase certo que ao comprar um produto da categoria supracitada, ele terá um desconto igual ou superior a 50%.