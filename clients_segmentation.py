import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

conn = sqlite3.connect('ecommerce_brasil.db')

query = """
SELECT
    c.Customer_Id,
    o.Order_Date,
    o.Total
    FROM orders o
    JOIN customers c ON o.Id = c.Id
"""

df =pd.read_sql(query, conn)

df['Order_Date'] = pd.to_datetime(df['Order_Date'])

data_hoje = df['Order_Date'].max() + pd.Timedelta(days=1)

# Criando a tabela RFM
df_rfm = df.groupby('Customer_Id').agg({
    'Order_Date': lambda x: (data_hoje - x.max()).days,
    'Customer_Id': 'count',
    'Total': 'sum'
}).rename(columns={
    'Order_Date': 'Recencia',
    'Customer_Id': 'Frequencia',
    'Total': 'Monetario'
}).reset_index()

print("--- Primeiras linhas do RFM ---")
print(df_rfm.head())

print("\n--- Estatísticas Descritivas ---")
print(df_rfm.describe())

