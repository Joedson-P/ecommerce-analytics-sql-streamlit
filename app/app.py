import streamlit as st
import pandas as pd
from queries import get_unique_status, get_filtered_data
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas E-commerce", layout="wide")


# --- SIDEBAR ---
st.sidebar.header("Filtros")
status_list = ["Todos"] + get_unique_status()
selected_status = st.sidebar.selectbox("Selecione o Status da Compra", status_list)

# --- CARREGAMENTO DE DADOS FILTRADOS ---
df_filtered = get_filtered_data(selected_status)

st.sidebar.divider()
st.sidebar.subheader("Período")

df_filtered['Order_Date'] = pd.to_datetime(df_filtered['Order_Date'])
min_date = df_filtered["Order_Date"].min().date()
max_date = df_filtered['Order_Date'].max().date()

date_range = st.sidebar.date_input(
    "Selecione o Intervalo",
    value=(min_date, max_date),
    min_value = min_date,
    max_value = max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered["Order_Date"].dt.date >= start_date) &
        (df_filtered['Order_Date'].dt.date <= end_date)
    ]

# --- TÍTULO ---
st.title("Dashboard de Análise de E-commerce")
st.markdown(f"Exibindo dados para o status **{selected_status}**")

# --- LINHA 1: KPIs Dinâmicos ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Faturamento", f"R${df_filtered['Total'].sum():,.2f}")
kpi2.metric("Pedidos", f"{len(df_filtered)}")
kpi3.metric("Ticket Médio", f"R$ {df_filtered['Total'].mean():,.2f}")

st.divider()

# --- LINHA 2: Gráficos ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Faturamento por Subcategoria")
    vendas_cat = df_filtered.groupby('Subcategory')['Total'].sum().reset_index()
    fig_bar = px.bar(vendas_cat, x='Total', y='Subcategory', orientation='h', color='Subcategory')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Status dos Pedidos (Proporção)")
    fig_pie = px.pie(df_filtered, names='Purchase_Status', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)