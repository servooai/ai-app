import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY', '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')
BASE_URL = 'https://api.openweathermap.org/data/2.5'

def get_current_weather(city):
    """Fetch current weather data for a city"""
    try:
        url = f'{BASE_URL}/weather'
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def get_forecast(city):
    """Fetch 5-day weather forecast for a city"""
    try:
        url = f'{BASE_URL}/forecast'
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def format_weather_response(weather_data):
    """Format weather data for frontend"""
    if 'error' in weather_data or 'cod' in weather_data and weather_data['cod'] != 200:
        return None
    
    return {
        'city': weather_data.get('name'),
        'country': weather_data.get('sys', {}).get('country'),
        'temperature': weather_data.get('main', {}).get('temp'),
        'feels_like': weather_data.get('main', {}).get('feels_like'),
        'temp_min': weather_data.get('main', {}).get('temp_min'),
        'temp_max': weather_data.get('main', {}).get('temp_max'),
        'humidity': weather_data.get('main', {}).get('humidity'),
        'pressure': weather_data.get('main', {}).get('pressure'),
        'wind_speed': weather_data.get('wind', {}).get('speed'),
        'wind_deg': weather_data.get('wind', {}).get('deg'),
        'cloudiness': weather_data.get('clouds', {}).get('all'),
        'description': weather_data.get('weather', [{}])[0].get('main'),
        'details': weather_data.get('weather', [{}])[0].get('description'),
        'icon': weather_data.get('weather', [{}])[0].get('icon'),
        'sunrise': weather_data.get('sys', {}).get('sunrise'),
        'sunset': weather_data.get('sys', {}).get('sunset'),
        'visibility': weather_data.get('visibility'),
        'rain': weather_data.get('rain', {}).get('1h', 0)
    }

@app.route('/weather/current', methods=['GET'])
def current_weather():
    """Get current weather for a city"""
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    weather_data = get_current_weather(city)
    
    if 'error' in weather_data or (weather_data.get('cod') != 200 and 'cod' in weather_data):
        return jsonify({'error': f"City not found: {city}"}), 404
    
    formatted_data = format_weather_response(weather_data)
    return jsonify(formatted_data)

@app.route('/weather/forecast', methods=['GET'])
def weather_forecast():
    """Get 5-day weather forecast for a city"""
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    forecast_data = get_forecast(city)
    
    if 'error' in forecast_data or (forecast_data.get('cod') != '200' and 'cod' in forecast_data):
        return jsonify({'error': f"City not found: {city}"}), 404
    
    # Process forecast data
    forecasts = []
    for item in forecast_data.get('list', []):
        forecasts.append({
            'dt': item.get('dt'),
            'date': datetime.fromtimestamp(item.get('dt')).strftime('%Y-%m-%d %H:%M'),
            'temperature': item.get('main', {}).get('temp'),
            'feels_like': item.get('main', {}).get('feels_like'),
            'humidity': item.get('main', {}).get('humidity'),
            'pressure': item.get('main', {}).get('pressure'),
            'wind_speed': item.get('wind', {}).get('speed'),
            'description': item.get('weather', [{}])[0].get('main'),
            'details': item.get('weather', [{}])[0].get('description'),
            'icon': item.get('weather', [{}])[0].get('icon'),
            'cloudiness': item.get('clouds', {}).get('all'),
            'rain': item.get('rain', {}).get('3h', 0)
        })
    
    return jsonify({
        'city': forecast_data.get('city', {}).get('name'),
        'country': forecast_data.get('city', {}).get('country'),
        'forecast': forecasts
    })

@app.route('/weather/multiple', methods=['POST'])
def multiple_cities_weather():
    """Get current weather for multiple cities"""
    data = request.get_json()
    cities = data.get('cities', []) if data else []
    
    if not cities or not isinstance(cities, list):
        return jsonify({'error': 'Cities array is required'}), 400
    
    results = {}
    for city in cities:
        weather_data = get_current_weather(city)
        formatted = format_weather_response(weather_data)
        results[city] = formatted if formatted else {'error': 'City not found'}
    
    return jsonify(results)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'weather-dashboard'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
