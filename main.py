"""Agents as Tools 패턴을 사용한 다중 에이전트 시스템"""
import os
import sys
from typing import Dict, Any
from super_agent import SuperAgent
from model_config import get_configured_model, MODEL_PROVIDER
from specialized_agents import memory_agent

class MultiAgentApplication:
    """Agents as Tools- multi Agent"""

    def __init__(self, model_id: str = None, user_id: str = "workshop_user"):
        self.model = get_configured_model(model_id)
        self.user_id = user_id
        self.super_agent = SuperAgent(self.model, user_id)
        # 시스템 정보 출력
        model_name = type(self.model).__name__
        current_model_id = getattr(self.model, 'model_id', 'unknown')

        print("=" * 60)
        print("🤖 Agents as Tools multi agent demo")
        print("=" * 60)
        print(f"사용자 ID: {user_id}")
        print()
        print("사용 가능한 agent:")
        print("• Search Agent - Wikipedia 검색")
        print("• Weather Agent - 날씨 정보 (미국 지역)")
        print("• Conversation Agent - 일반 대화")
        print("• Memory Agent - 대화 기록 관리")
        print("• Super Agent - 오케스트레이터")
        print("=" * 60)

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """사용자 입력을 Super Agent를 통해 처리"""
        return self.super_agent.process_user_input(user_input)

    def run_single_query(self, query: str) -> Dict[str, Any]:
        """단일 쿼리 실행"""
        return self.process_input(query)

    def format_response(self, response: Dict[str, Any]) -> str:
        """응답 포맷팅 - 시인성 개선"""
        if response.get("success"):
            raw_response = response.get("response", "응답을 생성할 수 없습니다.")
            
            # <thinking> 태그 제거
            import re
            clean_response = re.sub(r'<thinking>.*?</thinking>', '', raw_response, flags=re.DOTALL)
            clean_response = clean_response.strip()
            
            return clean_response
        else:
            return f"오류: {response.get('error', '알 수 없는 오류')}"

    def print_final_response(self, response_text: str):
        print("\n" + "🎯" + "="*58 + "🎯")
        print("🤖 최종 응답")
        print(response_text)
        print("🎯" + "="*58 + "🎯")

    def run_interactive(self):
        """대화형 모드 실행"""
        print("\n🚀 대화형 모드 시작!")
        print("다양한 요청을 입력해보세요:")
        print("- 정보 검색: '라스베가스에 대해 알려줘'")
        print("- 날씨 조회: '뉴욕 날씨 어때?'")
        print("- 일반 대화: '안녕하세요'")
        print("- 메모리 조회: /list")
        print("- 메모리 초기화: /clear")
        print("메모리 정상 초기화 안된다면 실행! rm -rf /tmp/mem0_384_faiss/")
        print("- 종료: '/quit'")
        print()

        while True:
            try:
                user_input = input("💬 입력: ").strip()
                if user_input.lower() in ['quit', 'exit', '종료', '/quit']:
                    print("\n👋 시스템을 종료합니다. 안녕히 가세요!")
                    break

                if not user_input:
                    print("⚠️ 메시지를 입력해주세요.")
                    continue
                    
                if user_input.lower() in ['/list']:
                    memory_agent("retrieve", self.user_id)
                    continue
                    
                if user_input.lower() in ['/clear']:
                    memory_agent("clear", self.user_id)
                    continue

                # 입력 처리
                result = self.process_input(user_input)
                
                # 결과 출력 - 시인성 개선
                response_text = self.format_response(result)
                
                # 추가 정보가 필요한 경우 대화 계속
                if result.get("needs_clarification", False):
                    self.print_final_response(response_text)
                    print("\n💡 더 구체적으로 알려주시면 정확한 정보를 찾아드릴 수 있습니다.")
                    
                    # 사용자의 추가 입력 대기
                    follow_up = input("💬 추가 입력: ").strip()
                    
                    if not follow_up:
                        print("⚠️ 추가 정보를 입력해주세요.")
                        continue
                        
                    if follow_up.lower() in ['quit', 'exit', '종료', '/quit']:
                        print("\n👋 시스템을 종료합니다.")
                        break
                    
                    # 원래 요청과 추가 정보를 결합하여 다시 처리
                    combined_input = f"{user_input} - {follow_up}"
                    print(f"\n[System] 결합된 요청으로 재 처리: '{combined_input}'")
                    
                    result = self.process_input(combined_input)
                    response_text = self.format_response(result)
                    self.print_final_response(response_text)
                else:
                    # 바로 실행된 경우
                    self.print_final_response(response_text)
                
                print("\n" + "-" * 50 + "\n")

            except KeyboardInterrupt:
                print("\n\n👋 시스템을 종료합니다.")
                break
            except Exception as e:
                print(f"\n❌ 오류 발생: {str(e)}")


def main():
    """메인 함수"""
    # 사용자 ID 설정
    user_id = os.getenv("USER_ID", "workshop_user")

    # 애플리케이션 초기화
    app = MultiAgentApplication(user_id=user_id)

    # 실행 모드 결정
    if len(sys.argv) > 1:
        # 단일 쿼리 모드
        query = " ".join(sys.argv[1:])
        result = app.run_single_query(query)
        print(app.format_response(result))
    else:
        # 대화형 모드
        app.run_interactive()


if __name__ == "__main__":
    main()
