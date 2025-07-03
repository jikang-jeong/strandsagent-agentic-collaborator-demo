"""MCP Tools for the multi-agent system"""
import httpx
import wikipedia
import asyncio
import json
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
                    headers={
                        "User-Agent": "StrandsAgents/1.0",
                        "Accept": "application/json",
                        "Accept-Charset": "utf-8"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    # UTF-8 디코딩 안전 처리
                    try:
                        data = response.json()
                    except UnicodeDecodeError:
                        content = response.content.decode('utf-8', errors='ignore')
                        data = json.loads(content)
                    
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
    """Search Wikipedia for comprehensive encyclopedic information
    
    BEST FOR:
    - Historical facts, biographical information, scientific concepts
    - Academic and educational content with citations
    - Detailed explanations of established topics
    - Geographic locations, countries, cities
    - Well-documented subjects with authoritative sources
    
    NOT SUITABLE FOR:
    - Real-time information, current events, breaking news
    - Personal opinions, reviews, or subjective content
    - Very recent developments (less than few months old)
    - Trending topics or social media content
    
    Args:
        query: The search query for Wikipedia (use specific, well-known terms)
        
    Returns:
        Dictionary containing comprehensive Wikipedia information with summary and URL
    """
    try:
        # Set language to English
        wikipedia.set_lang("en")
        
        # Search for the query with UTF-8 safe handling
        try:
            search_results = wikipedia.search(query, results=3)
        except UnicodeDecodeError:
            # Retry with ASCII-safe query
            safe_query = query.encode('ascii', errors='ignore').decode('ascii')
            search_results = wikipedia.search(safe_query, results=3)
        
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
        except UnicodeDecodeError:
            return {
                "success": False,
                "error": f"Text encoding issue with Wikipedia page for '{query}'",
                "query": query
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching Wikipedia for '{query}': {str(e)}",
            "query": query
        }


@tool
def duckduckgo_search(query: str) -> Dict[str, Any]:
    """Search DuckDuckGo for real-time web information and instant answers
    
    BEST FOR:
    - Quick definitions and explanations of terms
    - Current trends, recent developments, news-related queries
    - Programming concepts, technical definitions
    - Simple factual questions requiring instant answers
    - Topics that might not have detailed Wikipedia coverage
    - Modern technology, software, apps, recent innovations
    
    NOT SUITABLE FOR:
    - Deep historical analysis or comprehensive academic content
    - Complex topics requiring extensive citations
    - Queries better served by encyclopedic sources
    
    COMPLEMENTARY USE:
    - Use AFTER Wikipedia if Wikipedia results are insufficient
    - Use FIRST for modern/technical topics or quick definitions
    
    Args:
        query: The search query for DuckDuckGo (use clear, specific terms)
        
    Returns:
        Dictionary containing instant answers, definitions, and web information
    """
    try:
        async def fetch_search_results():
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.duckduckgo.com/",
                    params={
                        "q": query,
                        "format": "json",
                        "no_html": "1",
                        "skip_disambig": "1"
                    },
                    headers={
                        "User-Agent": "StrandsAgents/1.0",
                        "Accept": "application/json",
                        "Accept-Charset": "utf-8"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    # UTF-8 디코딩 안전 처리
                    try:
                        data = response.json()
                    except UnicodeDecodeError:
                        content = response.content.decode('utf-8', errors='ignore')
                        data = json.loads(content)
                    except json.JSONDecodeError:
                        return {
                            "success": False,
                            "error": f"Invalid JSON response from DuckDuckGo for '{query}'",
                            "query": query
                        }
                    
                    # Abstract (요약 정보)
                    abstract = data.get("Abstract", "")
                    abstract_source = data.get("AbstractSource", "")
                    abstract_url = data.get("AbstractURL", "")
                    
                    # Related Topics
                    related_topics = data.get("RelatedTopics", [])
                    
                    # Answer (즉석 답변)
                    answer = data.get("Answer", "")
                    answer_type = data.get("AnswerType", "")
                    
                    # Definition
                    definition = data.get("Definition", "")
                    definition_source = data.get("DefinitionSource", "")
                    
                    # 유용한 정보가 있는지 확인
                    has_content = any([abstract, answer, definition, related_topics])
                    
                    if has_content:
                        return {
                            "success": True,
                            "query": query,
                            "abstract": abstract,
                            "abstract_source": abstract_source,
                            "abstract_url": abstract_url,
                            "answer": answer,
                            "answer_type": answer_type,
                            "definition": definition,
                            "definition_source": definition_source,
                            "related_topics": [
                                {
                                    "text": topic.get("Text", ""),
                                    "url": topic.get("FirstURL", "")
                                }
                                for topic in related_topics[:3]  # 상위 3개만
                                if topic.get("Text")
                            ],
                            "source": "DuckDuckGo"
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"No useful information found for '{query}' on DuckDuckGo",
                            "query": query
                        }
                
                return {
                    "success": False,
                    "error": f"DuckDuckGo API request failed with status {response.status_code}",
                    "query": query
                }
        
        # 비동기 실행
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(fetch_search_results())
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching DuckDuckGo for '{query}': {str(e)}",
            "query": query
        }

