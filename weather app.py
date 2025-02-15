import requests
import matplotlib.pyplot as plt

# Constants
API_KEY = "your_openweathermap_api_key"
BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

def get_coordinates(city_name):
    """Get latitude and longitude for a given city name."""
    params = {
        'q': city_name,
        'appid': API_KEY
    }
    response = requests.get(GEO_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
        else:
            print("City not found!")
    else:
        print(f"Error: {response.status_code}")
    return None, None

def fetch_weather_data(lat, lon):
    """Fetch weather data using coordinates."""
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly,alerts',
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def display_current_weather(current):
    """Display current weather information."""
    print("\n--- Current Weather ---")
    print(f"Temperature: {current['temp']}°C")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind Speed: {current['wind_speed']} m/s")
    print(f"Description: {current['weather'][0]['description'].capitalize()}")

def display_forecast(daily):
    """Display 7-day weather forecast."""
    print("\n--- 7-Day Forecast ---")
    for day in daily:
        date = day['dt']
        temp_day = day['temp']['day']
        temp_night = day['temp']['night']
        description = day['weather'][0]['description'].capitalize()
        print(f"Date: {date}, Day: {temp_day}°C, Night: {temp_night}°C, {description}")

def plot_temperature_chart(daily):
    """Plot temperature chart for the next 7 days."""
    dates = [day['dt'] for day in daily]
    temps = [day['temp']['day'] for day in daily]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, temps, marker='o', label='Day Temperature')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('7-Day Temperature Trend')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    print("Welcome to the Weather App!")
    city_name = input("Enter the city name: ")
    lat, lon = get_coordinates(city_name)

    if lat is not None and lon is not None:
        data = fetch_weather_data(lat, lon)
        if data:
            display_current_weather(data['current'])
            display_forecast(data['daily'][:7])
            plot_temperature_chart(data['daily'][:7])

if __name__ == "__main__":
    main()
