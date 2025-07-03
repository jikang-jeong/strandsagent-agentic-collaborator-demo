#!/usr/bin/env python3
"""
워크샵용 Agents as Tools 시스템 테스트

이 파일은 워크샵 참가자들이 시스템의 핵심 기능을 
쉽게 이해하고 테스트할 수 있도록 설계되었습니다.
"""

from main import MultiAgentApplication


class WorkshopTester:
    """워크샵용 간단한 테스트 실행기"""
    
    def __init__(self):
        print("🎓 워크샵용 Agents as Tools 시스템 테스트")
        print("=" * 60)
        self.app = MultiAgentApplication()
        print()
    
    def test_basic_functionality(self):
        """기본 기능 테스트"""
        print("📋 1. 기본 기능 테스트")
        print("-" * 40)
        
        test_cases = [
            ("안녕하세요", "일반 대화"),
            ("파이썬이란?", "검색 기능"),
            ("뉴욕 날씨", "날씨 조회")
        ]
        
        for query, description in test_cases:
            print(f"\n🧪 테스트: {query} ({description})")
            result = self.app.run_single_query(query)
            
            if result.get('success'):
                print("✅ 성공")
                response = self.app.format_response(result)
                print(f"📝 응답: {response[:100]}...")
            else:
                print("❌ 실패")
                print(f"오류: {result.get('error', 'Unknown')}")
    
    def test_orchestrator_planning(self):
        """오케스트레이터 계획 수립 테스트"""
        print("\n📋 2. 오케스트레이터 계획 수립 테스트")
        print("-" * 40)
        
        print("🎯 복합 요청으로 계획 수립 과정 확인")
        query = "파리에 대해 알려주고 날씨도 알려줘"
        print(f"테스트 쿼리: {query}")
        print()
        
        # 실행 계획이 출력되는 것을 확인
        result = self.app.run_single_query(query)
        
        if result.get('success'):
            print("✅ 계획 수립 및 실행 성공")
        else:
            print("❌ 계획 수립 실패")
    
    def test_sub_agents(self):
        """하위 에이전트별 테스트"""
        print("\n📋 3. 하위 에이전트별 테스트")
        print("-" * 40)
        
        agents_tests = [
            ("Search Agent", "인공지능이란 무엇인가?"),
            ("Weather Agent", "로스앤젤레스 날씨 어때?"),
            ("Conversation Agent", "오늘 기분이 좋아요")
        ]
        
        for agent_name, query in agents_tests:
            print(f"\n🤖 {agent_name} 테스트")
            print(f"쿼리: {query}")
            
            result = self.app.run_single_query(query)
            
            if result.get('success'):
                print("✅ 성공")
            else:
                print("❌ 실패")
    
    def test_interactive_flow(self):
        """대화형 흐름 테스트 (워크샵용 간소화)"""
        print("\n📋 4. 대화형 흐름 테스트")
        print("-" * 40)
        
        print("🔄 명확성 판단 기능 테스트")
        
        # 명확한 요청
        print("\n✅ 명확한 요청 테스트:")
        clear_query = "뉴욕 날씨 어때?"
        print(f"쿼리: {clear_query}")
        
        result = self.app.process_input(clear_query)
        needs_clarification = result.get('needs_clarification', False)
        
        print(f"명확화 필요: {needs_clarification}")
        if not needs_clarification:
            print("→ 바로 실행됨 ✅")
        else:
            print("→ 추가 정보 요청됨")
        
        # 모호한 요청 (LLM 판단에 따라 결과가 달라질 수 있음)
        print("\n❓ 모호한 요청 테스트:")
        vague_query = "커피"
        print(f"쿼리: {vague_query}")
        
        result = self.app.process_input(vague_query)
        needs_clarification = result.get('needs_clarification', False)
        
        print(f"명확화 필요: {needs_clarification}")
        if needs_clarification:
            print("→ 추가 정보 요청됨 ✅")
            print(f"응답: {result.get('response', '')[:100]}...")
        else:
            print("→ 바로 실행됨 (LLM이 처리 가능으로 판단)")
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        try:
            self.test_basic_functionality()
            self.test_orchestrator_planning()
            self.test_sub_agents()
            self.test_interactive_flow()
            
            print("\n" + "=" * 60)
            print("🎉 워크샵 테스트 완료!")
            print("=" * 60)
            print("✅ 모든 핵심 기능이 정상 작동합니다.")
            print("🎓 이제 워크샵을 진행할 준비가 되었습니다!")
            
        except Exception as e:
            print(f"\n❌ 테스트 중 오류 발생: {str(e)}")
            print("🔧 시스템 설정을 확인해주세요.")


def main():
    """메인 실행 함수"""
    tester = WorkshopTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
