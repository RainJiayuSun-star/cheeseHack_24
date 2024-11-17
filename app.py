import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from greening_suggestions import suggest_greening  # Import the greening suggestion function

# Load environment variables from .env file
load_dotenv()

# Define constants
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

app = Flask(__name__)

def get_weather_data_for_state(state_name):
    """Fetch weather data (temperature, humidity) for the capital of the state from OpenWeatherMap API."""
    # Check if state_name is valid and get the corresponding capital city (this is case-insensitive)
    states = load_states()  # Load states and capitals
    capital = None
    for state in states:
        if state["name"].strip().lower() == state_name.lower():
            capital = state["capital"]
            break

    if not capital:
        return None  # State not found

    # If we have a capital, fetch weather data for that capital
    url = f"{BASE_URL}/weather?q={capital}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "state": state_name,
            "capital": capital,
            "temperature": data["main"]["temp"],  # Temperature in Celsius
            "humidity": data["main"]["humidity"],  # Humidity percentage
            "weather_description": data["weather"][0]["description"]  # Weather condition
        }
        return weather_info
    else:
        print(f"Error fetching weather data for {capital}: {response.status_code}, {response.text}")
        return None

def load_states():
    """Load states and their capitals from a JSON file."""
    with open('states.json', 'r') as file:
        states_data = json.load(file)
    return states_data

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    greening_advice = "Consider planting trees and shrubs to improve urban greenery!"
    greening_suggestion = None

    if request.method == "POST":
        state_name = request.form["state_name"].strip().lower()
        print(f"User entered state: {state_name}")

        # Fetch weather data for the state
        weather_data = get_weather_data_for_state(state_name)
        if not weather_data:
            error = "Incorrect State entered! Please enter an US State!"
        else:
            # Get greening suggestions based on temperature
            temperature = weather_data["temperature"]
            greening_suggestion = suggest_greening(temperature)

    return render_template(
        "index.html", 
        weather_data=weather_data, 
        error=error,
        greening_advice=greening_advice,
        greening_suggestion=greening_suggestion  # Pass greening suggestion to the template
    )

if __name__ == "__main__":
    app.run(debug=True)
