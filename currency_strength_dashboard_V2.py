import os
import requests
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import time
import math
from dotenv import load_dotenv

# =====================
# ENV
# =====================
load_dotenv()
API_KEY = os.getenv("CURRENCY_FREAKS_API_KEY")

if not API_KEY:
    st.error("API Key não encontrada. Verifique o arquivo .env")
    st.stop()

# =====================
# CONFIG
# =====================
API_URL = "https://api.currencyfreaks.com/v2.0/rates/latest"
CURRENCIES = ["USD", "GBP", "CHF", "EUR", "CAD", "AUD", "NZD", "JPY", "XAU"]
CACHE_TTL = 43200 # 12 horas
AUTO_REFRESH = 43200 # 12 horas

# =====================
# STREAMLIT
# =====================
st.set_page_config(
    page_title="Currency Strength Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem !important;
    }
    h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💱 Currency Strength Dashboard")
st.caption("Monitoramento intraday de força de moedas")

# =====================
# API
# =====================
@st.cache_data(ttl=CACHE_TTL)
def load_rates():
    api_key = os.getenv("CURRENCY_FREAKS_API_KEY")

    if not api_key:
        raise RuntimeError("API Key não encontrada. Verifique o arquivo .env")

    params = {
        "apikey": api_key
    }

    r = requests.get(API_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    data["_api_call_time"] = datetime.now().strftime("%H:%M:%S")

    return data

# =====================
# STRENGTH
# =====================
import math

def calculate_strength(rates: dict) -> pd.DataFrame:
    base = {}

    # cálculo base (exceto USD)
    for c in CURRENCIES:
        if c == "USD":
            continue
        if c in rates:
            base[c] = -math.log(float(rates[c]))

    if len(base) < 2:
        raise ValueError("Poucas moedas para calcular força")

    # normalização por mediana
    median = pd.Series(base).median()
    base = {c: v - median for c, v in base.items()}

    # escala 0–100
    min_val = min(base.values())
    max_val = max(base.values())

    strength = {
        c: round(((v - min_val) / (max_val - min_val)) * 100)
        for c, v in base.items()
    }

    # USD como referência neutra
    strength["USD"] = 50

    return (
        pd.DataFrame(strength.items(), columns=["Currency", "Strength"])
        .sort_values("Strength", ascending=False)
        .reset_index(drop=True)
    )

# =====================
# COLOR SCALE
# =====================
def strength_color(value):
    if value >= 95:
        return "#145a32" 
    elif value >= 90:
        return "#1e8449"
    elif value >= 85:
        return "#27ae60"
    elif value >= 80:
        return "#2ecc71"
    elif value >= 75:
        return "#58d68d"
    elif value >= 70:
        return "#7dcea0"
    elif value >= 65:
        return "#a9dfbf"
    elif value >= 60:
        return "#f9e79f" 
    elif value >= 55:
        return "#f4d03f"
    elif value >= 50:
        return "#f1c40f"
    elif value >= 45:
        return "#f39c12"
    elif value >= 40:
        return "#e67e22"
    elif value >= 35:
        return "#dc7633"
    elif value >= 30:
        return "#e74c3c"
    elif value >= 25:
        return "#cb4335"
    elif value >= 20:
        return "#b03a2e"
    elif value >= 15:
        return "#922b21"
    elif value >= 10:
        return "#7b241c"
    else:
        return "#641e16"

# =====================
# MAIN
# =====================
try:
    raw = load_rates()

    rates = raw["rates"]

    df = calculate_strength(rates)
    df["Color"] = df["Strength"].apply(strength_color)

    last_update = datetime.now().strftime("%d/%m/%y %H:%M")

    # ===== LAYOUT =====
    col1, col2 = st.columns([0.55, 2.0])

    # ===== TABELA ESQUERDA =====
    with col1:
        st.subheader("📊 Strength")

        st.dataframe(
            df[["Currency", "Strength"]].style.applymap(
                lambda v: f"background-color: {strength_color(v)}; color: black; font-weight: 600",
                subset=["Strength"]
            ),
            use_container_width=True,
            hide_index=True
        )

    # ===== GRÁFICO DE BARRAS =====
    with col2:
        st.subheader("📈 Visual")

        chart = (
            alt.Chart(df)
            .mark_bar(
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6
            )
            .encode(
                x=alt.X(
                    "Currency:N",
                    sort=None,
                    axis=alt.Axis(labelFontSize=12)
                ),
                y=alt.Y(
                    "Strength:Q",
                    scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(grid=True)
                ),
                color=alt.Color(
                    "Currency:N",
                    scale=alt.Scale(
                        domain=df["Currency"].tolist(),
                        range=df["Color"].tolist()
                    ),
                    legend=None
                )
            )
            .properties(height=360)
            .configure_view(strokeWidth=0)
            .configure_axis(grid=True)
        )

        st.altair_chart(chart, use_container_width=True)

    # ===== RODAPÉ =====
    refresh_minutes = AUTO_REFRESH // 60 // 60

    st.caption(
        f"Atualizado em: {last_update} • Dados são atualizados a cada: {refresh_minutes} horas"
    )

    # ===== AUTO-REFRESH =====
    time.sleep(AUTO_REFRESH)
    st.rerun()

except Exception as e:
    st.error("Erro ao carregar dados de câmbio")
    st.exception(e)
