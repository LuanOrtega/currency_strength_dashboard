import requests
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import time

# =====================
# CONFIG
# =====================
API_URL = "https://open.er-api.com/v6/latest/USD"
CURRENCIES = ["GBP", "CHF", "EUR", "CAD", "AUD", "NZD", "JPY"]
CACHE_TTL = 30
AUTO_REFRESH = 30

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
st.caption("Fonte: ExchangeRate-API (dados intraday)")

# =====================
# API
# =====================
@st.cache_data(ttl=CACHE_TTL)
def load_rates():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()

    data["_api_call_time"] = datetime.now().strftime("%H:%M:%S")

    if data.get("result") != "success":
        raise RuntimeError("Falha ao obter dados de câmbio")

    return data

# =====================
# STRENGTH
# =====================
def calculate_strength(rates: dict) -> pd.DataFrame:
    base = {}

    for c in CURRENCIES:
        base[c] = 1 / rates[c]

    max_val = max(base.values())

    strength = {
        c: round((v / max_val) * 100)
        for c, v in base.items()
    }

    return (
        pd.DataFrame(strength.items(), columns=["Currency", "Strength"])
        .sort_values("Strength", ascending=False)
        .reset_index(drop=True)
    )

# =====================
# COLOR SCALE
# =====================
def strength_color(value):
    if value >= 85:
        return "#2ecc71"
    elif value >= 70:
        return "#6ab04c"
    elif value >= 55:
        return "#f1c40f"
    elif value >= 40:
        return "#e67e22"
    else:
        return "#e74c3c"

# =====================
# MAIN
# =====================
try:
    raw = load_rates()
    call_api = raw["_api_call_time"]

    rates = raw["rates"]

    df = calculate_strength(rates)
    df["Color"] = df["Strength"].apply(strength_color)

    last_update = datetime.strptime(
        raw["time_last_update_utc"],
        "%a, %d %b %Y %H:%M:%S %z"
    ).strftime("%d/%m/%y %H:%M")

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
        )

        st.altair_chart(chart, use_container_width=True)

    # ===== RODAPÉ COMPACTO =====
    st.caption(
        f"Última atualização: {last_update} • Atualização automática a cada {CACHE_TTL // 60} minutos • Última chamada à API: {call_api}"
    )

    # ===== AUTO-REFRESH =====
    time.sleep(AUTO_REFRESH)
    st.rerun()

except Exception as e:
    st.error("Erro ao carregar dados de câmbio")
    st.exception(e)