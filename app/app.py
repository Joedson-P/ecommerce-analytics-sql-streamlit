import streamlit as st
import pandas as pd
from queries import get_unique_status, get_filtered_data
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas E-commerce", layout="wide")


# --- SIDEBAR ---
st.sidebar.header("Filtros")
status_list = ["Todos"] + get_unique_status()
selected_status = st.sidebar.selectbox("Selecione o Status da Compra", status_list)

# --- CARREGAMENTO DE DADOS FILTRADOS ---
df_filtered = get_filtered_data(selected_status)

st.sidebar.markdown("---")
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

# Botão de download
st.sidebar.markdown("---")
st.sidebar.subheader("Exportar Dados")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Baixar Relatório em CSV",
    data=csv,
    file_name=f'vendas_{selected_status}.csv',
    mime='text/csv',
)

# Função para segmentação
def processar_segmentacao(df):
    if df.empty:
        return pd.DataFrame()
    
    # Preparação dos dados
    data_ref = df['Order_Date'].max() + pd.Timedelta(days=1)

    df_rfm = df.groupby('Id').agg({
        'Order_Date': lambda x: (data_ref - x.max()).days,
        'Total': 'sum'
    }).rename(columns={
        'Order_Date': 'Recencia',
        'Total': 'Monetario'
    }).reset_index()

    # Machine Learning
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_rfm[['Recencia', 'Monetario']])

    model = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_rfm['Cluster'] = model.fit_predict(X_scaled)

    # Nomeação inteligente dos Clusters
    resumo = df_rfm.groupby('Cluster').agg({'Recencia':'mean', 'Monetario':'mean'})

    nomes = {}
    for i, row in resumo.iterrows():
        if row['Monetario']>resumo['Monetario'].quantile(0.75):
            nomes[i] = 'VIP'
        elif row['Recencia'] <= resumo['Recencia'].median() and row['Monetario'] > resumo['Monetario'].median():
            nomes[i] = 'Potencial'
        elif row['Recencia'] <= resumo['Recencia'].median():
            nomes[i] = 'Ativo'
        else:
            nomes[i] = 'Em Risco'
    
    df_rfm['Segmento'] = df_rfm['Cluster'].map(nomes)
    return df_rfm

# --- TÍTULO ---
st.title("Dashboard de Análise de E-commerce")
st.markdown(f"Exibindo dados para o status **{selected_status}**")

# --- CRIAÇÃO DE ABAS ---
tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Análise Regional", "Pagamentos", "Segmentação"])

with tab1:
    # --- LINHA 1: KPIs Dinâmicos ---
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Faturamento", f"R${df_filtered['Total'].sum():,.2f}")
    kpi2.metric("Pedidos", f"{len(df_filtered)}")
    kpi3.metric("Ticket Médio", f"R$ {df_filtered['Total'].mean() if not df_filtered.empty else 0:,.2f}")

    st.markdown("---")

    # --- LINHA 2: Gráficos ---
    st.subheader("Evolução de Vendas no Tempo")
    vendas_tempo = df_filtered.groupby('Order_Date')['Total'].sum().reset_index()
    fig_line = px.line(vendas_tempo, x='Order_Date', y='Total', 
                       title="Faturamento Diário",
                       line_shape="spline", render_mode="svg")
    st.plotly_chart(fig_line, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Faturamento por Subcategoria")
        vendas_cat = df_filtered.groupby('Subcategory')['Total'].sum().reset_index()
        fig_bar = px.bar(vendas_cat, x='Total', y='Subcategory',
                         orientation='h', color='Subcategory', color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("Status dos Pedidos (Proporção)")
        fig_pie = px.pie(df_filtered, names='Purchase_Status', 
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader('Performance Geográfica')
    vendas_estado = df_filtered.groupby('State')['Total'].sum().reset_index().sort_values('Total', ascending=False)
    vendas_estado_fmt = vendas_estado.copy()
    vendas_estado_fmt['Total'] = vendas_estado_fmt['Total'].apply(lambda x: f"R$ {x:,.2f}")

    col_map, col_table = st.columns([2, 1])

    with col_map:
        fig_map = px.bar(vendas_estado.head(10), x='Total', y='State', orientation='h',
                         color='Total', color_continuous_scale='Viridis', )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_table:
        st.dataframe(vendas_estado_fmt, hide_index=True)

with tab3:
    st.subheader("Métodos de Pagamento")
    vendas_pay = df_filtered.groupby('payment')['Total'].sum().reset_index()
    fig_pay = px.pie(vendas_pay, values='Total', names='payment', hole=0.3,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pay, use_container_width=True)

with tab4:
    st.subheader('Segmentação Estratégica de Clientes')
    st.markdown('Utilizamos o algoritmo **K-Means** para agrupar clientes por comportamento de compra.')

    df_segmentado = processar_segmentacao(df_filtered)
    
    if not df_segmentado.empty:
        col1, col2, col3, col4 = st.columns(4)

        for i, seg in enumerate(['VIP', 'Potencial', 'Ativo', 'Em Risco']):
            dados_seg = df_segmentado[df_segmentado['Segmento'] == seg]
            cols = [col1, col2, col3, col4]
            cols[i].metric(seg, f"{len(dados_seg)} Clientes", f"R$ {dados_seg['Monetario'].mean():,.0f} avg")

        st.markdown("---")

        # Gráfico Scatter Plot Interativo
        fig_seg = px.scatter(
            df_segmentado,
            x='Recencia',
            y='Monetario',
            color='Segmento',
            title='Distribuição de Clientes por Segmento',
            labels={'Recencia':'Dias desde a última compra', 'Monetario':'Valor Total Gasto (R$)'},
            hover_data=['Id'],
            color_discrete_map={'VIP':'gold', 'Potencial':'green', 'Ativo':'blue', 'Em Risco':'red'}
        )
        st.plotly_chart(fig_seg, use_container_width=True)
    else:
        st.warning("Sem dados suficientes para segmentação.")