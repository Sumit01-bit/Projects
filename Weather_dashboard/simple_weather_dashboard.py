
import requests
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Configuration
API_KEY = "e8d141af7784739e336efa6d87f7b76e"  # Get from https://openweathermap.org/api
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city_name):
    """
    Simple function to fetch weather data for a city
    """
    # Build the complete URL
    url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"

    # Make API request
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Could not fetch weather data for {city_name}")
        return None

def show_weather(weather_data):
    """
    Display weather information in a readable format
    """
    if weather_data:
        city = weather_data['name']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

        print(f"\nWeather in {city}:")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {description.title()}")

def create_simple_chart(weather_data):
    """
    Create a simple bar chart
    """
    if not weather_data:
        return

    # Extract data for chart
    city = weather_data['name']
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    # Create chart data
    categories = ['Temperature (°C)', 'Humidity (%)']
    values = [temp, humidity]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color=['red', 'blue'])
    plt.title(f'Weather Data for {city}')
    plt.ylabel('Values')

    # Show the chart
    plt.show()

    # Save the chart
    plt.savefig(f'weather_{city.lower()}.png')
    print(f"Chart saved as weather_{city.lower()}.png")

def save_weather_data(weather_data):
    """
    Save weather data to a CSV file
    """
    if not weather_data:
        return

    # Prepare data
    data_row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        weather_data['name'],
        weather_data['main']['temp'],
        weather_data['main']['humidity'],
        weather_data['weather'][0]['description']
    ]

    # Save to CSV
    with open('weather_history.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        # Add header if file is empty
        file.seek(0, 2)  # Go to end of file
        if file.tell() == 0:  # If file is empty
            writer.writerow(['Date', 'City', 'Temperature', 'Humidity', 'Description'])

        writer.writerow(data_row)

    print("Weather data saved to weather_history.csv")

# Main program
def main():
    print("Simple Weather Dashboard")
    print("=" * 25)

    if not API_KEY:
        print("Please set your OpenWeatherMap API key in the script!")
        print("Get a free key at: https://openweathermap.org/api")
        return

    city = input("Enter city name: ")

    print(f"Getting weather for {city}...")
    weather = fetch_weather(city)

    if weather:
        show_weather(weather)

        chart_choice = input("\nShow chart? (y/n): ").lower()
        if chart_choice == 'y':
            create_simple_chart(weather)

        save_choice = input("Save data to CSV? (y/n): ").lower()
        if save_choice == 'y':
            save_weather_data(weather)
if __name__ == "__main__":
    main()
