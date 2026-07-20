import requests
import csv
from bs4 import BeautifulSoup

# ini adalah basic signature untuk mengindentifikasi bahwa request ini berasal dari browser, 
# bukan skrip python. Ini membantu menghindari pemblokiran oleh server.
header = {"User-Agent": "Mozilla/5.0"} 

response = requests.get("https://quotes.toscrape.com/", headers=header)
soup = BeautifulSoup(response.text, 'html.parser')

# response.text berisi HTML dari halaman web yang diambil, dan kita memparsenya (html.parser) 
# menggunakan BeautifulSoup untuk memudahkan ekstraksi data.

quotes = soup.find_all('div', class_='quote')
# find_all digunakan untuk menemukan semua elemen <div> dengan class 'quote',
# yang berisi kutipan-kutipan dari halaman web.

for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small',class_='author').text
    tags = []
    for tag in quote.find_all('a', class_='tag'):
        tags.append(tag.text)
    print(text, '\n-', author)
    print('Tags:', ', '.join(tags), '\n')

with open('quotes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Quote", "Author", "Tags"])
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small',class_='author').text
        tags = []
        for tag in quote.find_all('a', class_='tag'):
            tags.append(tag.text) 
        writer.writerow([text, author, tags])

print('Done! csv file is ready')