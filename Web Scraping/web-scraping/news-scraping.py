import requests
import csv
from bs4 import BeautifulSoup

header = {"User-Agent": "Mozilla/5.0"}

url = "https://indeks.kompas.com/"
response = requests.get(url, headers = header)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all("div", class_="articleItem-wrap")

print("Jumlah artikel yang ditemukan:", len(articles), "\n")

with open("news_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Judul Berita", "Tanggal", "Link berita"])

    for article in articles:
        title_element = article.find("h2", class_="articleTitle")
        category_element = article.find("div", class_="articlePost-subtitle")
        date_element = article.find("div", class_="articlePost-date")

        title_news = title_element.text.strip() if title_element else "Title Not Found"
        category_news = category_element.text.strip() if category_element else "Category Not Found"
        date_news = date_element.text.strip() if date_element else "-"

        print("Judul Berita:", title_news)
        print("Tanggal:", date_news)
        print("Kategori berita:", category_news)
        print("\n")

        writer.writerow([title_news, date_news, category_news])

print('Scraping selesai! Data berita telah disimpan')