"""메모리 지원을 갖춘 다중 에이전트 시스템의 에이전트 구현"""
import httpx
import json
from typing import Dict, Any, List
from strands import Agent
from mcp_tools import get_position, wikipedia_search
from model_config import get_configured_model


class WeatherForecastAgent:
    """좌표를 기반으로 날씨 예보를 제공하는 에이전트"""
    
    def __init__(self, model=None):
        self.model = model or get_configured_model()
        self.agent = Agent(
            model=self.model,
            system_prompt="""당신은 날씨 예보 에이전트입니다. 좌표가 주어지면 포괄적인 날씨 분석을 제공하세요.
            
작업:
1. 제공된 좌표 분석
2. 해당 위치의 현실적인 날씨 정보 생성
3. 현재 상황과 예보 제공
4. 사용자 친화적인 형식으로 응답 형식화

항상 날씨 상황에 대해 도움이 되고 정보를 제공하는 방식으로 응답하세요.""",
            tools=[]
        )
    
    def get_weather_forecast(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """LLM을 사용하여 주어진 좌표의 날씨 예보 가져오기"""
        try:
            print(f"  [*] 좌표 날씨 분석 중: {latitude}, {longitude}")
            
            # LLM이 날씨 정보를 생성하도록 프롬프트 생성
            prompt = f"""다음 좌표의 날씨 정보를 제공해주세요:
위도: {latitude}
경도: {longitude}

다음을 포함한 현실적인 날씨 데이터를 생성하세요:
1. 현재 날씨 상황 (온도, 습도, 설명, 풍속)
2. 최고/최저 온도와 설명이 포함된 3일 예보
3. 이 위치에 대한 관련 날씨 통찰력

포괄적인 날씨 보고서로 응답을 형식화하세요."""

            print("  [*] LLM으로 날씨 분석 생성 중...")
            # LLM을 사용하여 날씨 정보 생성
            response = self.agent(prompt)
            print("  [+] 날씨 분석 완료")
            
            # API 호환성을 위한 모의 구조화된 데이터
            weather_data = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "llm_analysis": response,
                "current": {
                    "temperature": 22.5,
                    "humidity": 65,
                    "description": "부분적으로 흐림",
                    "wind_speed": 12.3
                },
                "forecast": [
                    {"day": "오늘", "high": 25, "low": 18, "description": "맑음"},
                    {"day": "내일", "high": 23, "low": 16, "description": "흐림"},
                    {"day": "모레", "high": 27, "low": 20, "description": "맑음"}
                ]
            }
            
            return {
                "success": True,
                "agent": "weather_forecaster",
                "model_info": {
                    "provider": type(self.model).__name__,
                    "model_id": getattr(self.model, 'model_id', 'unknown')
                },
                "llm_response": response,
                "data": weather_data,
                "coordinates": {"latitude": latitude, "longitude": longitude}
            }
            
        except Exception as e:
            print(f"  [!] 날씨 에이전트 오류: {str(e)}")
            return {
                "success": False,
                "agent": "weather_forecaster",
                "error": f"날씨 예보 가져오기 오류: {str(e)}",
                "coordinates": {"latitude": latitude, "longitude": longitude}
            }


class SearchAgent:
    """위키피디아와 위치 도구를 사용하여 포괄적인 검색을 수행하는 에이전트"""
    
    def __init__(self, model=None):
        self.model = model or get_configured_model()
        self.agent = Agent(
            model=self.model,
            system_prompt="""당신은 포괄적인 검색 전문가입니다. 역할:

1. 사용 가능한 도구를 사용하여 모든 검색 쿼리에 대한 포괄적인 정보 수집
2. 관련되고 상세한 정보를 위한 위키피디아 검색
3. 해당하는 경우 위치의 정확한 좌표 가져오기
4. 수집된 정보 분석 및 종합
5. 포괄적인 검색 통찰력과 요약 제공

검색 쿼리를 처리할 때 사용 가능한 도구를 사용한 다음 발견한 내용에 대한 상세한 분석을 제공하세요. 연구에서 철저하고 가치 있는 통찰력을 제공하세요.""",
            tools=[get_position, wikipedia_search]
        )
    
    def search(self, query: str) -> Dict[str, Any]:
        """도구와 함께 LLM을 사용하여 포괄적인 검색 수행"""
        try:
            print(f"  [*] 포괄적 검색 시작: '{query}'")
            
            # LLM용 포괄적인 프롬프트 생성
            prompt = f"""다음에 대한 포괄적인 검색을 도와주세요: "{query}"

사용 가능한 도구를 사용하여:
1. 이 쿼리에 대한 위키피디아 정보 검색
2. 위치인 경우 정확한 좌표 (위도 및 경도) 가져오기
3. 수집한 정보 분석
4. 포괄적인 통찰력과 요약 제공

도구를 사용한 후 "{query}"에 대해 학습한 내용의 상세한 요약을 제공하세요."""

            print("  [*] 도구와 함께 LLM으로 검색 실행 중...")
            # 도구와 함께 LLM을 사용하여 검색 처리
            response = self.agent(prompt)
            print("  [+] 검색 분석 완료")
            
            print("  [*] 추가 도구 데이터 수집 중...")
            # 구조화된 데이터를 위한 원시 도구 결과도 가져오기
            wiki_result = wikipedia_search(query)
            
            # 위치처럼 보이면 위치 가져오기 시도
            position_result = None
            try:
                position_result = get_position(query)
                if position_result.get("success"):
                    print(f"  [*] 위치 좌표 발견: {position_result.get('latitude')}, {position_result.get('longitude')}")
                else:
                    print("  [*] 위치 좌표를 찾을 수 없음")
            except:
                position_result = {"success": False, "error": "위치 기반 쿼리가 아님"}
                print("  [*] 쿼리가 위치 기반이 아님")
            
            return {
                "success": True,
                "agent": "search",
                "model_info": {
                    "provider": type(self.model).__name__,
                    "model_id": getattr(self.model, 'model_id', 'unknown')
                },
                "query": query,
                "llm_response": response,
                "wikipedia_info": wiki_result,
                "position_info": position_result
            }
            
        except Exception as e:
            print(f"  [!] 검색 에이전트 오류: {str(e)}")
            return {
                "success": False,
                "agent": "search",
                "error": f"'{query}' 검색 수행 오류: {str(e)}",
                "query": query
            }


class ExtraAgent:
    """friendly hello and greeting , hello world같은 simple 에이전트"""
    
    def __init__(self, model=None):
        self.model = model or get_configured_model()
        self.agent = Agent(
            model=self.model,
            system_prompt="""당신은 친근한 보조 에이전트입니다. 호출될 때 다음을 해야 합니다:

1. 따뜻하고 도움이 되는 인사말 제공
2. 제공된 입력이나 문맥 인정
3. 지원이나 격려 제공
4. 간결하지만 친근하게

다른 에이전트들이 어려움을 겪었을 수 있을 때 긍정적인 상호작용을 제공하는 것이 역할입니다.""",
            tools=[]
        )
    
    def say_hello(self, message: str = "") -> Dict[str, Any]:
        """LLM을 사용하여 친근한 응답 생성"""
        try:
            print(f"  [*] 친근한 응답 생성 중: '{message}'")
            
            prompt = f"""친근한 인사말과 도움이 되는 응답을 제공해주세요. 
            
문맥: 사용자가 "{message}"에 대해 묻고 있었지만 다른 에이전트들이 정보 수집에 어려움을 겪었을 수 있습니다.

요청을 인정하고 친근한 방식으로 도움을 제공하겠다는 따뜻하고 격려적인 응답을 제공하세요."""

            print("  [*] LLM으로 친근한 응답 생성 중...")
            response = self.agent(prompt)
            print("  [+] 친근한 응답 생성됨")
            
            return {
                "success": True,
                "agent": "extra",
                "model_info": {
                    "provider": type(self.model).__name__,
                    "model_id": getattr(self.model, 'model_id', 'unknown')
                },
                "llm_response": response,
                "message": "hello",
                "input_message": message,
                "note": "추가 에이전트의 친근한 응답입니다"
            }
            
        except Exception as e:
            print(f"  [!] 추가 에이전트 오류: {str(e)}")
            return {
                "success": False,
                "agent": "extra",
                "error": f"인사말 생성 오류: {str(e)}",
                "input_message": message
            }
