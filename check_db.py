import sqlite3
import pandas as pd

conn = sqlite3.connect('ecommerce_brasil.db')

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tabelas no banco:")
print(tables)

# Visualizando as 5 primeiras linhas da tabela de pedidos
print("\n5 Primeiras linhas  de FACT_Orders:")
df = pd.read_sql("SELECT * FROM orders LIMIT 5;", conn)
print(df)

conn.close()