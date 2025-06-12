"""Test script for the multi-agent system"""
import json
from main import MultiAgentApplication


def test_single_location():
    """Test with a single location"""
    app = MultiAgentApplication()
    
    test_locations = [
        "Seoul",
        "New York",
        "London",
        "Tokyo",
        "InvalidLocationName123"
    ]
    
    for location in test_locations:
        print(f"\n🧪 Testing location: {location}")
        print("=" * 50)
        
        try:
            result = app.run_single_query(location)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ Error testing {location}: {str(e)}")
        
        print("\n" + "=" * 50)


def test_individual_components():
    """Test individual components"""
    from agents import WeatherForecastAgent, HelloWorldAgent, ExtraAgent
    from mcp_tools import get_position, wikipedia_search
    
    print("\n🧪 Testing Individual Components")
    print("=" * 50)
    
    # Test MCP Tools
    print("\n📍 Testing Position Tool:")
    position_result = get_position("Seoul")
    print(json.dumps(position_result, indent=2))
    
    print("\n📚 Testing Wikipedia Tool:")
    wiki_result = wikipedia_search("Seoul")
    print(json.dumps(wiki_result, indent=2))
    
    # Test Individual Agents
    print("\n🌤️ Testing Weather Agent:")
    weather_agent = WeatherForecastAgent()
    weather_result = weather_agent.get_weather_forecast(37.5665, 126.9780)  # Seoul coordinates
    print(json.dumps(weather_result, indent=2))
    
    print("\n👋 Testing Hello World Agent:")
    hello_agent = HelloWorldAgent()
    hello_result = hello_agent.process_location("Seoul")
    print(json.dumps(hello_result, indent=2))
    
    print("\n✨ Testing Extra Agent:")
    extra_agent = ExtraAgent()
    extra_result = extra_agent.say_hello("test message")
    print(json.dumps(extra_result, indent=2))


def main():
    """Main test function"""
    print("🧪 Starting Multi-Agent System Tests")
    print("=" * 50)
    
    # Test individual components
    test_individual_components()
    
    # Test full system
    test_single_location()


if __name__ == "__main__":
    main()
