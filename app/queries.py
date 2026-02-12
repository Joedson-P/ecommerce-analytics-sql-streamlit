import sqlite3
import pandas as pd
import os

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'ecommerce_brasil.db')
    return sqlite3.connect(db_path)

def get_unique_status():
    conn = get_connection()
    query = "SELECT DISTINCT Purchase_Status FROM orders"
    status = pd.read_sql(query, conn)['Purchase_Status'].to_list()
    conn.close()
    return status

def get_filtered_data(status_filter):
    conn = get_connection()
    where_clause = "" if  status_filter == 'Todos' else f'Where o.Purchase_Status = "{status_filter}"'
    query = f"""
    SELECT
        o.Id, o.Order_Date, o.Total, o.Purchase_Status,
        p.Subcategory
    FROM orders o
    JOIN shopping s ON o.Id = s.Id
    JOIN products p ON s.Product = p.Product_Name
    {where_clause}
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_kpis():
    conn = get_connection()
    # Query para métricas globais
    query = """
    SELECT
        SUM(Total) as faturamento_total,
        COUNT(Id) as total_pedidos,
        AVG(Total) as ticket_medio
    FROM orders
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_vendas_por_dia():
    conn = get_connection()
    # Agrupando vendas por data
    query = """
    SELECT
        DATE(Order_Date) as data_venda,
        SUM(Total) as faturamento_diario
    FROM orders
    GROUP BY data_venda
    ORDER BY data_venda
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_vendas_por_subcategoria():
    conn = get_connection()
    # Fazendo JOIN triplo: orders -> shopping -> products
    query = """
    SELECT
        p.Subcategory,
        SUM(o.Total) as faturamento_categoria
    FROM Orders o
    JOIN shopping s ON o.Id = s.Id
    JOIN products p ON s.Product = p.Product_Name
    GROUP BY p.Subcategory
    ORDER BY faturamento_categoria DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df