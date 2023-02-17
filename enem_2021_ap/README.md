Estudo estatístico onde serão abordadas dados sobre o ENEM 2021 no Estado do Amapá, comparando informações entre alunos de escolas públicas e privadas.  
Para esse estudo, será utilizado um dataset pré-tratado, relativo às provas do ENEM, realizadas no Amapá, que por sua vez, foi retirado dos [microdados](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) do ENEM 2021.

# IDENTIFICAÇÃO DA POPULAÇÃO DO ESTUDO E DAS VARIÁVEIS DE INTERESSE
## Importando o Pandas
A biblioteca [pandas](https://pandas.pydata.org/) será utilizada para a manipulação e análise de dados.

```python
import pandas as pd
```

```python
pd.set_option("display.max_columns", 100) # modifica o número de colunas a serem exibidas
```

```python
df = pd.read_csv("/content/drive/MyDrive/estudo_enem_ap/enem_2021_ap.csv",
                 encoding="iso-8859-1")
df.head()
```


```python
df.shape
```

> (11020, 52)

O número total de vestibulandos no Amapá é de 11020 pessoas.

## Identificação da População do Estudo e das Variáveis
A população de estudo será dividida em dois grupos de vestibulandos, por tipo de escola:
* pública
* privada

As populações de estudo podem ser encontradas na variável `TP_ESCOLA` do dataframe.


```python
df_estudo = df.copy()
```

```python
df.TP_ESCOLA.value_counts()
```
> nao_respondeu    7581  
> publica          2961  
> privada           478  
> Name: TP_ESCOLA, dtype: int64  

Nota-se que a maioria dos vestibulandos não responderam o tipo de escola.

### Removendo variáveis
Serão removidas variáveis que não serão utilizadas neste estudo, bem como os vestibulandos que não responderam ao questionário sobre qual tipo de escola frequentam.

```python
esc_invalida = df_estudo[df_estudo.TP_ESCOLA == "nao_respondeu"].index
```

```python
df_estudo.drop(esc_invalida, inplace=True)
df_estudo.shape
```

> (3439, 52)

```python
df_estudo.TP_ESCOLA.value_counts()
```

> publica          2961  
> privada           478  
> Name: TP_ESCOLA, dtype: int64  

O total de vestibulandos de escolas públicas e privadas é de 3439. Desses, 2961 matriculados em escolas públicas e 478 em escolas privadas.

```python
var_drop = ["ESTADO_CIVIL", "NACIONALIDADE", "ST_CONCLUSAO", "ANO_CONCLUSAO",
            "TP_ENSINO", "DEPENDENCIA_ADM_ESC", "UF_ESC", "LOCALIZACAO_ESC",
            "LOCALIZACAO_ESC", "SIT_FUNC_ESC"]
```

```python
df_estudo.drop(var_drop, axis=1, inplace=True)
df_estudo.shape
```

> (3439, 43)

Será adicionado uma variável contendo a nota final do vestibulando.

```python
provas = ["NOTA_CN", "NOTA_CH",  "NOTA_LC",  "NOTA_MT", "NOTA_REDACAO"]
nota_final = df_estudo[provas].sum(axis=1) / 5
df_estudo.insert(11, "NOTA_FINAL", nota_final)
df_estudo.shape
````

> (3439, 44)

### Transformação das faixas etárias, de numéricas para alfanuméricas

```python
df_estudo.FAIXA_ETARIA.replace({1:  "Menor de 17 anos",
                                2:  "17 anos",
                                3:  "18 anos",
                                4:  "19 anos",
                                5:  "20 anos",
                                6:  "21 anos",
                                7:  "22 anos",
                                8:  "23 anos",
                                9:  "24 anos",
                                10: "25 anos",
                                11: "Entre 26 e 30 anos",
                                12: "Entre 31 e 35 anos",
                                13: "Entre 36 e 40 anos",
                                14: "Entre 41 e 45 anos",
                                15: "Entre 46 e 50 anos",
                                16: "Entre 51 e 55 anos",
                                17: "Entre 56 e 60 anos",
                                18: "Entre 61 e 65 anos",
                                19: "Entre 66 e 70 anos",
                                20: "Maior de 70 anos"},
                               inplace=True)
```

```python
df_estudo.head()
```

### Divisão das populações

Os dados serão divididos em duas populações de vestibulandos, entre alunos de escolas públicas e privadas.
Escola Pública:

```python
esc_publica = df_estudo.copy().query("TP_ESCOLA == 'publica'").drop("TP_ESCOLA",
                                                                    axis=1)
esc_publica.shape
```

> (2961, 43)

Escola Privada:

```python
esc_privada = df_estudo.copy().query("TP_ESCOLA == 'privada'").drop("TP_ESCOLA",
                                                                    axis=1)
esc_privada.shape
```

> (478, 43)

# Descrição dos Dados
## Frequências absoluta, percentual e percentual relativa
Frequências absoluta, percentual e percentual relativa da faixa etária de idades.

Escolas Públicas:

```python
dados_abs_pub = esc_publica.FAIXA_ETARIA.value_counts()
abs_pub = pd.DataFrame(dados_abs_pub).rename(columns={"FAIXA_ETARIA": "ABSOLUTA"})
```

```python
dados_rel_pub = round(dados_abs_pub / dados_abs_pub.sum(), 4)
rel_pub = pd.DataFrame(dados_rel_pub).rename(columns={"FAIXA_ETARIA": "RELATIVA"})
```

```python
data_perc_pub = round(dados_rel_pub * 100, 4)
perc_pub = pd.DataFrame(data_perc_pub).rename(columns={"FAIXA_ETARIA": "PERC_RELATIVA"})
```

```python
df_freq_pub = pd.concat([abs_pub, rel_pub, perc_pub], axis=1)
df_freq_pub
```

| --- | ABSOLUTA | RELATIVA | PERCENTUAL_RELATIVA |
| --- | --- | --- | --- |
| 18 anos |	1446 |	0.4883 | 48.83 |
| 17 anos |	1020 |	0.3445 |	34.45 |
| 19 anos |	306 |	0.1033 |	10.33 |
| 20 anos |	76 |	0.0257 |	2.57 |
| Menor de 17 anos | 59 |	0.0199 |	1.99 |
| 21 anos |	19 | 0.0064 |	0.64 |
| 22 anos |	9 |	0.0030 |	0.30 |
| Entre 31 e 35 anos |	6 |	0.0020 |	0.20 |
| 23 anos |	5 |	0.0017 |	0.17 |
| 24 anos |	4 |	0.0014 |	0.14 |
| Entre 26 e 30 anos |	4 |	0.0014 |	0.14 |
| 25 anos |	3 |	0.0010 |	0.10 |
| Entre 36 e 40 anos |	3 |	0.0010 |	0.10 |
| Entre 51 e 55 anos |	1 |	0.0003 |	0.03 |

Percebemos que a parte predominante dos vestibulandos de escolas públicas encontra-se na faixa etária de 17 a 19. Também é possível perceber valores diversos para as faixas etárias.

Escolas Privadas:

```python
dados_abs_priv = esc_privada.FAIXA_ETARIA.value_counts()
abs_priv = pd.DataFrame(dados_abs_priv).rename(columns={"FAIXA_ETARIA": "ABSOLUTA"})
```

```python
dados_rel_priv = round(dados_abs_priv / dados_abs_priv.sum(), 4)
rel_priv = pd.DataFrame(dados_rel_priv).rename(columns={"FAIXA_ETARIA": "RELATIVA"})
```

```python
dados_perc_priv = round(dados_rel_priv * 100, 4)
perc_priv = pd.DataFrame(dados_perc_priv).rename(columns={"FAIXA_ETARIA": "PERCENTUAL_RELATIVA"})
```

```python
df_freq_priv = pd.concat([abs_priv, rel_priv, perc_priv], axis=1)
df_freq_priv
```

| --- | ABSOLUTA | RELATIVA | PERCENTUAL_RELATIVA |
| --- |  --- | --- | --- |
| 17 anos | 306 | 0.6402 | 64.02 |
| 18 anos | 140 | 0.2929 | 29.29 |
| Menor de 17 anos | 24 | 0.0502 | 5.02 |
| 19 anos | 7 | 0.0146 | 1.46 |
| 20 anos | 1 | 0.0021 | 0.21 |

Para as escolas privadas, idades entre 17 e 18 anos predominam, muito dentro do que se encontra para idade do ensino médio regular.
Além disso, no escopo do conjunto de dados, encontram-se categorias resumidas, em relação aos dados das escolas públicas.

### Visualização de frequências

```python
import plotly.express as px
```

```python
tema = px.colors.qualitative.Light24
```

Notas:  
Frequência de notas finais do enem, em relação ao percentual, em que as mesmas aparecem, separadas pelo tipo da escola.

```python
graf_notas = px.histogram(df_estudo, x="NOTA_FINAL", width=900, height=500,
                               marginal="rug", histnorm="percent",
                               barmode="group", color="TP_ESCOLA",
                               color_discrete_sequence=tema)

graf_notas.update_layout(font_size=12, xaxis=dict(title="Nota final"),
                              yaxis=dict(title="Percentual"),
                              title=dict(text="Distribuição de notas", x=0.5,
                                         font_size=22),
                              legend=dict(title="Escola", borderwidth=1,
                                          bordercolor="lightgrey",
                                          bgcolor="rgb(251, 251, 251)"),
                              plot_bgcolor="rgb(250, 250, 250)", bargap=0)
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_freq_notas.png)

Percebemos que as notas das escolas públicas estão distribuidas assimétricamente à direita, enquanto que, as de escolas particulares, estão melhor distribuídas. Assim, para as escolas públicas, quando o valor da nota aumenta, o número de ocorrências diminui.

Faixas Etárias:  
Frequência de faixas etárias dos vestibulandos que fizeram a prova do ENEM 2021.

```python
fx_eta_pub = px.bar(df_freq_pub, x="ABSOLUTA", width=900, text_auto=True,
                    color_discrete_sequence=tema)

fx_eta_pub.update_layout(font_size=12,
                         xaxis=dict(title="Quantidade de Vestibulandos"),
                         yaxis=dict(title="Faixa Etária"),
                         title=dict(text="Faixa Etária - Escola Pública",
                                    x=0.5, font_size=22),
                         plot_bgcolor="rgb(250, 250, 250)")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/fx_eta_pub.png)

```python
fx_eta_priv = px.bar(df_freq_priv, x="ABSOLUTA", width=900, text_auto=True,
                     color_discrete_sequence=[tema[1]])

fx_eta_priv.update_layout(font_size=14,
                          xaxis=dict(title="Quantidade de Vestibulandos"),
                          yaxis=dict(title="Faixa Etária"),
                          title=dict(text="Faixas Etárias - Escola Privada",
                                     x=0.5, font_size=22),
                          plot_bgcolor="rgb(250, 250, 250)")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/fx_eta_priv.png)

A variabilidade de participantes vestibulandos em diferentes faixa etárias de escolas públicas é maior, em relação às escolas privadas. Além disso, tanto para escolas públicas, quanto para privadas, a maior ocorrência foram de alunos entre 18 e 17 anos.

## Medidas de Tendência Central  
Média, moda e mediana das notas de escolas públicas e privadas.

Média:  

```python
med_pub = round(esc_publica.NOTA_FINAL.mean(), 2)
med_priv = round(esc_privada["NOTA_FINAL"].mean(), 2)
```

Moda:  

```python
mod_pub = round(esc_publica.NOTA_FINAL.mode(), 2).values
mod_priv = round(esc_privada["NOTA_FINAL"].mode(), 2).values
```

Mediana:  

```python
medn_pub = round(esc_publica.NOTA_FINAL.median(), 2)
medn_priv = round(esc_privada["NOTA_FINAL"].median(), 2)
```

```python
dados_mtc = {"MEDIA": [med_pub, med_priv],
             "MODA": [mod_pub, mod_priv],
             "MEDIANA": [medn_pub, medn_priv]}
```

```python
df_mtc = pd.DataFrame(dados_mtc, index=["ESCOLA_PUBLICA",
                                        "ESCOLA_PRIVADA"])
df_mtc
```

| --- | MEDIA | MODA | MEDIANA |
| --- |  --- | --- | --- |
| ESCOLA_PUBLICA | 488.31 | [447.04, 501.3, 533.06] | 479.70 |
| ESCOLA_PRIVADA | 576.67 | [470.92, 528.24, 663.78] | 572.73 |

```python
round((mean_priv / mean_pub) * 100, 2)
```

> 118.1

A partir da tabela, podemos concluir que a média das notas finais das escolas privadas é 118,1% maior, em relação as das escolas públicas.  
É possível notar também que, ambos os tipos de escolas apresentaram 3 modas cada.

## Medidas de dispersão ou variação
Será verificado o grau de variação das notas finais com relação a média.

Amplitude:

```python
ampt_pub = esc_publica.NOTA_FINAL.max() - esc_publica["NOTA_FINAL"].min()
ampt_priv = esc_privada["NOTA_FINAL"].max() - esc_privada.NOTA_FINAL.min()
```

Desvio Padrão:

```python
dp_pub = round(esc_publica.NOTA_FINAL.std(), 2)
dp_priv = round(esc_privada.NOTA_FINAL.std(), 2)
```

Variância:

```python
var_pub = round(esc_publica.NOTA_FINAL.var(ddof=0), 2)
var_priv = round(esc_privada.NOTA_FINAL.var(ddof=0), 2)
```

Desvio Absoluto Médio:

```python
dam_pub = round(esc_publica.NOTA_FINAL.mad(), 2)
dam_priv = round(esc_privada.NOTA_FINAL.mad(), 2)
```

```python
data_disp_var = {"AMPLITUDE": [ampt_pub, ampt_priv],
                 "DESVIO_PADRAO": [dp_pub, dp_priv],
                 "VARIANCIA": [var_pub, var_priv],
                 "DESVIO_ABS_MEDIO": [mad_pub, mad_priv]}
```

```python
df_disp_var = pd.DataFrame(data_disp_var, index=["ESCOLA_PUBLICA",
                                                 "ESCOLA_PRIVADA"])
df_disp_var
```

| --- | AMPLITUDE | DESVIO_PADRAO | VARIANCIA | DESVIO_ABS_MEDIO |
| --- |  --- | --- | --- | --- |
| ESCOLA_PUBLICA | 452.0 | 61.02 | 3722.66 | 48.43 |
| ESCOLA_PRIVADA | 377.9 | 80.59 | 6481.31 | 65.79 |

A amplitude revela que as notas das escolas públicas estão mais próximas uma das outras, em relação as das privadas.
É possível perceber que o desvio padrão das escolas privadas é maior, indicando dados que os dados estão melhor distribuídos, se comprado aos das escolas públicas. Essa informação é enfatizada ao olhar para variância dos dados.

## Medidas de Posição
Com as medidas de posição, é possível descrever a tendência da concentração dos valores observados no dataframe.


Fractis:

```python
q1_priv = esc_privada.NOTA_FINAL.quantile(q=0.25)
q2_priv = esc_privada.NOTA_FINAL.median()
q3_priv = esc_privada.NOTA_FINAL.quantile(q=0.75)
q4_priv = esc_privada.NOTA_FINAL.max()
```

```python
q1_pub = esc_publica.NOTA_FINAL.quantile(q=0.25)
q2_pub = esc_publica.NOTA_FINAL.quantile(q=0.5)
q3_pub = esc_publica.NOTA_FINAL.quantile(q=0.75)
q4_pub = esc_publica.NOTA_FINAL.quantile(q=1)
```

```python
iqr_pub = q3_pub - q1_pub
iqr_priv = q3_priv - q1_priv
```

```python
dados_med_pos = {"Q1": [q1_pub, q1_priv],
                 "Q2": [q2_pub, q2_priv],
                 "Q3": [q3_pub, q3_priv],
                 "Q4": [q4_pub, q4_priv],
                 "IQR": [iqr_pub, iqr_priv]}
```

```python
df_med_pos = pd.DataFrame(dados_med_pos, index=["ESCOLA_PUBLICA",
                                                "ESCOLA_PRIVADA"])
df_med_pos
```

| --- | Q1 | Q2 | Q3 | Q4 | IQR |
| --- | --- | --- | --- | --- | --- |
| ESCOLA_PUBLICA | 443.60 | 479.70 | 524.700 | 778.14 | 81.100 |
| ESCOLA_PRIVADA | 520.06 | 572.73 | 636.495 | 775.64 | 116.435 |

### Outliers

```python
boxplot_notas = px.box(df_estudo, y="NOTA_FINAL", width=500, notched=True,
                       color="TP_ESCOLA", color_discrete_sequence=tema)

boxplot_notas.update_layout(font_size=12, yaxis=dict(title="Nota Final"),
                            title=dict(text="Comparação de Notas", x=0.5,
                                       font_size=22),
                            legend=dict(title="Escola", borderwidth=1,
                                        bordercolor="lightgrey",
                                        bgcolor="rgb(251, 251, 251)"),
                            plot_bgcolor="rgb(250, 250, 250)")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/outliers_notas.png)

Há diversas ocorrências de dados discrepantes para as escolas públicas, enquanto que, para escolas privadas, o mesmo não acontece. Com isso, subentende-se que, as notas das escolas privadas encontram consistência maior entre si. Além disso, é possível notar uma melhor distribuição das notas das escolas privadas.

## Comparação Entre os Questionários dos Alunos de Escolas Públicas e Privadas
Para esse módulo, será criado um novo dataframe, apenas com as variáveis a serem visualizadas.

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
```

```python
df_plot = df_estudo.copy()[["TP_ESCOLA", "Q001", "Q002", "Q003", "Q004", "Q005",
                            "Q006", "Q007", "Q008", "Q009", "Q010", "Q011",
                            "Q012", "Q013", "Q014", "Q015", "Q016", "Q017",
                            "Q018", "Q019", "Q020", "Q021", "Q022", "Q023",
                            "Q024", "Q025"]]
df_plot.head()
```
### Substituição dos valores nos registros  
Será feito uma substituição dos valores das linhas (registros), para que se facilite a compreensão dos mesmos.

```python
df_plot.Q001 = df_plot.Q001.replace(
    {"A": "Nunca estudou",
     "B": "Não completou a 4ª série/5º ano do Ensino Fundamental",
     "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental",
     "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio",
     "E": "Completou o Ensino Médio, mas não completou a Faculdade",
     "F": "Completou a Faculdade, mas não completou a Pós-graduação",
     "G": "Completou a Pós-graduação",
     "H": "Não sei"})
```

```python
df_plot.Q002 = df_plot.Q002.replace(
   {"A": "Nunca estudou",
     "B": "Não completou a 4ª série/5º ano do Ensino Fundamental",
     "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental",
     "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio",
     "E": "Completou o Ensino Médio, mas não completou a Faculdade",
     "F": "Completou a Faculdade, mas não completou a Pós-graduação",
     "G": "Completou a Pós-graduação",
     "H": "Não sei"})
```

```python
df_plot.Q006 = df_plot.Q006.replace(
   {"A":	"Nenhuma Renda",
   "B": "Até R$ 1.100,00",
    "C":	"De R$ 1.100,01 até R$ 1.650,00",
    "D":	"De R$ 1.650,01 até R$ 2.200,00",
    "E":	"De R$ 2.200,01 até R$ 2.750,00",
    "F":	"De R$ 2.750,01 até R$ 3.300,00",
    "G":	"De R$ 3.300,01 até R$ 4.400,00",
    "H":	"De R$ 4.400,01 até R$ 5.500,00",
    "I":	"De R$ 5.500,01 até R$ 6.600,00",
    "J":	"De R$ 6.600,01 até R$ 7.700,00",
    "K":	"De R$ 7.700,01 até R$ 8.800,00",
    "L":	"De R$ 8.800,01 até R$ 9.900,00",
    "M":	"De R$ 9.900,01 até R$ 11.000,00",
    "N":	"De R$ 11.000,01 até R$ 13.200,00",
    "O":	"De R$ 13.200,01 até R$ 16.500,00",
    "P":	"De R$ 16.500,01 até R$ 22.000,00",
    "Q":	"Acima de R$ 22.000,00"})
```

```python
df_plot.Q008 = df_plot.Q008.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q009 = df_plot.Q009.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q012 = df_plot.Q012.replace(
   {"A":	"Não",
   "B":	"Sim, uma",
   "C":	"Sim, duas",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q014 = df_plot.Q014.replace(
   {"A":	"Não",
   "B":	"Sim, uma",
   "C":	"Sim, duas",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q019 = df_plot.Q019.replace(
   {"A":	"Não",
   "B":	"Sim, uma",
   "C":	"Sim, duas",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q022 = df_plot.Q022.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q024 = df_plot.Q024.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})
```

```python
df_plot.Q025 = df_plot.Q025.replace(
   {"A":	"Não",
   "B":	"Sim"})
```

```python
df_plot.head()
```

```python
quest = {"Q001": "Até que série seu pai, ou o homem responsável por você, estudou?",
         "Q002": "Até que série sua mãe, ou a mulher responsável por você, estudou?",
         "Q005": "Incluindo você, quantas pessoas moram atualmente em sua residência?",
         "Q006": "Qual é a renda mensal de sua família? (Some a sua renda com a dos seus familiares.)",
         "Q008": "Na sua residência tem banheiro?",
         "Q009": "Na sua residência tem quartos para dormir?",
         "Q012": "Na sua residência tem geladeira?",
         "Q014": "Na sua residência tem máquina de lavar roupa? (o tanquinho NÃO deve ser considerado)",
         "Q019": "Na sua residência tem televisão em cores?",
         "Q022": "Na sua residência tem telefone celular?",
         "Q024": "Na sua residência tem computador?",
         "Q025": "Na sua residência tem acesso à Internet?"}
```

### Visualização gráfica  
Agora, serão expostas comparações entre as respostas dos questionários entre vestibulandos de escolas públicas e privadas.

```python
titles = ["Escolas Públicas", "Escolas Privadas"]
specs = [[{'type':'domain'}, {'type':'domain'}]]
```

```python
q001_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q001"].value_counts()
label_pub = q001_pub.index
value_pub = q001_pub.values

q001_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q001"].value_counts()
label_priv = q001_priv.index
value_priv = q001_priv.values

graph_q001 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q001.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q001.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q001.update_layout(font_size=12, title=dict(text=quest["Q001"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```
![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q001.png)

Para ambos os tipos de escolas, o que predomina são pais que completaram o ensino médio, mas não a faculdade. Os dados começam a ficar discrepantes quando se compara os que completaram a faculdade e a pós graduação, por exemplo.

```python
q002_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q002"].value_counts()
label_pub = q002_pub.index
value_pub = q002_pub.values

q002_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q002"].value_counts()
label_priv = q002_priv.index
value_priv = q002_priv.values

graph_q002 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q002.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q002.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q002.update_layout(font_size=12, title=dict(text=quest["Q002"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q002.png)

Já para as mães, a maior concentração está na faixa dos 40%, porém, com valores contrastantes. As de escolas públicas, completaram apenas o ensino médio, enquanto que as de escolas privadas, completaram a pós graduação. Mesmo as mães de alunos de escolas privadas que não completaram a pós-graduação, completaram ao menos a faculdade, ocupando 31% dos dados.

```python
q005_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q005"].value_counts()
label_pub = q005_pub.index
value_pub = q005_pub.values

q005_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q005"].value_counts()
label_priv = q005_priv.index
value_priv = q005_priv.values

graph_q005 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q005.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q005.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q005.update_layout(font_size=12, title=dict(text=quest["Q005"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q005.png)

Para ambos, a maioria reside em residências com total de habitantes entre 3 e 6 pessoas.

```python
q006_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q006"].value_counts()
label_pub = q006_pub.index
value_pub = q006_pub.values

q006_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q006"].value_counts()
label_priv = q006_priv.index
value_priv = q006_priv.values

graph_q006 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q006.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q006.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q006.update_layout(font_size=12, title=dict(text=quest["Q006"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q006.png)

A renda mensal familiar dos vestibulandos de escolas privadas está distribuída entre valores de R\$1100,00 até R\$13200,00. O mesmo não acontece em relação aos vestibulandos de escolas públicas, onde a maior concentração mensal gira em torno de R\$1100,00, porém, encontramos ainda 7,36% dos vestibulandos de escolas públicas com nenhuma renda familiar.

```python
q008_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q008"].value_counts()
label_pub = q008_pub.index
value_pub = q008_pub.values

q008_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q008"].value_counts()
label_priv = q008_priv.index
value_priv = q008_priv.values

graph_q008 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q008.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q008.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q008.update_layout(font_size=12, title=dict(text=quest["Q008"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q008.png)

Ainda que poucos, vemos ainda vestibulandos de escolas públicas que residem em locais com nenhum banheiro.

```python
q009_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q009"].value_counts()
label_pub = q009_pub.index
value_pub = q009_pub.values

q009_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q009"].value_counts()
label_priv = q009_priv.index
value_priv = q009_priv.values

graph_q009 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q009.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q009.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q009.update_layout(font_size=12, title=dict(text=quest["Q009"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q009.png)

É possível encontrar ainda residências de vestibulandos de escolas públicas com nenhum quarto.

```python
q012_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q012"].value_counts()
label_pub = q012_pub.index
value_pub = q012_pub.values

q012_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q012"].value_counts()
label_priv = q012_priv.index
value_priv = q012_priv.values

graph_q012 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q012.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q012.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q012.update_layout(font_size=12, title=dict(text=quest["Q012"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q012.png)

Para ambos, a predominância percentual de vestibulandos possui ao menos uma geladeira em sua residência. Ainda assim, um número relativamente grande (4,39%) dos vestibulandos de escolas públicas não possuem nenhuma.

```python
q014_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q014"].value_counts()
label_pub = q014_pub.index
value_pub = q014_pub.values

q014_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q014"].value_counts()
label_priv = q014_priv.index
value_priv = q014_priv.values

graph_q014 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q014.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q014.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q014.update_layout(font_size=12, title=dict(text=quest["Q014"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q014.png)

```python
q019_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q019"].value_counts()
label_pub = q019_pub.index
value_pub = q019_pub.values

q019_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q019"].value_counts()
label_priv = q019_priv.index
value_priv = q019_priv.values

graph_q019 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q019.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q019.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q019.update_layout(font_size=12, title=dict(text=quest["Q019"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q019.png)

```python
q022_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q022"].value_counts()
label_pub = q022_pub.index
value_pub = q022_pub.values

q022_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q022"].value_counts()
label_priv = q022_priv.index
value_priv = q022_priv.values

graph_q022 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q022.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q022.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q022.update_layout(font_size=12, title=dict(text=quest["Q022"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q022.png)

Se observarmos os dados de pessoas por residência de escolas privadas, percebe-se que em 37,7% moram 4 pessoas, olhando para o número de aparelhos celulares por residência, temos um percentual de 46,7% das residências com 4 aparelhos. Contudo, na maioria das residências de vestibulandos de escolas públicas também residem 4 pessoas, porém, não se conta com mesma proporção de celulares por residente.

```python
q024_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q024"].value_counts()
label_pub = q024_pub.index
value_pub = q024_pub.values

q024_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q024"].value_counts()
label_priv = q024_priv.index
value_priv = q024_priv.values

graph_q024 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q024.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q024.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q024.update_layout(font_size=12, title=dict(text=quest["Q024"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q024.png)

Um item essencial para um vestibulando não está presente para 64,7% das residências de vestibulandos de escolas públicas. Enquanto que, para os de escolas privadas, 85,6% das residências possuem ao menos um aparelho.

```python
q025_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q025"].value_counts()
label_pub = q025_pub.index
value_pub = q025_pub.values

q025_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q025"].value_counts()
label_priv = q025_priv.index
value_priv = q025_priv.values

graph_q025 = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=titles)

graph_q025.add_trace(go.Pie(labels=label_pub, values=value_pub,
                            marker_colors=tema), 1, 1)

graph_q025.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q025.update_layout(font_size=12, title=dict(text=quest["Q025"], x=0.5,
                                                  font_size=22),
                         uniformtext_minsize=14, uniformtext_mode="hide")
```

![](https://github.com/pyrataria/data_analytics/blob/main/enem_2021_ap/resources/images/graph_q025.png)