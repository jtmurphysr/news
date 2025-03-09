import os
from datetime import datetime
from typing import List, Dict, Any
import requests
from feed_parser import FeedParser, FeedEntry

class WeatherParser(FeedParser):
    """Parser for OpenWeather API data"""
    
    def __init__(self, api_key: str, lat: float = 40.489632, lon: float = -111.940018):
        super().__init__("Weather Forecast")
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
    
    def extract_weather_data(self, weather_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key weather information from the OpenWeather API response."""
        # Extract location info
        location = {
            "lat": weather_json.get("lat"),
            "lon": weather_json.get("lon"),
            "timezone": weather_json.get("timezone")
        }

        # Extract current weather
        current = weather_json.get("current", {})
        current_weather = {
            "timestamp": datetime.fromtimestamp(current.get("dt", 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "sunrise": datetime.fromtimestamp(current.get("sunrise", 0)).strftime("%H:%M"),
            "sunset": datetime.fromtimestamp(current.get("sunset", 0)).strftime("%H:%M"),
            "temp": current.get("temp"),
            "feels_like": current.get("feels_like"),
            "pressure": current.get("pressure"),
            "humidity": current.get("humidity"),
            "wind_speed": current.get("wind_speed"),
            "wind_deg": current.get("wind_deg"),
            "description": current.get("weather", [{}])[0].get("description", ""),
            "main": current.get("weather", [{}])[0].get("main", "")
        }

        # Extract daily forecast
        daily_forecast = []
        for day in weather_json.get("daily", []):
            daily_data = {
                "date": datetime.fromtimestamp(day.get("dt", 0)).strftime("%Y-%m-%d"),
                "summary": day.get("summary", ""),
                "temp_day": day.get("temp", {}).get("day"),
                "temp_min": day.get("temp", {}).get("min"),
                "temp_max": day.get("temp", {}).get("max"),
                "humidity": day.get("humidity"),
                "description": day.get("weather", [{}])[0].get("description", ""),
                "main": day.get("weather", [{}])[0].get("main", ""),
                "rain": day.get("rain", 0),
                "snow": day.get("snow", 0),
                "pop": day.get("pop", 0)
            }
            daily_forecast.append(daily_data)

        # Extract hourly forecast (next 24 hours)
        hourly_forecast = []
        for hour in weather_json.get("hourly", [])[:24]:
            hourly_data = {
                "timestamp": datetime.fromtimestamp(hour.get("dt", 0)).strftime("%Y-%m-%d %H:%M"),
                "temp": hour.get("temp"),
                "feels_like": hour.get("feels_like"),
                "humidity": hour.get("humidity"),
                "description": hour.get("weather", [{}])[0].get("description", ""),
                "pop": hour.get("pop", 0)
            }
            hourly_forecast.append(hourly_data)

        return {
            "location": location,
            "current": current_weather,
            "daily_forecast": daily_forecast,
            "hourly_forecast": hourly_forecast
        }

    def format_current_weather(self, current: Dict[str, Any]) -> str:
        """Format current weather as HTML content"""
        return f"""
        <div class="weather-current">
            <p><strong>Current Conditions:</strong> {current['main']} - {current['description']}</p>
            <p>Temperature: {current['temp']}°F (Feels like: {current['feels_like']}°F)</p>
            <p>Wind: {current['wind_speed']} mph</p>
            <p>Humidity: {current['humidity']}%</p>
            <p>Sunrise: {current['sunrise']}, Sunset: {current['sunset']}</p>
        </div>
        """

    def format_daily_forecast(self, daily: List[Dict[str, Any]]) -> str:
        """Format daily forecast as HTML content"""
        forecast_html = []
        for day in daily[:5]:  # Next 5 days
            day_name = datetime.strptime(day['date'], "%Y-%m-%d").strftime("%A")
            
            precip_info = []
            if day['pop'] > 0:
                precip_info.append(f"Chance of precipitation: {int(day['pop'] * 100)}%")
            if day['rain'] > 0:
                precip_info.append(f"Rain: {day['rain']}mm")
            if day['snow'] > 0:
                precip_info.append(f"Snow: {day['snow']}mm")

            forecast_html.append(f"""
            <div class="weather-day">
                <h3>{day_name}</h3>
                <p>{day['main']}: {day['description']}</p>
                <p>High: {day['temp_max']}°F, Low: {day['temp_min']}°F</p>
                {f"<p>{', '.join(precip_info)}</p>" if precip_info else ""}
            </div>
            """)
        
        return "\n".join(forecast_html)

    def parse(self) -> List[FeedEntry]:
        """Fetch and parse weather data from OpenWeather API"""
        entries = []
        try:
            # Fetch weather data
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "imperial"
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            weather_json = response.json()
            
            # Process weather data
            weather_data = self.extract_weather_data(weather_json)
            
            # Create current conditions entry
            current = weather_data['current']
            current_content = self.format_current_weather(current)
            entries.append(FeedEntry(
                title="Current Weather Conditions",
                content=current_content,
                published=current['timestamp'],
                source="OpenWeather",
                category="Weather"
            ))
            
            # Create forecast entry
            forecast_content = self.format_daily_forecast(weather_data['daily_forecast'])
            entries.append(FeedEntry(
                title="5-Day Weather Forecast",
                content=forecast_content,
                published=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                source="OpenWeather",
                category="Weather"
            ))
            
        except Exception as e:
            print(f"Error fetching weather data: {str(e)}")
        
        return entries 