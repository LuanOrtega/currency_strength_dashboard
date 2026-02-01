# 💱 Currency Strength Dashboard

Dashboard interativo desenvolvido em **Python + Streamlit** para análise
de **força relativa de moedas**, utilizando dados de câmbio em tempo
quase real.

O projeto consome uma API pública de câmbio, calcula a força de cada
moeda com base em uma moeda de referência (USD) e apresenta os
resultados de forma visual, clara e dinâmica.

------------------------------------------------------------------------

## 🚀 Funcionalidades

-   📊 Tabela de força das moedas com cores dinâmicas\
-   📈 Gráfico de barras interativo com Altair\
-   🎨 Escala de cores baseada na força (vermelho → amarelo → verde)\
-   🔄 Atualização automática a cada 30 segundos\
-   ⚡ Cache inteligente para evitar chamadas excessivas à API\
-   🧮 Cálculo normalizado de força relativa (0--100)\
-   🕒 Exibição do horário da última atualização e da última chamada à
    API

------------------------------------------------------------------------

## 🪙 Moedas analisadas

-   GBP --- Libra Esterlina\
-   CHF --- Franco Suíço\
-   EUR --- Euro\
-   CAD --- Dólar Canadense\
-   AUD --- Dólar Australiano\
-   NZD --- Dólar Neozelandês\
-   JPY --- Iene Japonês

------------------------------------------------------------------------

## 🛠️ Tecnologias utilizadas

-   Python 3\
-   Streamlit\
-   Pandas\
-   Altair\
-   Requests\
-   ExchangeRate-API

------------------------------------------------------------------------

## 📡 Fonte dos dados

API pública de câmbio:

https://open.er-api.com/v6/latest/USD

------------------------------------------------------------------------

## ⏱️ Atualização dos dados

-   Atualização automática da interface: **a cada 30 segundos**
-   Cache da API: **30 segundos**
-   Horário da última chamada à API exibido no dashboard

------------------------------------------------------------------------

## ▶️ Como executar localmente

1.  Clone o repositório\
2.  Crie um ambiente virtual\
3.  Instale as dependências\
4.  Execute:

streamlit run currency_strength_dashboard.py

------------------------------------------------------------------------

## 🌐 Deploy

Compatível com **Streamlit Community Cloud**\
Repositório pode ser **público ou privado**

------------------------------------------------------------------------

## 👨‍💻 Autor

**Luan Ortega**\
Analista de Dados / Desenvolvedor

LinkedIn:\
https://www.linkedin.com/in/luan-carlos-ortega-a73422199

------------------------------------------------------------------------

⭐ Se este projeto foi útil, considere deixar uma estrela!
