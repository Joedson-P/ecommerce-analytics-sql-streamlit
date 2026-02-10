import streamlit as st
import pandas as pd
from queries import get_kpis, get_vendas_por_dia, get_vendas_por_subcategoria
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas E-commerce", layout="wide")

st.title("Dashboard de Análise de E-commerce")
st.markdown("Análise de performance de vendas (Brasil)")

# --- BUSCA DE DADOS ---
kpis = get_kpis()
vendas_diarias = get_vendas_por_dia()

# --- LINHA 1: KPIs ---
col1, col2, col3, = st.columns(3)

with col1:
    st.metric("Faturamento Total", f"R$ {kpis['faturamento_total'][0]:,.2f}")

with col2:
    st.metric("Total de Pedidos", f"{int(kpis['total_pedidos'][0])}")

with col3:
    st.metric("Ticket Médio", f"R$ {kpis['ticket_medio'][0]:,.2f}")

st.divider()

# --- LINHA 2: Gráfico de Vendas ---
st.subheader("Evolução de Vendas no Tempo")
fig = px.line(vendas_diarias, x='data_venda', y='faturamento_diario',
              title="Faturamento Diário", labels={'data_venda': 'Data', 'faturamento_diario': 'Faturamento(R$)'})
st.plotly_chart(fig, use_container_width=True)

# --- BUSCA DE DADOS ADICIONAIS ---
vendas_categoria = get_vendas_por_subcategoria()

# --- LINHA 3: Gráfico de Categorias ---
st.divider()
st.subheader("Faturamento por Categoria")
fig_bar = px.bar(vendas_categoria, x='faturamento_categoria', y='Subcategory', orientation='h', color='Subcategory',
                 title='Top Categorias', labels={'faturamento_categoria':'Faturamento (R$)', 'Subcategory':'Subcategoria'})
st.plotly_chart(fig_bar, use_container_width=True)