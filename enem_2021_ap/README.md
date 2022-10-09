Estudo estatístico onde serão abordadas algumas variáveis sobre o ENEM 2021 no Estado do Amapá.  
Para esse estudo, será utilizado um dataset pré-tratado, relativo às provas do ENEM, realizadas no Amapá, que por sua vez, foi retirado dos [microdados](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) do ENEM 2021.
### Importando o pandas

```python
import pandas as pd
```

# Preparação, Organização e Estruturação dos Dados

```python
pd.set_option("display.max_columns", 100)
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

## Valores nulos
Verificando valores nulos das principais variáveis do estudo.

```python
df[["NOTA_CN",	"NOTA_CH",	"NOTA_LC",	"NOTA_MT", "NOTA_REDACAO", "TP_ESCOLA",
    "FAIXA_ETARIA", "Q001",	"Q002",	"Q003",	"Q004",	"Q005",
    "Q006",	"Q007",	"Q008",	"Q009",	"Q010",	"Q011",	"Q012",	"Q013",
    "Q014",	"Q015",	"Q016",	"Q017",	"Q018",	"Q019",	"Q020",	"Q021",
    "Q022",	"Q023",	"Q024",	"Q025"]].isnull().sum()
```

> NOTA_CN         0
> NOTA_CH         0
> NOTA_LC         0
> NOTA_MT         0
> NOTA_REDACAO    0
> TP_ESCOLA       0
> FAIXA_ETARIA    0
> Q001            0
> Q002            0
> Q003            0
> Q004            0
> Q005            0
> Q006            0
> Q007            0
> Q008            0
> Q009            0
> Q010            0
> Q011            0
> Q012            0
> Q013            0
> Q014            0
> Q015            0
> Q016            0
> Q017            0
> Q018            0
> Q019            0
> Q020            0
> Q021            0
> Q022            0
> Q023            0
> Q024            0
> Q025            0
> dtype: int64

Não há valores nulos para as principais variáveis em estudo.

# Identificação da População e das Variáveis
A população de estudo será dividida em dois grupos de vestibulandos por tipo de escola:
* públicas
* privadas

```python
df.TP_ESCOLA.value_counts()
```
> nao_respondeu    7581
> publica          2961
> privada           478
> Name: TP_ESCOLA, dtype: int64

```python
esc_invalida = df[df.TP_ESCOLA == "nao_respondeu"].index

df_estudo = df.copy().drop(esc_invalida)

nota_final = ["NOTA_CN", "NOTA_CH",	"NOTA_LC",	"NOTA_MT", "NOTA_REDACAO"]

df_estudo.insert(20, "NOTA_FINAL", df_estudo[nota_final].sum(axis=1) / 5)

df_estudo.FAIXA_ETARIA = df_estudo.FAIXA_ETARIA.replace(
    {1:	"Menor de 17 anos",
    2:	"17 anos",
    3:	"18 anos",
    4:	"19 anos",
    5:	"20 anos",
    6:	"21 anos",
    7:	"22 anos",
    8:	"23 anos",
    9:	"24 anos",
    10:	"25 anos",
    11:	"Entre 26 e 30 anos",
    12:	"Entre 31 e 35 anos",
    13:	"Entre 36 e 40 anos",
    14:	"Entre 41 e 45 anos",
    15:	"Entre 46 e 50 anos",
    16:	"Entre 51 e 55 anos",
    17:	"Entre 56 e 60 anos",
    18:	"Entre 61 e 65 anos",
    19:	"Entre 66 e 70 anos",
    20:	"Maior de 70 anos"}
)

df_estudo.head()

df_estudo.shape
```

> (3439, 53)

```python
df_estudo.TP_ESCOLA.value_counts()
```
> publica    2961
> privada     478
> Name: TP_ESCOLA, dtype: int64


O total de vestibulandos de escolas públicas e privadas é de 3439. Desses, 2961 matriculados em escolas públicas e 478 em escolas privadas.

**Escola Pública:**

```python
esc_publica = df_estudo.copy().query("TP_ESCOLA == 'publica'").drop("TP_ESCOLA", axis=1)

esc_publica.shape
```

> (2961, 52)

**Escola Privada:**

```python
esc_privada = df_estudo.copy().query("TP_ESCOLA == 'privada'").drop("TP_ESCOLA", axis=1)

esc_privada.shape
```

> (478, 52)

# Descrição dos Dados
## Frequências absoluta, percentual e percentual relativa
Frequências absoluta, percentual e percentual relativa da faixa etária de idades.

**Escolas Públicas:**

```python
abs_pub = pd.DataFrame.from_dict(esc_publica.FAIXA_ETARIA.value_counts()).rename(columns={"FAIXA_ETARIA": "ABSOLUTA"})

rel_pub = pd.DataFrame.from_dict(round(abs_pub / abs_pub.sum(), 4)).rename(columns={"ABSOLUTA": "RELATIVA"})

perc_pub = pd.DataFrame.from_dict(round(rel_pub * 100, 4)).rename(columns={"RELATIVA": "PERCENTUAL_RELATIVA"})

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

Percebemos que a maior parte dos valores para as escolas públicas está concetrada entre as faixas de 17 a 20 anos.

**Escolas Privadas:**

```python
abs_priv = pd.DataFrame.from_dict(esc_privada.FAIXA_ETARIA.value_counts()).rename(columns={"FAIXA_ETARIA": "ABSOLUTA"})

rel_priv = pd.DataFrame.from_dict(round(abs_priv / abs_priv.sum(), 4)).rename(columns={"ABSOLUTA": "RELATIVA"})

perc_priv = pd.DataFrame.from_dict(round(rel_priv * 100, 4)).rename(columns={"RELATIVA": "PERCENTUAL_RELATIVA"})

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
Além disso, no escopo do conjunto de dados a maior ocorrência de idades foram de pessoas de até 19 anos.

### Visualização de frequências

```python
import plotly.express as px
```

**Notas:**  
Frequência de notas finais do enem, em relação ao percentual em que as mesmas aparecem, separadas pelo tipo da escola.

```python
graph_freq_notas = px.histogram(df_estudo, x="NOTA_FINAL", height=700,
                                marginal="rug", histnorm="percent",
                                barmode="group", color="TP_ESCOLA")
graph_freq_notas.update_layout(bargap=0)
```

Percebemos que as notas das escolas públicas estão distribuidas assimétricamente à direita, enquanto que, as de escolas particulares, encontram-se mais uniformemente distribuídas. Ou seja, para as escolas públicas, quando o valor da nota aumenta, o número de ocorrências diminui.

**Faixas Etárias:**  
Frequência de faixas etárias dos vestibulandos que fizeram a prova do ENEM 2021.

```python
px.bar(df_freq_pub, x="ABSOLUTA", text_auto=True)

px.bar(df_freq_priv, x="ABSOLUTA", text_auto=True)
```

A variabilidade de participantes vestibulandos em diferentes faixa etárias de escolas públicas é maior, em relação às escolas privadas. Além disso, tanto para escolas públicas, quanto para privadas, a maior ocorrência foram de alunos entre 18 e 17 anos.

## Medidas de Tendência Central  
Média, moda e mediana das notas de escolas públicas e privadas.

**Média:**

```python
mean_pub = round(esc_publica.NOTA_FINAL.mean(), 2)
mean_priv = round(esc_privada["NOTA_FINAL"].mean(), 2)
```

**Moda:**

```python
mod_pub = round(esc_publica.NOTA_FINAL.mode(), 2).values
mod_priv = round(esc_privada["NOTA_FINAL"].mode(), 2).values
```

**Mediana**

```python
medn_pub = round(esc_publica.NOTA_FINAL.median(), 2)
medn_priv = round(esc_privada["NOTA_FINAL"].median(), 2)

data_cent = {
    "MEDIA": [mean_pub, mean_priv],
    "MODA": [mod_pub, mod_priv],
    "MEDIANA": [medn_pub, medn_priv]
}

df_med_cent = pd.DataFrame(data_cent, index=["ESCOLA_PUBLICA", "ESCOLA_PRIVADA"])
df_med_cent
```

| --- | MEDIA | MODA | MEDIANA |
| --- |  --- | --- | --- |
| ESCOLA_PUBLICA | 488.31 | [447.04, 501.3, 533.06] | 479.70 |
| ESCOLA_PRIVADA | 576.67 | [470.92, 528.24, 663.78] | 572.73 |

```python
round((mean_priv / mean_pub) * 100, 2)
```

> 118.1

Com isso, percebemos que as escolas apresentaram 3 modas cada.
A partir da tabela, podemos concluir também que a média das notas finais das escolas privadas é 118,1% maior, em relação as das escolas públicas.

## Medidas de dispersão ou variação
Será verificado o grau de variação das notas finais com relação a média.

**Amplitude:**

```python
ampt_pub = esc_publica.NOTA_FINAL.max() - esc_publica["NOTA_FINAL"].min()
ampt_priv = esc_privada["NOTA_FINAL"].max() - esc_privada.NOTA_FINAL.min()
```

**Desvio Padrão:**

```python
std_pub = round(esc_publica.NOTA_FINAL.std(), 2)
std_priv = round(esc_privada.NOTA_FINAL.std(), 2)
```

**Variância:**

```python
var_pub = round(esc_publica.NOTA_FINAL.var(ddof=0), 2)
var_priv = round(esc_privada.NOTA_FINAL.var(ddof=0), 2)
```

**Desvio Absoluto Médio:**

```python
mad_pub = round(esc_publica.NOTA_FINAL.mad(), 2)
mad_priv = round(esc_privada.NOTA_FINAL.mad(), 2)

data_disp_var = {
    "AMPLITUDE": [ampt_pub, ampt_priv],
    "DESVIO_PADRAO": [std_pub, std_priv],
    "VARIANCIA": [var_pub, var_priv],
    "DESVIO_ABS_MEDIO": [mad_pub, mad_priv]
}

df_disp_var = pd.DataFrame(data_disp_var, index=["ESCOLA_PUBLICA", "ESCOLA_PRIVADA"])
df_disp_var
```

| --- AMPLITUDE| --- | DESVIO_PADRAO | VARIANCIA | DESVIO_ABS_MEDIO |
| --- |  --- | --- | --- |
| --- ESCOLA_PUBLICA| --- | 452.0 | 61.02 | 3722.66 | 48.43 |
| --- ESCOLA_PRIVADA| --- | 377.9 | 80.59 | 6481.31 | 65.79 |

Olhando para o desvio padrão, percebemos que as notas das escolas privadas estão melhores distribuídas em torno da média. Além disso, a variância nos mostra que os dados das escola públicas estão mais condensados ao valor central.

## Medidas de Posição

**Fractis:**

```python
q1_priv = esc_privada.NOTA_FINAL.quantile(q=0.25)
q2_priv = esc_privada.NOTA_FINAL.median()
q3_priv = esc_privada.NOTA_FINAL.quantile(q=0.75)
q4_priv = esc_privada.NOTA_FINAL.max()

q1_pub = esc_publica.NOTA_FINAL.quantile(q=0.25)
q2_pub = esc_publica.NOTA_FINAL.quantile(q=0.5)
q3_pub = esc_publica.NOTA_FINAL.quantile(q=0.75)
q4_pub = esc_publica.NOTA_FINAL.quantile(q=1)

iqr_pub = q3_pub - q1_pub
iqr_priv = q3_priv - q1_priv

data_med_pos = {
    "Q1": [q1_pub, q1_priv],
    "Q2": [q2_pub, q2_priv],
    "Q3": [q3_pub, q3_priv],
    "Q4": [q4_pub, q4_priv],
    "IQR": [iqr_pub, iqr_priv]
}

df_med_pos = pd.DataFrame(data_med_pos, index=["ESCOLA_PUBLICA", "ESCOLA_PRIVADA"])
df_med_pos
```
| Q1 | Q2 | Q3 | Q4 | IQR |
| --- | --- | --- | --- |
| ESCOLA_PUBLICA | 443.60 | 479.70 | 524.700 | 778.14 | 81.100 |
| ESCOLA_PRIVADA | 520.06 | 572.73 | 636.495 | 775.64 | 116.435 |

### Outliers

```python
px.box(data_frame=df_estudo, y="NOTA_FINAL", width=500, height=600,
       color="TP_ESCOLA")
```

Há diversas ocorrências de dados discrepantes para as escolas públicas, enquanto que, para escolas privadas, o mesmo não acontece. Com isso, subentende-se que, as notas das escolas privadas encontram certa consistência entre si.

## Comparação Entre os Questionários dos Alunos de Escolas Públicas e Privadas

Para esse módulo, será criado um novo dataset, apenas com as variáveis a serem visualizadas.

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_plot = df_estudo.copy()[["TP_ESCOLA", "Q001", "Q002", "Q003", "Q004", "Q005",
                            "Q006", "Q007", "Q008", "Q009", "Q010", "Q011",
                            "Q012", "Q013", "Q014", "Q015", "Q016", "Q017",
                            "Q018", "Q019", "Q020", "Q021", "Q022", "Q023",
                            "Q024", "Q025"]]
df_plot.head()
```
#### Fazendo substituição dos valores nos registros.

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

df_plot.Q002 = df_plot.Q002.replace(
   {"A": "Nunca estudou",
     "B": "Não completou a 4ª série/5º ano do Ensino Fundamental",
     "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental",
     "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio",
     "E": "Completou o Ensino Médio, mas não completou a Faculdade",
     "F": "Completou a Faculdade, mas não completou a Pós-graduação",
     "G": "Completou a Pós-graduação",
     "H": "Não sei"})

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

df_plot.Q008 = df_plot.Q008.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q009 = df_plot.Q009.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q012 = df_plot.Q012.replace(
   {"A":	"Não",
   "B":	"Sim, uma",
   "C":	"Sim, duas",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q014 = df_plot.Q014.replace(
   {"A":	"Não",
   "B":	"Sim, uma",
   "C":	"Sim, duas",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q019 = df_plot.Q019.replace(
   {"A":	"Não",
   "B":	"Sim, uma",
   "C":	"Sim, duas",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q022 = df_plot.Q022.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q024 = df_plot.Q024.replace(
   {"A":	"Não",
   "B":	"Sim, um",
   "C":	"Sim, dois",
   "D":	"Sim, três",
   "E":	"Sim, quatro ou mais"})

df_plot.Q025 = df_plot.Q025.replace(
   {"A":	"Não",
   "B":	"Sim"})

df_plot.head()

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

Visualização gráfica entre questionários dos alunos de escolas públicas e privadas.

```python
q001_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q001"].value_counts()
label_pub = q001_pub.index
value_pub = q001_pub.values

q001_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q001"].value_counts()
label_priv = q001_priv.index
value_priv = q001_priv.values

graph_q001 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q001.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q001.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q001.update_layout(title_text=quest["Q001"])
graph_q001.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q002_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q002"].value_counts()
label_pub = q002_pub.index
value_pub = q002_pub.values

q002_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q002"].value_counts()
label_priv = q002_priv.index
value_priv = q002_priv.values

graph_q002 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q002.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q002.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q002.update_layout(title_text=quest["Q002"])
graph_q002.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q005_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q005"].value_counts()
label_pub = q005_pub.index
value_pub = q005_pub.values

q005_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q005"].value_counts()
label_priv = q005_priv.index
value_priv = q005_priv.values

graph_q005 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q005.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q005.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q005.update_layout(title_text=quest["Q005"])
graph_q005.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q006_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q006"].value_counts()
label_pub = q006_pub.index
value_pub = q006_pub.values

q006_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q006"].value_counts()
label_priv = q006_priv.index
value_priv = q006_priv.values

graph_q006 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q006.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q006.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q006.update_layout(title_text=quest["Q006"])
graph_q006.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q008_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q008"].value_counts()
label_pub = q008_pub.index
value_pub = q008_pub.values

q008_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q008"].value_counts()
label_priv = q008_priv.index
value_priv = q008_priv.values

graph_q008 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q008.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q008.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q008.update_layout(title_text=quest["Q008"])
graph_q008.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q009_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q009"].value_counts()
label_pub = q009_pub.index
value_pub = q009_pub.values

q009_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q009"].value_counts()
label_priv = q009_priv.index
value_priv = q009_priv.values

graph_q009 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q009.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q009.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q009.update_layout(title_text=quest["Q009"])
graph_q009.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q012_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q012"].value_counts()
label_pub = q012_pub.index
value_pub = q012_pub.values

q012_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q012"].value_counts()
label_priv = q012_priv.index
value_priv = q012_priv.values

graph_q012 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q012.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q012.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q012.update_layout(title_text=quest["Q012"])
graph_q012.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q014_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q014"].value_counts()
label_pub = q014_pub.index
value_pub = q014_pub.values

q014_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q014"].value_counts()
label_priv = q014_priv.index
value_priv = q014_priv.values

graph_q014 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q014.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q014.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q014.update_layout(title_text=quest["Q014"])
graph_q014.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q019_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q019"].value_counts()
label_pub = q019_pub.index
value_pub = q019_pub.values

q019_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q019"].value_counts()
label_priv = q019_priv.index
value_priv = q019_priv.values

graph_q019 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q019.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q019.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q019.update_layout(title_text=quest["Q019"])
graph_q019.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q022_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q022"].value_counts()
label_pub = q022_pub.index
value_pub = q022_pub.values

q022_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q022"].value_counts()
label_priv = q022_priv.index
value_priv = q022_priv.values

graph_q022 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q022.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q022.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q022.update_layout(title_text=quest["Q022"])
graph_q022.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q024_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q024"].value_counts()
label_pub = q024_pub.index
value_pub = q024_pub.values

q024_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q024"].value_counts()
label_priv = q024_priv.index
value_priv = q024_priv.values

graph_q024 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q024.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q024.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q024.update_layout(title_text=quest["Q024"])
graph_q024.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')

q025_pub = df_plot.query("TP_ESCOLA == 'publica'")["Q025"].value_counts()
label_pub = q025_pub.index
value_pub = q025_pub.values

q025_priv = df_plot.query("TP_ESCOLA == 'privada'")["Q025"].value_counts()
label_priv = q025_priv.index
value_priv = q025_priv.values

graph_q025 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'},
                                          {'type':'domain'}]],
                  subplot_titles=["Escolas Públicas", "Escolas Privadas"])

graph_q025.add_trace(go.Pie(labels=label_pub, values=value_pub), 1, 1)
graph_q025.add_trace(go.Pie(labels=label_priv, values=value_priv), 1, 2)

graph_q025.update_layout(title_text=quest["Q025"])
graph_q025.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
```
