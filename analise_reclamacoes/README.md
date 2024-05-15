**SOBRE O CONJUNTO**  
Este conjunto de dados apresenta uma lista de reclamações de consumidores apresentadas contra seguradoras licenciadas em Connecticut (Estado dos EUA). O mesmo inclui a empresa, linha de negócios, natureza da reclamação, resultado ou resolução e recuperação.  

**PROJETO**  
Este projeto sob a perspectiva de estatística descritiva e probabilística, demonstrar de forma prática e visual, dados acerca do dataset [Insurance Company Complaints](https://www.kaggle.com/datasets/adelanseur/insurance-company-complaints). Ao final, serão respondidas algumas perguntas de negócio, acerca das questões levantadas.

<u>VARIÁVEIS</u>:  
**Company**: nome da seguradora envolvida na reclamação.  
**Opened**: data em que a reclamação foi aberta ou recebida.  
**Closed**: data em que a reclamação foi resolvida e oficialmente encerrada.  
**Coverage**: tipo de cobertura de seguro relacionada à reclamação (por exemplo, seguro de automóvel, seguro de saúde, etc.).  
**SubCoverage**: maiores detalhes ou subcategoria da cobertura do seguro.  
**Reason**: principal motivo ou causa da reclamação.  
**SubReason**: maiores detalhes ou subcategoria do motivo da reclamação.     
**Recovery**: quantia de dinheiro recuperada (se aplicável), como resultado da resolução da reclamação.  
**Status** : status atual da reclamação (por exemplo, aberta, fechada, em andamento, etc.).  

# PREPARAÇÃO, ORGANIZAÇÃO E ESTRUTURAÇÃO DOS DADOS

## Extração e Limpeza de Dados

```python
import pandas as pd
```

```python
df = pd.read_csv("/content/drive/MyDrive/programacao/datasets/reclamacoes_seguradoras/iccrsr.csv")
df.head()
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/img00.png)

Primeiramente, será verificado a quantidade de variáveis e registros contidos no dataset.

```python
df.shape
```
>(38267, 12)

Também é importante verificar o tipo dos dados.

```python
df.dtypes
```

> Company         object  
> File No.         int64  
> Opened          object  
> Closed          object  
> Coverage        object  
> SubCoverage     object  
> Reason          object  
> SubReason       object  
> Disposition     object  
> Conclusion      object  
> Recovery       float64  
> Status          object  
> dtype: object

As variáveis Opened e Closed devem ser modificadas para o tipo *datetime*.

```python
df["Opened"] = pd.to_datetime(df["Opened"])
df["Closed"] = pd.to_datetime(df["Closed"])
```

<u>Remoção de variáveis e registros</u>  
Para a remoção de dados, primeiramente, será verificado valores nulos.

```python
df.isnull().sum()
```
> Company            0  
> File No.           0  
> Opened             0  
> Closed           963  
> Coverage        2440  
> SubCoverage     8960  
> Reason          2617  
> SubReason       2617  
> Disposition    15288  
> Conclusion     17094  
> Recovery           0  
> Status             0  
> dtype: int64

Há variáveis com valores nulos, porém, apenas algumas são de suma importância para o projeto e, estas devem ser removidas.
Como não será feito nenhum processo de machine learning, não é interessante manter valores nulos acerca da variável Opened.

```python
df.dropna(subset=["Closed"], inplace=True)
```

```python
df.shape
```
> (37304, 12)

```python
df.reset_index(drop=True, inplace=True)
```

# ESTATÍSTICA DESCRITIVA

## Distribuição de Frequências
É interessante começar verificando a exclusividade dos dados.

```python
df.nunique()
```
> Company          755  
> File No.       20029  
> Opened          1593  
> Closed          1377  
> Coverage          53  
> SubCoverage      101  
> Reason             4  
> SubReason        177  
> Disposition       13  
> Conclusion        52  
> Recovery        2742  
> Status             9  
> dtype: int64

Olhando para a exclusividade em cada variável, é possível ter um ponto de partida para a descrição dos dados.  
### Seguradora x Reclamações
O dataset gira em torno de reclamações acerca de seguradoras, portanto, a descrição dos dados iniciará sob as seguradoras com maior número de reclamações.

```python
cols_segs = {"index": "Seguradora", "Company": "Quantidade"}
```

```python
df_segs = df.Company.value_counts()[:10].reset_index().rename(columns=cols_segs)

df_segs
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/img01.png)

A informação obtida desta operação pode ser visualizada para um melhor entendimento. Um gráfico aceitável para tal, que demonstra de forma objetiva o percentual de ocorrências das reclamações.

```python
import plotly.graph_objects as go
import plotly.express as px
```

```python
tema = px.colors.qualitative.Light24
```

```python
labels = df_segs.Seguradora.values
values = df_segs.Quantidade.values
```

```python
graf_segs = go.Figure(go.Pie(labels=labels, values=values, hole=0.25,
                             texttemplate="%{label}<br>%{percent}",
                             marker=dict(colors=tema)))

graf_segs.update_layout(font_size=12, showlegend=False,
                        title=dict(text="SEGURADORA x QUANTIDADE DE RECLAMAÇÃO",
                                   x=0.5, font_size=22),
                        annotations=[dict(text=f"<b>TOTAL<br>{sum(values)}</b>",
                                          x=0.5, y=0.5, font_size=14,
                                          showarrow=False)])
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/graf_segs.png)

Com isso, se observa uma grande discrepância acerca das reclamções. A seguradora *Anthem Health Plans, Inc* possui um percentual elevado de reclamações, se comparado as demais, alcançando cerca de 40,1% dos dados, isso equivale a 6519 dos 16238 registros.  
### Motivo ou causa de reclamação
Outro fator importante a ser entendido é o principal motivo ou causa da reclamação. Esta informação pode ser obtida a partir da variável *Reason*.

```python
cols_recls = {"index": "Reclamação", "Reason": "Quantidade"}
```

```python
df_recls = df.Reason.value_counts().reset_index().rename(columns=cols_recls)

df_recls
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/img02.png)

Os motivos ou causas de reclamação são: Claim Handling (Manuseio de Reclamações), PolicyHolder Service (Atendimento ao Titular da Apólice), Underwriting (Subscrição) e Marketing & Sales (Marketing & Vendas). Dentre elas, a predominante é *Claim Handling*. A visualização desstas frequências pode ser feita, de modo a facilitar o entendimento dos dados, a partir de um gráfico de barras.

```python
graf_reason = px.histogram(df_recls, x="Quantidade", y="Reclamação", width=750,
                           height=400, orientation='h', text_auto=True,
                           color="Reclamação", color_discrete_sequence=tema)

graf_reason.update_layout(font_size=12, showlegend=False,
                          title=dict(text="PRINCIPAIS MOTIVOS OU CAUSAS DE RECLAMAÇÃO",
                                     x=0.5, font_size=22),
                          plot_bgcolor="rgb(250, 250, 250)")

graf_reason.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                         title="Quantidade")

graf_reason.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey",
                         title=None, categoryorder="total descending")
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/graf_reason.png)

Observando a distribuição, fica evidente a discrepância acerca do principal motivo ou causa de reclamação, em relação aos demais. Além disso, é possível se ver as principais sub-reclamações, para se ter um entendimento maior sobre a variável *Reason*, encontrada na variável *SubReason*.  
<u>**Manuseio de Reclamações (Claim Handling)**</u>  
Área responsável por lidar com os processos e procedimentos quando um segurado precisa fazer uma reclamação devido a um evento coberto pela apólice.

```python
df[df.Reason == "Claim Handling"].SubReason.value_counts()[:5]
```
> Claim Denial                       4501  
> Claim Delay                        3837  
> Unsatisfactory Settlement/Offer    3250  
> Claim Procedure                    1701  
> Medical Necessity Denial           1307  
Name: SubReason, dtype: int64

<u>**Atendimento ao Titular da Apólice (PolicyHolder Service)**</u>  
Engloba todos os aspectos de comunicação e assistência fornecidos aos clientes que possuem uma apólice de seguro.

```python
df[df.Reason == "PolicyHolder Service"].SubReason.value_counts()[:5]
```
> Premium Notice/Billing              1012  
> Delays/No Response                   712  
> Unsatisfactory Refund of Premium     432  
> Premium/Notice                       312  
> Premium Refund Delay                 159  
> Name: SubReason, dtype: int64

<u>**Subscrição (Underwriting)**</u>  
Processo pelo qual a seguradora avalia o risco de cobrir um cliente em potencial.

```python
df[df.Reason == "Underwriting"].SubReason.value_counts()[:5]
```
> Premium & Rating         1544  
> Cancellation              669  
> Nonrenewal                496  
> Premium/Rate Increase     288  
> No Subreason              153  
> Name: SubReason, dtype: int64

<u>**Marketing & Vendas (Marketing & Sales)**</u>  
Responsável por promover os produtos e serviços da seguradora, bem como atrair novos clientes.

```python
df[df.Reason == "Marketing & Sales"].SubReason.value_counts()[:5]
```
> High Pressure Tactics          241  
> Misrepresentation              185  
> Misappropriation of Premium    163  
> No Coverage/Premium Paid       144  
> Misleading Advertising          71  
> Name: SubReason, dtype: int64

### Cobertura de seguro x Motivo de reclamação
Através da variável *Coverage*, é determinado o tipo de cobertura de seguro. Com isso, será feita uma análise sobre a mesma, em relação ao motivo ou causa de reclamação.

```python
cob_seg = df.Coverage.value_counts()
```

```python
i_cob_seg = cob_seg[cob_seg > 1000].index
```

```python
df_cob_seg = df[df.Coverage.isin(i_cob_seg)]
```

```python
graf_cob_seg = px.histogram(df_cob_seg, x="Coverage", width=600, height=700,
                            text_auto=True, color="Reason",
                            color_discrete_sequence=tema)

graf_cob_seg.update_layout(font_size=12, showlegend=False,
                           title=dict(text="COBERTURA DE SEGURO x MOTIVO DE RECLAMAÇÃO",
                                      x=0.5, font_size=22),
                           plot_bgcolor="rgb(250, 250, 250)")

graf_cob_seg.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                          title=None, categoryorder="total descending")

graf_cob_seg.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey",
                          title="Quantidade")
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/graf_cob_seg.png)

Com isso, se constata que os tipos de coberturas de seguros mais solicitados, tem como principal motivo ou causa de reclamação a "Claim Handling", com excessão de *Individual Life*, que tem PolicyHolder Service como principal motivo ou causa de reclamação.
### Reclamações por dia
Agora, se discorrerá sobre o número de abertura de reclamações (Opened) por dia. Com isso, será possível entender se houve picos, altas, baixas, a respeito das reclamações.

```python
recs_dia = df.sort_values(by="Opened").Opened.value_counts(sort=False)
```

```python
graf_recs_dia = go.Scatter(x=recs_dia.index, y=recs_dia.values, mode="lines",
                           line=dict(color=tema[0]))

layout_recs = go.Layout(title=dict(text="ABERTURA DE RECLAMAÇÕES POR DIA",
                                   x=0.5, font_size=22),
                        yaxis=dict(title="Reclamação (ões)"), height=600)

fig_recs_dia = go.Figure(data=graf_recs_dia, layout=layout_recs)

fig_recs_dia.update_layout(xaxis_range=["2020", "2023-06"],
                           plot_bgcolor="#F9F9F9")

fig_recs_dia.update_yaxes(showline=True, linewidth=1, linecolor="lightgrey")

fig_recs_dia.update_xaxes(showline=True, linewidth=1, linecolor="lightgrey",
                          rangeslider_visible=True)
```
![](https://github.com/pyrataria/data_analytics/blob/main/analise_reclamacoes/resources/images/fig_recs_dia.png)

Olhando para o gráfico, é possível ver um aumento exponencial a partir de novembro de 2021. Além disso, se nota que, até o dia 31 de outubro de 2017, há poucos registros de reclamações.

# ESTATÍSTICA PROBABILÍSTICA
Aqui, será visto as chances de determinado evento acontecer.

## Perguntas de Negócio
Sob a perspectiva de perguntas de negócio, serão resolvidas algumas questões a partir do conjunto de dados.

**1) Qual a probabilidade de um cliente com o tipo de cobertura de seguro *Individual* ter seu problema resolvido em menos 20 dias?**

```python
prob_a = lambda a, e: round((a / e) * 100, 2)
e1 = df[df.Coverage == "Individual"]
```

```python
a1 = len([i.days for i in e1.Closed - e1.Opened if i.days < 20])
```

```python
print(f"R = Há {prob_a(a1, len(e1))}% de chance do evento ocorrer.")
```
> R = Há 36.56% de chance do evento ocorrer.

**2) Clientes com cobertura do tipo group tem quantos por cento de chance de não ter problemas de *Claim Handling*?**

```python
prob_nao = lambda a, e: round((1 - (a / e)) * 100, 2)
e2 = df[df.Coverage == "Group"]
```

```python
a2 = len(e2[e2.Reason == "Claim Handling"])
```

```python
print(f"R = Há {prob_nao(a2, len(e2))}% de chance do evento não ocorrer.")
```
> R = Há 10.62% de chance do evento não ocorrer.

**3) Houve quantas aberturas de reclamação por dia em média?**

```python
md_dia = int(df.Opened.value_counts().mean())
```

```python
print(f"R = Houve em média {md_dia} aberturas de reclamação por dia.")
```
> R = Houve em média 23 aberturas de reclamação por dia.

**4) Um cliente que possui a cobertura *Homeowners* tem quantos por cento de chance de ter seu caso reaberto (Reopened).**

```python
e4 = df[df.Coverage == "Homeowners"]
```

```python
a4 = len(e4[e4.Status == "Reopened"])
```

```python
print(f"R = Há {prob_a(a4, len(e4))}% de chance do evento ocorrer.")
```
> R = Há 0.03% de chance do evento ocorrer.

**5) Os casos foram resolvidos em média em quantos dias**

```python
dias = [i.days for i in df.Closed - df.Opened]
```

```python
md_casos = int(sum(dias) / len(dias))
```

```python
print(f"R = Demorou em média {md_casos} dias para a resolução dos problemas.")
```
> R = Demorou em média 41 dias para a resolução dos problemas.

**6) Ao optar pelo plano *Individual* da seguradora *Anthem Health Plans, Inc*, qual a chance de se ter um problema de *PolicyHolder Service*?**

```python
e6 = df.query("Company == 'Anthem Health Plans, Inc' and Coverage == 'Individual'")
```

```python
a6 = len(e6[e6.Reason == "PolicyHolder Service"])
```

```python
print(f"R = Há {prob_a(a6, len(e6))}% de chance do evento ocorrer.")
```
> R = Há 13.79% de chance do evento ocorrer.

**7) Qual a probabilidade de se ter problema de *Claim Handling* ou *PolicyHolder Service* ao se contratar o serviço de uma seguradora?**

```python
prob_uniao = lambda pA, pB: pA + pB
e8 = len(df.Reason)
```

```python
pA = prob_a(len(df.query("Reason == 'Claim Handling'")), e8)
pB = prob_a(len(df[df.Reason == "PolicyHolder Service"]), e8)
```

```python
print(f"R = Há {prob_uniao(pA, pB)}% de chance do evento ocorrer.")
```
> R = Há 80.52% de chance do evento ocorrer.

**8) Em geral, qual foi a média de recuperação de valores?**

```python
md_rec = prob_a(len(df[df.Recovery > 0]), len(df))
```

```python
print(f"R = Houve em média {md_rec}% de recuperação de valores.")
```
> R = Houve em média 20.76% de recuperação de valores.