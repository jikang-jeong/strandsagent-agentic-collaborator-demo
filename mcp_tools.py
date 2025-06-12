"""MCP Tools for the multi-agent system"""
import httpx
import wikipedia
from typing import Dict, Any
from strands import tool


@tool
def get_position(location: str) -> Dict[str, Any]:
    """Get latitude and longitude coordinates for a given location name
    
    Args:
        location: The name of the location to get coordinates for
        
    Returns:
        Dictionary containing coordinates and location information
    """
    try:
        # Using OpenStreetMap Nominatim API for geocoding
        import httpx
        import asyncio
        
        async def fetch_coordinates():
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={
                        "q": location,
                        "format": "json",
                        "limit": 1
                    },
                    headers={"User-Agent": "StrandsAgents/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        result = data[0]
                        return {
                            "success": True,
                            "location": location,
                            "latitude": float(result["lat"]),
                            "longitude": float(result["lon"]),
                            "display_name": result.get("display_name", location)
                        }
                
                return {
                    "success": False,
                    "error": f"Location '{location}' not found",
                    "location": location
                }
        
        # Run async function
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(fetch_coordinates())
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting position for {location}: {str(e)}",
            "location": location
        }


@tool
def wikipedia_search(query: str) -> Dict[str, Any]:
    """Search Wikipedia for information about a location or topic
    
    Args:
        query: The search query for Wikipedia
        
    Returns:
        Dictionary containing Wikipedia search results and information
    """
    try:
        # Set language to English
        wikipedia.set_lang("en")
        
        # Search for the query
        search_results = wikipedia.search(query, results=3)
        
        if not search_results:
            return {
                "success": False,
                "error": f"No Wikipedia results found for '{query}'",
                "query": query
            }
        
        # Get the first result's summary
        page_title = search_results[0]
        try:
            page = wikipedia.page(page_title)
            summary = wikipedia.summary(page_title, sentences=3)
            
            return {
                "success": True,
                "query": query,
                "title": page.title,
                "summary": summary,
                "url": page.url,
                "search_results": search_results
            }
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation by taking the first option
            page = wikipedia.page(e.options[0])
            summary = wikipedia.summary(e.options[0], sentences=3)
            
            return {
                "success": True,
                "query": query,
                "title": page.title,
                "summary": summary,
                "url": page.url,
                "search_results": search_results,
                "note": "Disambiguation resolved automatically"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching Wikipedia for '{query}': {str(e)}",
            "query": query
        }
