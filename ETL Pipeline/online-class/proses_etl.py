import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# 1. Proses Extract Data
df = pd.read_csv('client_online_class.csv')

# 2. Proses Transform Data
# Membuat huruf kapital untuk kolom status
df['completion_status'] = df['completion_status'].str.upper()
df['payment_status'] = df['payment_status'].str.upper()
# Mencatat jam berapa data ini diproses
df['processed_at'] = datetime.now()

# 3. Proses Load Data
db_user = 'postgres'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'portfolio_de'

connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)
# Proses Memasukkan Data ke Database
df.to_sql('online_class_clients', engine, if_exists='append', index=False)
print("Data berhasil dimasukkan ke database!")