import requests
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Configuration
API_KEY = "e8d141af7784739e336efa6d87f7b76e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city_name):
    """
    Fetch weather data from OpenWeatherMap API with error handling
    """
    url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Ensure expected fields exist
        if 'main' in data and 'weather' in data and 'name' in data:
            return data
        else:
            print("Error: Incomplete weather data received.")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

def show_weather(weather_data):
    """
    Display weather information in a readable format with fallback
    """
    try:
        city = weather_data['name']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

        print(f"\nWeather in {city}:")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {description.title()}")

    except (KeyError, TypeError) as e:
        print(f"Error displaying weather data: {e}")

def create_simple_chart(weather_data):
    """
    Create and save a bar chart of temperature and humidity with exception handling
    """
    try:
        city = weather_data['name']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        categories = ['Temperature (°C)', 'Humidity (%)']
        values = [temp, humidity]

        plt.figure(figsize=(8, 5))
        plt.bar(categories, values, color=['red', 'blue'])
        plt.title(f'Weather Data for {city}')
        plt.ylabel('Values')

        plt.tight_layout()
        plt.show()

        filename = f'weather_{city.lower()}.png'
        plt.savefig(filename)
        print(f"Chart saved as {filename}")

    except KeyError as e:
        print(f"Missing key in weather data: {e}")
    except Exception as e:
        print(f"Error creating chart: {e}")

def save_weather_data(weather_data):
    """
    Save weather data to CSV file with file I/O exception handling
    """
    try:
        data_row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            weather_data['name'],
            weather_data['main']['temp'],
            weather_data['main']['humidity'],
            weather_data['weather'][0]['description']
        ]

        with open('weather_history.csv', 'a+', newline='') as file:
            writer = csv.writer(file)

            file.seek(0, 2)  # Move to end of file
            if file.tell() == 0:  # File is empty
                writer.writerow(['Date', 'City', 'Temperature', 'Humidity', 'Description'])

            writer.writerow(data_row)

        print("Weather data saved to weather_history.csv")

    except (IOError, OSError) as e:
        print(f"File I/O error: {e}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    """
    Main program flow with input validation
    """
    print("Simple Weather Dashboard")
    print("=" * 25)

    if not API_KEY:
        print("Please set your OpenWeatherMap API key in the script.")
        return

    city = input("Enter city name: ").strip()
    if not city:
        print("City name cannot be empty.")
        return

    print(f"Getting weather for {city}...")
    weather = fetch_weather(city)

    if weather:
        show_weather(weather)

        try:
            chart_choice = input("\nShow chart? (y/n): ").strip().lower()
            if chart_choice == 'y':
                create_simple_chart(weather)

            save_choice = input("Save data to CSV? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_weather_data(weather)

        except Exception as e:
            print(f"Unexpected error during user interaction: {e}")

if __name__ == "__main__":
    main()
