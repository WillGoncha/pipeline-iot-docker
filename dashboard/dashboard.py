
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from src.connection import engine


# Configuração da página
st.set_page_config(
    page_title="Dashboard IoT",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ Dashboard de Temperaturas IoT")
st.write("Análise dos dados reais de temperatura armazenados no PostgreSQL.")

# Função para consultar as Views SQL
@st.cache_data(ttl=60)
def carregar_dados(view_name):
    consultas = {
        "avg_temp_por_ambiente": """
            SELECT * FROM avg_temp_por_ambiente
        """,
        "leituras_por_hora": """
            SELECT * FROM leituras_por_hora
        """,
        "temp_max_min_por_dia": """
            SELECT * FROM temp_max_min_por_dia
        """
    }

    if view_name not in consultas:
        raise ValueError("View não permitida.")

    with engine.connect() as conexao:
        return pd.read_sql(
            text(consultas[view_name]),
            conexao
        )


try:
    # Carrega os dados das três Views
    df_ambiente = carregar_dados("avg_temp_por_ambiente")
    df_hora = carregar_dados("leituras_por_hora")
    df_diaria = carregar_dados("temp_max_min_por_dia")

    # Indicadores gerais
    with engine.connect() as conexao:
        resumo = pd.read_sql(
            text("""
                SELECT
                    COUNT(*) AS total,
                    MIN(temperatura) AS minima,
                    MAX(temperatura) AS maxima,
                    ROUND(AVG(temperatura), 2) AS media
                FROM leituras_iot
            """),
            conexao
        )

    total = int(resumo.loc[0, "total"])
    minima = int(resumo.loc[0, "minima"])
    maxima = int(resumo.loc[0, "maxima"])
    media = float(resumo.loc[0, "media"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total de leituras", f"{total:,}".replace(",", "."))
    col2.metric("Temperatura mínima", f"{minima} °C")
    col3.metric("Temperatura máxima", f"{maxima} °C")
    col4.metric("Temperatura média", f"{media:.2f} °C")

    st.divider()

    # Gráfico 1: Temperatura média por ambiente
    st.header("1. Temperatura média por ambiente")

    fig1 = px.bar(
        df_ambiente,
        x="ambiente",
        y="temperatura_media",
        color="ambiente",
        labels={
            "ambiente": "Ambiente",
            "temperatura_media": "Temperatura média (°C)"
        },
        text="temperatura_media"
    )

    fig1.update_traces(texttemplate="%{text:.2f} °C")
    st.plotly_chart(fig1, use_container_width=True)

    st.caption(
        "View SQL: avg_temp_por_ambiente. "
        "Compara as temperaturas médias dos ambientes internos e externos."
    )

    st.divider()

    # Gráfico 2: Leituras por hora
    st.header("2. Quantidade de leituras por hora")

    fig2 = px.line(
        df_hora,
        x="hora",
        y="contagem",
        markers=True,
        labels={
            "hora": "Hora do dia",
            "contagem": "Quantidade de leituras"
        }
    )

    fig2.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        "View SQL: leituras_por_hora. "
        "Mostra a distribuição das leituras ao longo das 24 horas."
    )

    st.divider()

    # Gráfico 3: Temperaturas por dia
    st.header("3. Temperaturas máximas e mínimas por dia")

    df_diaria["data"] = pd.to_datetime(df_diaria["data"])

    fig3 = px.line(
        df_diaria,
        x="data",
        y=["temp_max", "temp_min"],
        labels={
            "data": "Data",
            "value": "Temperatura (°C)",
            "variable": "Medição",
            "temp_max": "Temperatura máxima",
            "temp_min": "Temperatura mínima"
        }
    )

    fig3.update_layout(
        legend_title_text="Temperaturas"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.caption(
        "View SQL: temp_max_min_por_dia. "
        "Apresenta as temperaturas máximas e mínimas registradas por dia."
    )

    # Tabela de dados
    with st.expander("Consultar dados das Views"):
        st.subheader("Temperatura média por ambiente")
        st.dataframe(df_ambiente, use_container_width=True)

        st.subheader("Leituras por hora")
        st.dataframe(df_hora, use_container_width=True)

        st.subheader("Temperaturas por dia")
        st.dataframe(df_diaria, use_container_width=True)

except Exception as erro:
    st.error("Não foi possível carregar os dados do PostgreSQL.")
    st.code(str(erro))
    st.info(
        "Verifique se o contêiner postgres-iot está ativo "
        "e se as três Views SQL foram criadas."
    )