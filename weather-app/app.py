from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

def get_weather(city):
    openweathermap_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'

    openweathermap_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}'

    try:
        response = requests.get(openweathermap_url)
        response.raise_for_status()
        weather_data = json.loads(response.text)

        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        temperature_celsius = temperature - 273.15

        weather_forecast = {
            'city': city,
            'temperature': f"{temperature_celsius:.2f}°C",
            'description': description,
            'latitude': weather_data['coord']['lat'],
            'longitude': weather_data['coord']['lon'],
            'google_maps_api_key': google_maps_api_key
        }

        return weather_forecast

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city_name = request.form['city']
        weather_data = get_weather(city_name)
        return render_template('index.html', weather_data=weather_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
