"""워크샵용 간단한 에이전트 계획 시스템"""
from typing import Dict, Any, List, Optional
from strands import Agent
from model_config import get_configured_model
import json


class AgentPlanner:
    """워크샵 데모용 간단한 에이전트 계획자"""
    
    def __init__(self, model=None):
        self.model = model or get_configured_model()
        self.agent = Agent(
            model=self.model,
            system_prompt="""당신은 지능적인 에이전트 계획자입니다. 사용자 요청을 분석하고 실행할 에이전트를 결정하세요.

사용 가능한 에이전트:
1. SEARCH_AGENT: 위키피디아 검색 및 위치 좌표 조회
2. WEATHER_AGENT: 날씨 예보 
3. EXTRA_AGENT: 친근한 인사말

규칙:
- 날씨 쿼리: SEARCH_AGENT 먼저 실행 (좌표 획득용), 그 다음 WEATHER_AGENT
- 위치/일반 쿼리: SEARCH_AGENT만 사용
- 인사말: EXTRA_AGENT만 사용

응답 형식 (JSON만):
{
    "agents_to_execute": ["agent1", "agent2"],
    "reasoning": "간단한 설명"
}

에이전트 이름: "search", "weather", "extra"
""",
            tools=[]
        )
    
    def create_execution_plan(self, user_input: str) -> Dict[str, Any]:
        """간단한 실행 계획 생성"""
        try:
            print("[*] 실행 계획 생성 중...")
            
            prompt = f"""분석: "{user_input}"

실행할 에이전트를 결정하세요. JSON만 반환하세요."""

            response = self.agent(prompt)
            plan = self._extract_json_from_response(response)
            
            if plan and "agents_to_execute" in plan:
                print(f"[*] 계획: {plan.get('agents_to_execute', [])}")
                return {
                    "success": True,
                    "plan": plan
                }
            else:
                # 간단한 기본값: 검색만 사용
                print("[*] 기본값 사용: 검색 에이전트")
                return {
                    "success": True,
                    "plan": {
                        "agents_to_execute": ["search"],
                        "reasoning": "기본 검색 에이전트"
                    }
                }
                
        except Exception as e:
            print(f"[!] 계획 오류: {str(e)}")
            # 간단한 기본값: 검색만 사용
            return {
                "success": True,
                "plan": {
                    "agents_to_execute": ["search"],
                    "reasoning": "오류 대체 - 검색 사용"
                }
            }
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """응답에서 JSON 추출"""
        try:
            if hasattr(response, '__str__'):
                response = str(response)
            
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass
        return None
