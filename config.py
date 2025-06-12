"""Configuration settings for the multi-agent system"""

# API Configuration
OPENWEATHER_API_KEY = "your_openweather_api_key_here"  # Replace with actual API key
NOMINATIM_USER_AGENT = "StrandsAgents/1.0"

# Agent Configuration
WEATHER_AGENT_CONFIG = {
    "name": "weather_forecaster",
    "timeout": 30,
    "max_retries": 3
}

HELLO_WORLD_AGENT_CONFIG = {
    "name": "hello_world",
    "timeout": 30,
    "max_retries": 3
}

EXTRA_AGENT_CONFIG = {
    "name": "extra",
    "timeout": 10,
    "max_retries": 1
}

SUPER_AGENT_CONFIG = {
    "name": "super_agent",
    "timeout": 60,
    "max_retries": 2
}

# Response Format Configuration
RESPONSE_FORMAT = {
    "version": "1.0",
    "format": "json",
    "include_metadata": True,
    "include_timestamps": True
}
