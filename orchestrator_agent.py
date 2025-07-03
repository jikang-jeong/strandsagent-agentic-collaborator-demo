"""Orchestrator Agent - Agents as Tools 패턴의 오케스트레이터"""
from strands import Agent
from sub_agents import search_agent, weather_agent, conversation_agent
from model_config import get_configured_model
from typing import Dict, Any


class OrchestratorAgent:
    """
    Agents as Tools 패턴의 오케스트레이터 에이전트
    사용자 요청을 분석하고 적절한 하위 에이전트에게 작업을 위임
    """

    def __init__(self, model=None, user_id: str = "default_user"):
        self.model = model or get_configured_model()
        self.user_id = user_id
        self.model_available = True

        # 모델 가용성 테스트
        try:
            test_agent = Agent(
                model=self.model,
                system_prompt="Test",
                tools=[]
            )
            test_agent("Hello")
        except Exception as e:
            self.model_available = False
            print(f"⚠️ 모델 접근 제한: 기본 기능으로 동작합니다.")

        # 오케스트레이터 에이전트 생성
        if self.model_available:
            self.orchestrator = Agent(
                model=self.model,
                system_prompt=f"""당신은 사용자 요청을 분석하고 적절한 하위 에이전트에게 작업을 위임하는 오케스트레이터입니다.
사용자 ID: {user_id}

사용 가능한 하위 에이전트들을 적절히 사용하여 사용자 요청에 응답하세요.
각 에이전트의 설명을 참고하여 언제, 어떻게 사용할지 스스로 판단하세요.""",
                tools=[search_agent, weather_agent, conversation_agent]
            )
        else:
            self.orchestrator = None

        print(f"Orchestrator Agent 초기화 완료 (사용자: {user_id})")
        print(f"사용 모델: {type(self.model).__name__}")
        if not self.model_available:
            print("📝 참고: 일부 고급 기능이 제한될 수 있습니다.")

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        사용자 입력을 처리하고 적절한 하위 에이전트에게 위임

        Args:
            user_input: 사용자 입력

        Returns:
            처리 결과
        """
        try:
            # 모델이 사용 불가능한 경우 간단한 처리
            if not self.model_available:
                return {
                    "success": True,
                    "agent": "fallback",
                    "user_input": user_input,
                    "response": f"현재 AI 모델에 접근할 수 없습니다. '{user_input}' 요청을 처리하려면 모델 설정을 확인해주세요.",
                    "needs_clarification": False,
                    "user_id": self.user_id
                }
            
            # 명확성 판단
            clarity_agent = Agent(
                model=self.model,
                system_prompt="""당신은 사용자 요청의 명확성만 판단하는 전문가입니다.

판단 기준:
- 매우 모호한 경우만 "NEED_MORE"로 응답 (예: "커피", "음식" 같은 단일 키워드)
- 대부분의 경우는 "PROCEED"로 응답 (예: "ice coffee", "파리", "날씨 정보" 등)

응답 형식: "NEED_MORE" 또는 "PROCEED"만 출력하세요.""",
                tools=[]
            )
            
            clarity_prompt = f"""
            사용자 요청: "{user_input}"
            
            사용자 요청이 추가 정보 없이 처리 가능한지 판단하세요.
            응답 형식: "NEED_MORE" 또는 "PROCEED"만 출력
            """
            
            clarity_response = clarity_agent(clarity_prompt)
            clarity_result = str(clarity_response).strip()

            
            # 매우 모호한 경우만 질문
            if "NEED_MORE" in clarity_result:
                # 사용자에게 명확화 질문
                clarification_response = conversation_agent(f"""
                사용자가 "{user_input}"라고 입력했습니다.
                이 요청은 모호하여 추가 정보가 필요합니다.
                
                사용자에게 어떤 정보를 원하는지 구체적으로 물어보세요.
                예를 들어:
                - "ice coffee"라면 → 레시피를 원하는지, 브랜드 추천을 원하는지, 일반 정보를 원하는지
                - "날씨"라면 → 어느 지역의 날씨인지
                - "음식"이라면 → 어떤 음식에 대한 정보인지
                
                간단한 질문으로 응답하세요.
                """)
                
                return {
                    "success": True,
                    "agent": "orchestrator_agent",
                    "user_input": user_input,
                    "response": str(clarification_response),
                    "needs_clarification": True,
                    "user_id": self.user_id
                }

            # 요청이 명확한 경우 - 실행 계획 수립
            planning_agent = Agent(
                model=self.model,
                system_prompt="""당신은 실행 계획만 수립하는 전문가입니다.
도구를 사용하지 말고, 오직 계획만 세우세요.

사용 가능한 하위 에이전트들:
- search_agent: Wikipedia 및 DuckDuckGo 검색이 필요한 정보 요청
- weather_agent: 날씨 정보 요청 (미국 지역만 지원)  
- conversation_agent: 일반 대화, 인사, 간단한 질문
""",
                tools=[]
            )

            planning_prompt = f"""
            사용자 요청: "{user_input}"
            
            이 요청을 처리하기 위한 실행 계획을 다음 형식으로 작성하세요:
            
            **📋 실행 계획:**
            1. [하위 에이전트명] - [사용 이유와 목적]
            2. [하위 에이전트명] - [사용 이유와 목적]
            ...
            
            **🎯 예상 결과:**
            [어떤 최종 결과를 사용자에게 제공할 예정인지]
            
            **⚠️ 주의사항:**
            [특별히 고려해야 할 사항이 있다면]
            """

            plan_response = planning_agent(planning_prompt)
            plan_text = str(plan_response)
            
            print("\n📋 ORCHESTRATOR AGENT 실행 계획")
            print("="*60)
            print(plan_text)
            print("="*60)

            # 계획에 따라 실제 하위 에이전트들 실행
            execution_prompt = f"""
            다음은 앞서 수립한 실행 계획입니다:
            
            {plan_text}
            
            이제 이 계획에 따라 실제로 하위 에이전트들을 사용하여 사용자 요청을 처리하세요:
            
            사용자 요청: "{user_input}"
            
            계획에 따라 순차적으로 하위 에이전트들을 실행하고, 최종적으로 사용자에게 도움이 되는 종합적인 답변을 제공하세요.
            """

            response = self.orchestrator(execution_prompt)
            
            # <thinking> 태그 제거
            import re
            clean_response = re.sub(r'<thinking>.*?</thinking>', '', str(response), flags=re.DOTALL)
            clean_response = clean_response.strip()

            return {
                "success": True,
                "agent": "orchestrator_agent",
                "user_input": user_input,
                "execution_plan": plan_text,
                "response": clean_response,
                "needs_clarification": False,
                "user_id": self.user_id
            }

        except Exception as e:
            # 간단한 오류 처리
            return {
                "success": False,
                "agent": "orchestrator_agent",
                "error": f"요청 처리 중 오류가 발생했습니다: {str(e)}",
                "user_input": user_input
            }

    def get_agent_status(self) -> Dict[str, Any]:
        """에이전트 상태 정보 반환"""
        return {
            "orchestrator_agent": "활성",
            "model": type(self.model).__name__,
            "user_id": self.user_id,
            "available_sub_agents": [
                "search_agent (Wikipedia 및 DuckDuckGo 검색)",
                "weather_agent (날씨 정보)",
                "conversation_agent (일반 대화)"
            ]
        }
