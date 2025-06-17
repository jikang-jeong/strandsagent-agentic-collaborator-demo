"""Agents as Tools 패턴을 위한 전문 에이전트들"""
from strands import Agent, tool
from strands_tools import mem0_memory, use_llm, http_request
from mcp_tools import get_position, wikipedia_search
from model_config import get_configured_model
from memory_manager import MemoryManager
import json
from typing import Dict, Any


# Search Agent - Wikipedia 검색 전문
SEARCH_AGENT_PROMPT = """
당신은 Wikipedia 검색 전문 에이전트입니다.
사용자의 검색 요청에 대해 Wikipedia API를 사용하여 정확하고 포괄적인 정보를 제공합니다.
검색 결과를 분석하고 사용자가 이해하기 쉽게 요약해서 답변하세요.
"""

@tool
def search_agent(query: str) -> str:
    """
    Wikipedia 검색을 통해 정보를 제공하는 전문 에이전트
    
    Args:
        query: 검색할 내용
        
    Returns:
        Wikipedia 검색 결과를 바탕으로 한 포괄적인 답변
    """
    try:
        agent = Agent(
            model=get_configured_model(),
            system_prompt=SEARCH_AGENT_PROMPT,
            tools=[wikipedia_search]
        )
        
        search_prompt = f"""
        다음 검색 요청에 대해 Wikipedia를 검색하고 포괄적인 답변을 제공하세요: "{query}"
        
        검색 후 결과를 분석하여 사용자가 이해하기 쉽게 요약해주세요.
        """
        
        response = agent(search_prompt)
        return str(response)
        
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"


# Weather Agent - 날씨 정보 전문
WEATHER_AGENT_PROMPT = """
당신은 날씨 정보 전문 에이전트입니다.
사용자가 특정 지역의 날씨를 요청하면, 먼저 해당 지역의 좌표를 찾고
National Weather Service API를 사용하여 날씨 정보를 제공합니다.
미국 지역만 지원됩니다.
"""

@tool
def weather_agent(location_query: str) -> str:
    """
    특정 지역의 날씨 정보를 제공하는 전문 에이전트
    
    Args:
        location_query: 날씨를 알고 싶은 지역
        
    Returns:
        해당 지역의 날씨 정보
    """
    try:
        agent = Agent(
            model=get_configured_model(),
            system_prompt=WEATHER_AGENT_PROMPT,
            tools=[get_position, http_request]
        )
        
        weather_prompt = f"""
        "{location_query}" 지역의 날씨 정보를 제공해주세요.
        
        단계:
        1. 먼저 지역의 정확한 좌표(위도, 경도)를 찾으세요
        2. 좌표가 미국 지역인지 확인하세요 (위도: 24-49, 경도: -125 ~ -66)
        3. 미국 지역이면 National Weather Service API를 사용하여 날씨 정보를 가져오세요
           - https://api.weather.gov/points/위도,경도 호출
           - 응답에서 forecast URL 추출
           - forecast URL 호출하여 날씨 예보 가져오기
        4. 미국 외 지역이면 "미국 지역만 지원합니다"라고 안내하세요
        
        사용자 친화적인 날씨 보고서를 제공해주세요.
        """
        
        response = agent(weather_prompt)
        return str(response)
        
    except Exception as e:
        return f"날씨 정보 조회 중 오류가 발생했습니다: {str(e)}"


# Conversation Agent - 일반 대화 전문
CONVERSATION_AGENT_PROMPT = """
당신은 친근하고 도움이 되는 대화 전문 에이전트입니다.
검색이나 날씨가 아닌 일반적인 대화, 인사, 질문에 대해 자연스럽고 유용한 답변을 제공합니다.
사용자와 친근한 대화를 나누며 필요시 조언이나 정보를 제공하세요.
"""

@tool
def conversation_agent(message: str) -> str:
    """
    일반적인 대화와 질문에 응답하는 전문 에이전트
    
    Args:
        message: 사용자의 메시지나 질문
        
    Returns:
        요청에 응답의 양식이 있다면 요청응답에 따르며, 없다면 도움이 되는 답변.
    """
    try:
        agent = Agent(
            model=get_configured_model(),
            system_prompt=CONVERSATION_AGENT_PROMPT,
            tools=[]
        )
        
        conversation_prompt = f"""
        사용자가 다음과 같이 입력하였습니다: "{message}" 
        """
        
        response = agent(conversation_prompt)
        return str(response)
        
    except Exception as e:
        return f"대화 처리 중 오류가 발생했습니다: {str(e)}"


# Memory Agent - 메모리 관리 전문
MEMORY_AGENT_PROMPT = """
당신은 사용자의 대화 기록을 관리하는 메모리 전문 에이전트입니다.
사용자의 요청에 따라 메모리를 저장, 검색, 요약하는 역할을 담당합니다.
"""

@tool
def memory_agent(action: str, content: str = "", user_id: str = "workshop_user") -> str:
    """
    메모리 관리를 담당하는 전문 에이전트
    
    Args:
        action: 수행할 작업 (store, retrieve, clear)
        content: 저장할 내용 (store 시에만 필요)
        user_id: 사용자 ID
        
    Returns:
        메모리 작업 결과
    """
    try:
        memory_manager = MemoryManager("workshop_user")

        if action == "store":
            if not content:
                return "저장할 내용이 필요합니다."
            
            success = memory_manager.store_memory(content)
            if success:
                return "메모리에 성공적으로 저장되었습니다."
            else:
                return "메모리 저장에 실패했습니다."
                
        elif action == "retrieve":
            memory_summary = memory_manager.get_relevant_memory()
            if memory_summary:
                return f"저장된 기록: {memory_summary}"
            else:
                return "저장된 기록이 없습니다."
                
        elif action == "clear":
            deleted_count = memory_manager.clear_all_memories()
            return f"{deleted_count}개의 메모리가 삭제되었습니다."
            
        else:
            return "지원하지 않는 작업입니다. (store, retrieve, clear 중 선택)"
            
    except Exception as e:
        return f"메모리 작업 중 오류가 발생했습니다: {str(e)}"
