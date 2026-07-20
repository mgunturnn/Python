import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine
import os
from datetime import datetime

# 1. Proses Extract Data dari BigQuery
print("Memulai koneksi ke BigQuery")
# Inisialiasi key untuk autentikasi ke Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key-gcp.json"
client = bigquery.Client()

# Query untuk mengambil data dari BigQuery
query = """
    SELECT
        order_id, 
        user_id, 
        status, 
        gender, 
        created_at, 
        returned_at, 
        shipped_at, 
        delivered_at, 
        num_of_item
    FROM `bigquery-public-data.thelook_ecommerce.orders`
    WHERE created_at >= '2024-01-01' 
    LIMIT 1000
"""

print("Crawling daata dari BigQuery")
df = client.query(query).to_dataframe()
print(f"Sukses crawling data, jumlah record: {len(df)}")

# 2. Proses Transform Data dari BigQuery
print("Memulai proses transform data")

# Menghapus zona waktu
waktu_kolom = ['created_at', 'returned_at', 'shipped_at', 'delivered_at']
for col in waktu_kolom:
    # Ubah format menjadi datetime
    df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)

# Tambahkan info waktu kapan dieksekusi
df['processed_at'] = datetime.now()

# 3. Proses Load Data dari BigQuery
print("Meload data ke data warehouse")
db_user = 'postgres'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'porto_bigquery'

connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

try:
    # Masukkan data ke tabel ecommerce_orders
    df.to_sql('ecommerce_orders', engine, if_exists='append', index=False)
    print("Sukses meload data ke data warehouse")
except Exception as e:
    print(f"Gagal meload data ke data warehouse: {e}")
