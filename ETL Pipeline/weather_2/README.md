# 🌤️ Technical Report: Automated Weather Forecast ETL Pipeline

## 🎯 1. Project Objective
Proyek ini bertujuan untuk membangun infrastruktur pipa data (ETL) otomatis yang mengekstraksi data prakiraan cuaca harian dari sumber publik, mengubahnya menjadi format bersih, dan memuatnya ke dalam gudang data berbasis *cloud* untuk kebutuhan analisis dan visualisasi.

## 🏗️ 2. Architecture & Data Flow
*   **Data Source:** Open-Meteo API (REST API) 🌐
*   **Orchestration:** Apache Airflow ⏱️
*   **Data Processing:** Python
*   **Data Warehouse:** Google BigQuery (GCP) ☁️
*   **Business Intelligence:** Google Looker Studio 📊

## 🗄️ 3. Data Schema (BigQuery)
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `date` | `DATE` | Tanggal prakiraan cuaca |
| `max_temp` | `FLOAT` | Suhu maksimum harian (°C) |
| `min_temp` | `FLOAT` | Suhu minimum harian (°C) |

## ⚙️ 4. ETL Process Breakdown
*   **📥 Extract:** Fungsi Python mengirimkan permintaan HTTP GET ke *endpoint* Open-Meteo API. Data berbentuk JSON di-fetch dan dikumpulkan pada elemen `daily` yang berisi metrik tanggal dan suhu.
*   **🔄 Transform:** Menggunakan struktur data *native* Python. *Array* tuggal dirangkai menjadi format *list of tuples* lewat perulangan (*looping*). Pendekatan ini dipilih untuk menjaga efisiensi memori.
*   **📤 Load:** Data hasil transformasi dimuat ke *cloud* melalui `bigquery.Client()`. Seluruh alur ini diotomatisasi oleh `PythonOperator` di Airflow dengan penjadwalan `@daily`.
