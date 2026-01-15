# aiccel/tools_unified/builtin.py
"""
Built-in Tools
===============

Ready-to-use tools for common tasks.
"""

import requests
from typing import Dict, Any, List, Optional
from urllib.parse import quote_plus

from .base import BaseTool
from .protocol import ToolParameter


class SearchTool(BaseTool):
    """
    Web search tool using Serper API.
    
    Usage:
        tool = SearchTool(api_key="your-api-key")
        result = tool.execute(query="Python tutorials")
    """
    
    _name = "search"
    _description = "Search the web for current information on any topic"
    _parameters = [
        ToolParameter(
            name="query",
            type="string",
            description="Search query",
            required=True
        ),
        ToolParameter(
            name="num_results",
            type="integer",
            description="Number of results to return (1-10)",
            required=False,
            default=5
        )
    ]
    _tags = ["search", "web", "information"]
    
    def __init__(self, api_key: str, timeout: int = 15):
        super().__init__()
        self.api_key = api_key
        self.timeout = timeout
        self._endpoint = "https://google.serper.dev/search"
    
    def execute(self, query: str, num_results: int = 5, **kwargs) -> str:
        """
        Execute web search.
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            Formatted search results
        """
        if not query:
            return "Error: No search query provided"
        
        try:
            response = requests.post(
                self._endpoint,
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json"
                },
                json={"q": query, "num": min(num_results, 10)},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return self._format_results(data)
            
        except requests.RequestException as e:
            return f"Search failed: {str(e)}"
    
    def _format_results(self, data: Dict[str, Any]) -> str:
        """Format search results."""
        results = []
        
        # Organic results
        for item in data.get("organic", [])[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            
            results.append(f"**{title}**\n{snippet}\nURL: {link}")
        
        # Answer box if available
        if "answerBox" in data:
            answer = data["answerBox"]
            if "answer" in answer:
                results.insert(0, f"**Quick Answer:** {answer['answer']}")
            elif "snippet" in answer:
                results.insert(0, f"**Quick Answer:** {answer['snippet']}")
        
        if not results:
            return "No results found"
        
        return "\n\n".join(results)


class WeatherTool(BaseTool):
    """
    Weather information tool using OpenWeatherMap API.
    
    Usage:
        tool = WeatherTool(api_key="your-api-key")
        result = tool.execute(location="London")
    """
    
    _name = "get_weather"
    _description = "Get current weather and forecast for a location"
    _parameters = [
        ToolParameter(
            name="location",
            type="string",
            description="City name or location",
            required=True
        ),
        ToolParameter(
            name="units",
            type="string",
            description="Temperature units",
            required=False,
            default="imperial",
            enum=["metric", "imperial"]
        )
    ]
    _tags = ["weather", "forecast", "temperature"]
    
    def __init__(self, api_key: str, timeout: int = 15):
        super().__init__()
        self.api_key = api_key
        self.timeout = timeout
        self._base_url = "https://api.openweathermap.org/data/2.5"
    
    def execute(self, location: str, units: str = "imperial", **kwargs) -> str:
        """
        Get weather for a location.
        
        Args:
            location: City name
            units: Temperature units (metric/imperial)
            
        Returns:
            Formatted weather information
        """
        if not location:
            return "Error: No location provided"
        
        try:
            # Current weather
            current = self._get_current_weather(location, units)
            
            # Forecast
            forecast = self._get_forecast(location, units)
            
            return self._format_weather(current, forecast, units)
            
        except requests.RequestException as e:
            return f"Weather lookup failed: {str(e)}"
    
    def _get_current_weather(self, location: str, units: str) -> Dict:
        """Get current weather."""
        url = f"{self._base_url}/weather"
        response = requests.get(
            url,
            params={
                "q": location,
                "appid": self.api_key,
                "units": units
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def _get_forecast(self, location: str, units: str) -> Dict:
        """Get weather forecast."""
        url = f"{self._base_url}/forecast"
        response = requests.get(
            url,
            params={
                "q": location,
                "appid": self.api_key,
                "units": units,
                "cnt": 8  # Next 24 hours (3-hour intervals)
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def _format_weather(self, current: Dict, forecast: Dict, units: str) -> str:
        """Format weather data."""
        temp_unit = "°F" if units == "imperial" else "°C"
        
        # Current conditions
        main = current.get("main", {})
        weather = current.get("weather", [{}])[0]
        
        result = [
            f"**Current Weather in {current.get('name', 'Unknown')}:**",
            f"- Temperature: {main.get('temp', 'N/A')}{temp_unit} (feels like {main.get('feels_like', 'N/A')}{temp_unit})",
            f"- Conditions: {weather.get('description', 'N/A').title()}",
            f"- Humidity: {main.get('humidity', 'N/A')}%",
            f"- Wind: {current.get('wind', {}).get('speed', 'N/A')} {'mph' if units == 'imperial' else 'm/s'}",
        ]
        
        # Forecast
        if forecast.get("list"):
            result.append("\n**Forecast:**")
            for item in forecast["list"][:3]:
                time = item.get("dt_txt", "").split(" ")[1][:5]
                temp = item.get("main", {}).get("temp", "N/A")
                desc = item.get("weather", [{}])[0].get("description", "")
                result.append(f"- {time}: {temp}{temp_unit}, {desc}")
        
        return "\n".join(result)


# Backward compatibility aliases
Tool = BaseTool
