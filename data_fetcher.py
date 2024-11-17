import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define constants
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")  # Mapbox API key for location validation
GREENERY_DATA_URL = "https://overpass-api.de/api/interpreter"  # OpenStreetMap Overpass API


def get_weather_data_for_state(state_name):
    """Fetch weather data (temperature, humidity) for a state from OpenWeatherMap API."""
    # OpenWeatherMap doesn't directly provide weather data for states, only cities.
    # We can attempt to get weather data for the capital city of the state.
    # Here, we need a dictionary or database of states and their capitals. We will assume that this exists.
    
    # Get the capital city of the state (you need a mapping from states to capitals)
    state_capitals = {
        "California": "Sacramento",
        "Texas": "Austin",
        "Florida": "Tallahassee",
        "New York": "Albany",
        "Illinois": "Springfield",
        # Add more state capitals as needed
    }
    
    capital_city = state_capitals.get(state_name)

    if capital_city:
        # Now fetch the weather data for the capital city
        url = f"{BASE_URL}/weather?q={capital_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "state": state_name,
                "capital": capital_city,
                "temperature": data["main"]["temp"],  # Temperature in Celsius
                "humidity": data["main"]["humidity"],  # Humidity percentage
                "weather_description": data["weather"][0]["description"]
            }
            return weather_info
        else:
            print(f"Error fetching weather data for {capital_city}: {response.status_code}, {response.text}")
    else:
        print(f"No capital found for state: {state_name}")
    
    return None


def validate_us_state(state_name):
    """Validate that a state is in the USA using Mapbox API."""
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{state_name}.json"
    params = {"access_token": MAPBOX_API_KEY, "types": "region", "country": "us"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["features"]:
            feature = data["features"][0]
            return {
                "state": feature["text"],
                "coordinates": feature["center"]
            }
    print(f"State validation failed for {state_name}.")
    return None


def get_greenery_data(coordinates):
    """Fetch the number of green spaces (parks) using OpenStreetMap Overpass API."""
    lon, lat = coordinates
    radius = 10000  # 10 km radius
    query = f"""
    [out:json];
    (
      node["leisure"="park"](around:{radius},{lat},{lon});
      way["leisure"="park"](around:{radius},{lat},{lon});
      relation["leisure"="park"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.get(GREENERY_DATA_URL, params={"data": query})
    if response.status_code == 200:
        data = response.json()
        return len(data.get("elements", []))  # Approximation: count green spaces
    print("Error fetching greenery data.")
    return 0
