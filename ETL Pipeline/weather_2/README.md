1. Project Objective
   Proyek ini bertujuan untuk membangun infrastruktur pipa data (ETL) otomatis yang mengekstraksi data prakiraan cuaca harian dari sumber publik, mengubahnya menjadi format tabular yang bersih, dan memuatnya ke dalam gudang data berbasis cloud untuk kebutuhan analisis dan visualisasi pemangku kepentingan.
3. Architecture & Data Flow
   - Data Source: Open-Meteo API (REST API).
   - Data Orchestration & Scheduling: Apache Airflow
   - Data Processing: Python
   - Data Warehouse: Google BigQuery
   - Business Intelligence: Google Looker Studio.
5. Data Schema
   Data yang dimuat ke dalam tabel BigQuery memiliki struktur berikut:
   - date (DATE): Tanggal prakiraan cuaca.
   - max_temp (FLOAT): Suhu maksimum harian dalam Celcius.
   - min_temp (FLOAT): Suhu minimum harian dalam Celcius.
7. ETL Process
   - Extract: Fungsi Python mengirimkan permintaan HTTP GET ke endpoint Open-Meteo API. Data JSON berisi prakiraan 7 hari ke depan di-fetch dan dikumpulkan pada array daily.
   - Transform: Proses transformasi dilakukan menggunakan struktur data Python (seperti merangkai array tunggal ke dalam format list of tuples melalui perulangan/looping). Pendekatan ini dipilih karena struktur respons API sudah cukup rapi, sehingga data bisa langsung disiapkan untuk di-load.
   - Load: Menggunakan modul bigquery.Client(), data hasil transformasi dimuat ke cloud melalui eksekusi query berparameter. Proses keseluruhan diotomatisasi melalui PythonOperator di dalam Airflow DAG yang dijadwalkan berjalan setiap hari (@daily)
9. Troubleshooting
   - Kendala Streaming: Proses load data satu per satu terbatas karena pembatasan akun (rate limits).
   - Solusi Batch Load: Proses load data menggunakan sistem pemrosesan per Batch.
