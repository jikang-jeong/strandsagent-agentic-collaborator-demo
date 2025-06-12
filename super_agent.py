"""워크샵 데모용 간단한 슈퍼 에이전트"""
import json
from typing import Dict, Any, List
from strands import Agent
from agents import WeatherForecastAgent, SearchAgent, ExtraAgent
from model_config import get_configured_model
from agent_planner import AgentPlanner


class SuperAgent:
    """워크샵 데모용 간단한 슈퍼 에이전트"""
    
    def __init__(self, model=None):
        self.model = model or get_configured_model()
        self.agent = Agent(
            model=self.model,
            system_prompt="""당신은 여러 전문 에이전트를 조정하는 슈퍼 에이전트입니다.

역할:
1. 지능적 계획에 기반한 에이전트 조정
2. 결과를 사용자 친화적인 응답으로 종합
3. 포괄적이고 도움이 되는 정보 제공

항상 정보를 제공하고 응답에서 도움이 되도록 하세요.""",
            tools=[]
        )
        
        # 에이전트 초기화
        self.weather_agent = WeatherForecastAgent(model)
        self.search_agent = SearchAgent(model)
        self.extra_agent = ExtraAgent(model)
        self.planner = AgentPlanner(model)
        
        # 에이전트 매핑
        self.agent_map = {
            "search": self.search_agent,
            "weather": self.weather_agent,
            "extra": self.extra_agent
        }
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """워크샵 데모용 간단한 에이전트 조정"""
        try:
            print("[*] 에이전트 조정 시작...")
            
            # 1단계: 실행 계획 생성
            planning_result = self.planner.create_execution_plan(user_input)
            
            if not planning_result.get("success"):
                print("[!] 계획 실패")
                return {"success": False, "error": "계획 실패"}
            
            plan = planning_result["plan"]
            agents_to_execute = plan.get("agents_to_execute", ["search"])
            reasoning = plan.get("reasoning", "이유 없음")
            
            print(f"[*] 선택된 에이전트: {', '.join(agents_to_execute)}")
            print(f"[*] 이유: {reasoning}")
            print()
            
            # 2단계: 에이전트 실행
            agent_results = {}
            executed_agents = []
            
            for agent_name in agents_to_execute:
                if agent_name in self.agent_map:
                    print(f"[>] {agent_name.upper()} 에이전트 실행 중...")
                    result = self._execute_agent(agent_name, user_input, agent_results)
                    
                    if result:
                        agent_results[agent_name] = result
                        executed_agents.append(agent_name)
                        
                        if result.get("success"):
                            print(f"[+] {agent_name.upper()} 에이전트 완료")
                        else:
                            print(f"[!] {agent_name.upper()} 에이전트 실패")
            
            # 3단계: LLM 종합 생성
            print("[*] 최종 응답 생성 중...")
            llm_synthesis = self._generate_llm_synthesis(user_input, agent_results, reasoning)
            
            # 4단계: 응답 컴파일
            response = self._compile_response(user_input, agent_results, llm_synthesis, reasoning, executed_agents)
            
            print(f"[*] 완료: {', '.join(executed_agents)}")
            print("=" * 50)
            
            return response
            
        except Exception as e:
            print(f"[!] 오류: {str(e)}")
            return {
                "success": False,
                "agent": "super_agent",
                "error": f"오류: {str(e)}",
                "user_input": user_input
            }
    
    def _execute_agent(self, agent_name: str, user_input: str, existing_results: Dict[str, Any]) -> Dict[str, Any]:
        """LLM 기반 문맥 이해를 통한 특정 에이전트 실행"""
        try:
            if agent_name == "search":
                return self.search_agent.search(user_input)
            
            elif agent_name == "weather":
                # LLM을 사용하여 문맥을 이해하고 날씨용 위치 추출
                return self._execute_weather_with_llm_context(user_input, existing_results)
            
            elif agent_name == "extra":
                return self.extra_agent.say_hello(user_input)
            
            else:
                return None
                
        except Exception as e:
            return {
                "success": False,
                "agent": agent_name,
                "error": f"{agent_name} 에이전트 실행 오류: {str(e)}",
                "user_input": user_input
            }
    
    def _execute_weather_with_llm_context(self, user_input: str, existing_results: Dict[str, Any]) -> Dict[str, Any]:
        """LLM 기반 문맥 이해를 통한 날씨 에이전트 실행"""
        try:
            # 먼저 검색 에이전트에서 좌표가 있는지 확인
            search_result = existing_results.get("search")
            if search_result and search_result.get("position_info", {}).get("success"):
                position_info = search_result["position_info"]
                latitude = position_info["latitude"]
                longitude = position_info["longitude"]
                print(f"  [*] 검색에서 좌표 사용: {latitude}, {longitude}")
                return self.weather_agent.get_weather_forecast(latitude, longitude)
            
            # 검색에서 좌표가 없으면 LLM을 사용하여 문맥을 이해하고 위치 추출
            print("  [*] LLM을 사용하여 위치 문맥 이해 중...")
            
            location_prompt = f"""이 사용자 요청을 분석하세요: "{user_input}"

사용자가 날씨 정보를 요청하고 있습니다. 다음을 수행하세요:
1. 요청에서 언급된 위치가 있는지 확인
2. 위치 이름이 있으면 추출
3. 특정 위치가 언급되지 않았으면 표시

위치 이름만 응답하거나, 위치를 찾을 수 없으면 "NO_LOCATION"으로 응답하세요.

예시:
- "용인 날씨" → "용인"
- "서울 weather" → "서울" 
- "도쿄 날씨는 어때?" → "도쿄"
- "날씨 어때?" → "NO_LOCATION"

사용자 요청: "{user_input}"
위치:"""

            # 슈퍼 에이전트의 LLM을 사용하여 문맥 이해
            location_response = self.agent(location_prompt)
            
            # 응답 정리
            if hasattr(location_response, '__str__'):
                location_response = str(location_response).strip()
            
            print(f"  [*] LLM이 추출한 위치: '{location_response}'")
            
            if location_response and location_response != "NO_LOCATION" and len(location_response) > 0:
                # 추출된 위치의 좌표 획득 시도
                from mcp_tools import get_position
                try:
                    pos_result = get_position(location_response)
                    if pos_result.get("success"):
                        lat, lon = pos_result["latitude"], pos_result["longitude"]
                        print(f"  [*] {location_response}의 좌표 발견: {lat}, {lon}")
                        return self.weather_agent.get_weather_forecast(lat, lon)
                    else:
                        print(f"  [!] 좌표를 찾을 수 없음: {location_response}")
                except Exception as e:
                    print(f"  [!] 좌표 획득 오류: {str(e)}")
            
            # 여전히 위치가 없으면 오류 반환
            return {
                "success": False,
                "agent": "weather",
                "error": "날씨 쿼리의 위치를 결정할 수 없습니다. 위치를 지정해주세요.",
                "user_input": user_input,
                "llm_extracted_location": location_response
            }
                
        except Exception as e:
            return {
                "success": False,
                "agent": "weather",
                "error": f"LLM 기반 날씨 실행 오류: {str(e)}",
                "user_input": user_input
            }
    
    def _generate_llm_synthesis(self, user_input: str, agent_results: Dict[str, Any], reasoning: str) -> str:
        """선택된 에이전트 결과의 포괄적 LLM 종합 생성"""
        try:
            # LLM용 간소화된 문맥 준비
            context_parts = [
                f"사용자 요청: \"{user_input}\"",
                f"계획 이유: {reasoning}",
                "\n에이전트 결과:\n"
            ]
            
            # 실행된 에이전트의 결과 추가
            for agent_name, result in agent_results.items():
                context_parts.append(f"{agent_name.upper()} 에이전트:")
                context_parts.append(f"   - 성공: {result.get('success', False)}")
                
                if agent_name == "search":
                    context_parts.append(f"   - 쿼리: {result.get('query', 'N/A')}")
                    if result.get('llm_response'):
                        context_parts.append(f"   - LLM 분석: {result['llm_response']}")
                    
                    wiki_info = result.get('wikipedia_info', {})
                    if wiki_info.get('success'):
                        context_parts.append(f"   - 위키피디아 제목: {wiki_info.get('title', 'N/A')}")
                        context_parts.append(f"   - 위키피디아 요약: {wiki_info.get('summary', 'N/A')}")
                    
                    position_info = result.get('position_info', {})
                    if position_info.get('success'):
                        context_parts.append(f"   - 좌표: {position_info.get('latitude', 'N/A')}, {position_info.get('longitude', 'N/A')}")
                
                elif agent_name == "weather":
                    if result.get('llm_response'):
                        context_parts.append(f"   - LLM 날씨 분석: {result['llm_response']}")
                    
                    weather_data = result.get('data', {})
                    if weather_data:
                        current = weather_data.get('current', {})
                        context_parts.append(f"   - 현재 온도: {current.get('temperature', 'N/A')}°C")
                        context_parts.append(f"   - 현재 설명: {current.get('description', 'N/A')}")
                
                elif agent_name == "extra":
                    if result.get('llm_response'):
                        context_parts.append(f"   - LLM 응답: {result['llm_response']}")
                
                context_parts.append("")  # 에이전트 간 빈 줄
            
            # 작업 지시사항 추가
            context_parts.extend([
                f"작업: 다음을 포함하는 포괄적이고 사용자 친화적인 응답을 제공하세요:",
                f"1. \"{user_input}\"에 대한 사용자 요청에 직접 답변",
                f"2. 실행된 에이전트의 정보 종합 (모든 에이전트가 실행된 것은 아님 - 관련된 것만)",
                f"3. 발견된 정보와 발견되지 않은 정보 설명",
                f"4. 실행 가능한 통찰력이나 흥미로운 사실 제공",
                f"5. 자연스럽고 대화적인 언어 사용",
                f"6. 지능적 에이전트 선택 과정 인정",
                f"\n\"{user_input}\"에 대해 묻는 사람에게 도움이 되고 정보를 제공하는 응답을 생성하세요."
            ])
            
            context = "\n".join(context_parts)
            
            # LLM 종합 생성
            synthesis = self.agent(context)
            return synthesis
            
        except Exception as e:
            return f"종합 생성 오류: {str(e)}"
    
    def _compile_response(self, user_input: str, agent_results: Dict[str, Any], 
                         llm_synthesis: str, reasoning: str, executed_agents: List[str]) -> Dict[str, Any]:
        """LLM 종합을 통한 선택된 에이전트 결과의 포괄적 응답 컴파일"""
        
        response = {
            "success": True,
            "agent": "super_agent",
            "model_info": {
                "provider": type(self.model).__name__,
                "model_id": getattr(self.model, 'model_id', 'unknown')
            },
            "user_input": user_input,
            "timestamp": self._get_timestamp(),
            "planning": {
                "reasoning": reasoning,
                "agents_selected": executed_agents,
                "total_available_agents": ["search", "weather", "extra"]
            },
            "llm_synthesis": llm_synthesis,  # 메인 LLM 생성 응답
            "agents_called": executed_agents,
            "agent_results": agent_results,  # 실행된 에이전트의 결과만
            "summary": {}
        }
        
        # 실행된 에이전트를 기반으로 요약 구성
        if "search" in agent_results:
            search_result = agent_results["search"]
            if search_result.get("success"):
                wiki_info = search_result.get("wikipedia_info", {})
                position_info = search_result.get("position_info", {})
                
                response["summary"]["query"] = search_result.get("query")
                response["summary"]["wikipedia_found"] = wiki_info.get("success", False)
                response["summary"]["coordinates_found"] = position_info.get("success", False)
                
                if wiki_info.get("success"):
                    response["summary"]["wikipedia_title"] = wiki_info.get("title")
                
                if position_info.get("success"):
                    response["summary"]["latitude"] = position_info.get("latitude")
                    response["summary"]["longitude"] = position_info.get("longitude")
        
        if "weather" in agent_results:
            weather_result = agent_results["weather"]
            response["summary"]["weather_available"] = weather_result.get("success", False)
        
        if "extra" in agent_results:
            response["summary"]["extra_agent_called"] = True
        else:
            response["summary"]["extra_agent_called"] = False
        
        # 전체 평가
        response["summary"]["overall_success"] = any(
            result.get("success", False) for result in agent_results.values()
        )
        
        response["summary"]["agents_executed"] = len(executed_agents)
        response["summary"]["intelligent_selection"] = True
        
        return response
    
    def _get_timestamp(self) -> str:
        """현재 타임스탬프 가져오기"""
        from datetime import datetime
        return datetime.now().isoformat()
