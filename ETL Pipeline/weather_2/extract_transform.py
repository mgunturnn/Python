import requests

# Fetch weather data from Open-Meteo API for Bandung, Indonesia
url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9147&longitude=107.6098&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FJakarta"
response = requests.get(url)
data = response.json()

# Fetch 'daily' data from the API response
daily_data = data['daily']

# Extract the data
dates = daily_data['time']
max_temps = daily_data['temperature_2m_max']
min_temps = daily_data['temperature_2m_min']

weather_data = []

# Combine the extracted data into a list of dictionaries
for date, max_t, min_t in zip(dates, max_temps, min_temps):
    weather_data.append({
        'date': date,
        'max_temp': max_t,
        'min_temp': min_t
    })

print(weather_data)