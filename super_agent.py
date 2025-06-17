"""Super Agent - Agents as Tools 패턴의 오케스트레이터"""
from strands import Agent
from specialized_agents import search_agent, weather_agent, conversation_agent, memory_agent
from model_config import get_configured_model
from memory_manager import MemoryManager
import os
from typing import Dict, Any


class SuperAgent:
    """
    Agents as Tools 패턴의 오케스트레이터 에이전트
    사용자 요청을 분석하고 적절한 전문 에이전트에게 작업을 위임
    """

    def __init__(self, model=None, user_id: str = "default_user"):
        self.model = model or get_configured_model()
        self.user_id = user_id

        # 오케스트레이터 에이전트 생성 - 간결한 시스템 프롬프트
        self.orchestrator = Agent(
            model=self.model,
            system_prompt=f"""당신은 사용자 요청을 분석하고 적절한 전문 에이전트에게 작업을 위임하는 오케스트레이터입니다.
사용자 ID: {user_id}

사용 가능한 도구들을 적절히 사용하여 사용자 요청에 응답하세요.
각 도구의 설명을 참고하여 언제, 어떻게 사용할지 스스로 판단하세요.""",
            tools=[search_agent, weather_agent, conversation_agent, memory_agent]
        )

        print(f"Super Agent 초기화 완료 (사용자: {user_id})")
        print(f"사용 모델: {type(self.model).__name__}")

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        사용자 입력을 처리하고 적절한 전문 에이전트에게 위임

        Args:
            user_input: 사용자 입력

        Returns:
            처리 결과
        """
        try:
            print(f"\n[Super Agent] 사용자 요청 분석 중: '{user_input}'")
            
            # 기존 메모리 컨텍스트 가져오기
            memory_context = memory_agent("retrieve", "", self.user_id)
            
            # 메모리에 사용자 입력 저장 여부 판단
            context_store = conversation_agent(f"""
            user context = {memory_context}
            user input = {user_input}

            TASK: Determine if user input contains new information worth storing.

            RULES:
            - If content exists in user context: return "000000"
            - If content is new but not meaningful for future requests: return "000000"
            - If content is new and meaningful: return ONLY the core content to store
            - NO explanations, reasons, or any additional text 
            - ONLY return the exact content or "000000"

            OUTPUT:
            """)
            
            if ("00000" in context_store):
                print("\nmemory에 저장될 내용이 아닙니다.\n")
            else:
                memory_agent("store", user_input, self.user_id)

            print("[Super Agent]  요청이 명확한지 분석합니다.")

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
            기존 대화 기록: {memory_context}
            
            사용자 요청이 추가 정보 없이 기존 대화 기록을 함께 사용해 답변 처리 가능한지 판단하세요.
            응답 형식: "NEED_MORE" 또는 "PROCEED"만 출력
            """
            
            clarity_response = clarity_agent(clarity_prompt)
            clarity_result = str(clarity_response).strip()

            
            # 매우 모호한 경우만 질문
            if "NEED_MORE" in clarity_result:
                print("\n[Super Agent] 📝 추가 정보가 필요합니다.")
                
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
                    "agent": "super_agent",
                    "user_input": user_input,
                    "response": str(clarification_response),
                    "needs_clarification": True,
                    "user_id": self.user_id
                }

            # 요청이 명확한 경우 - 실행 계획 수립 및 실행
            print("[Super Agent] 요청이 충분히 구체적입니다. 실행 계획 수립 중...")
            
            # 계획 수립 전용 Agent (도구 없음)
            planning_agent = Agent(
                model=self.model,
                system_prompt="""당신은 실행 계획만 수립하는 전문가입니다.
도구를 사용하지 말고, 오직 계획만 세우세요.

사용 가능한 도구들:
- search_agent: Wikipedia 검색이 필요한 정보 요청
- weather_agent: 날씨 정보 요청 (미국 지역만 지원)  
- conversation_agent: 일반 대화, 인사, 간단한 질문
- memory_agent: 메모리 저장/검색/삭제 요청
""",
                tools=[]
            )

            planning_prompt = f"""
            사용자 요청: "{user_input}"
            기존 대화 컨텍스트: {memory_context}
            
            이 요청을 처리하기 위한 실행 계획을 다음 형식으로 작성하세요:
            
            **📋 실행 계획:**
            1. [도구명] - [사용 이유와 목적]
            2. [도구명] - [사용 이유와 목적]
            ...
            
            **🎯 예상 결과:**
            [어떤 최종 결과를 사용자에게 제공할 예정인지]
            
            **⚠️ 주의사항:**
            [특별히 고려해야 할 사항이 있다면]
            """

            print()
            print("[SUPER AGENT 실행 계획]")
            print("="*60)
            plan_response = planning_agent(planning_prompt)
            print("="*60)
            plan_text = str(plan_response)


            # 계획에 따라 실제 도구들 실행 (이때만 orchestrator 사용)
            execution_prompt = f"""
            다음은 앞서 수립한 실행 계획입니다:
            
            {plan_text}
            
            이제 이 계획에 따라 실제로 도구들을 사용하여 사용자 요청을 처리하세요:
            
            사용자 요청: "{user_input}"
            기존 대화 컨텍스트: {memory_context}
            
            계획에 따라 순차적으로 도구들을 실행하고, 최종적으로 사용자에게 도움이 되는 종합적인 답변을 제공하세요.
            """

            print("\n[Super Agent] 🚀 계획에 따라 specialized agent 실행 중...")
            response = self.orchestrator(execution_prompt)

            print("[Super Agent] 모든 작업 완료")
            
            # <thinking> 태그 제거
            import re
            clean_response = re.sub(r'<thinking>.*?</thinking>', '', str(response), flags=re.DOTALL)
            clean_response = clean_response.strip()

            return {
                "success": True,
                "agent": "super_agent",
                "user_input": user_input,
                "execution_plan": plan_text,
                "response": clean_response,
                "needs_clarification": False,
                "user_id": self.user_id
            }

        except Exception as e:
            print(f"[Super Agent] ❌ 오류 발생: {str(e)}")
            return {
                "success": False,
                "agent": "super_agent",
                "error": str(e),
                "user_input": user_input
            }

    def get_agent_status(self) -> Dict[str, Any]:
        """에이전트 상태 정보 반환"""
        return {
            "super_agent": "활성",
            "model": type(self.model).__name__,
            "user_id": self.user_id,
            "available_agents": [
                "search_agent (Wikipedia 검색)",
                "weather_agent (날씨 정보)",
                "conversation_agent (일반 대화)",
                "memory_agent (메모리 관리)"
            ]
        }
