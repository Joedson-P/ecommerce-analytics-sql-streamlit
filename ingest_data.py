import pandas as pd
import sqlite3
import os

def ingest_to_sql():
    # Conectar ao banco
    conn = sqlite3.connect('ecommerce_brasil.db')

    #Lista de arquivos para importar
    files = {
        'customers': 'data/DIM_Customer.csv',
        'delivery': 'data/DIM_Delivery.csv',
        'products': 'data/DIM_Products.csv',
        'shopping': 'data/DIM_Shopping.csv',
        'orders': 'data/FACT_Orders.csv'
    }

    print(f"Diretório atual: {os.getcwd()}")

    for table_name, file_path in files.items():
        if os.path.exists(file_path):
            print(f"Importando {file_path} para a tabela '{table_name}'...")
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"   --- Tabela {table_name} criada com {len(df)} linhas.")
            except Exception as e:
                print(f"    Erro ao ler {file_path}: {e}")
        else:
            print(f"Erro: Arquivo {file_path} não encontrado!")

    conn.close()
    print("\n Processo finalizado!")

if __name__ == "__main__":
    ingest_to_sql()