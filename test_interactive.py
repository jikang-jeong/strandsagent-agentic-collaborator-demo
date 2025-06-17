#!/usr/bin/env python3
"""Interactive 기능 테스트 스크립트"""

from main import MultiAgentApplication

def test_interactive_flow():
    """Interactive 대화 흐름 테스트"""
    print("🧪 Interactive 대화 흐름 테스트 (LLM 기반 판단)")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    # 테스트 케이스들 - LLM이 직접 판단
    test_cases = [
        # 매우 모호한 요청 (LLM이 NEED_MORE로 판단할 가능성 높음)
        ("커피", "매우 모호 - LLM 판단"),
        ("음식", "매우 모호 - LLM 판단"),
        ("영화", "매우 모호 - LLM 판단"),
        
        # 약간 모호하지만 처리 가능한 요청 (LLM이 PROCEED로 판단할 가능성 높음)
        ("ice coffee", "LLM이 처리 가능으로 판단 예상"),
        ("파리", "LLM이 처리 가능으로 판단 예상"),
        ("날씨 정보", "LLM이 처리 가능으로 판단 예상"),
        
        # 명확한 요청 (LLM이 PROCEED로 판단할 것)
        ("뉴욕 날씨 어때?", "명확한 요청 - LLM 판단"),
        ("파리에 대해 자세히 알려줘", "명확한 요청 - LLM 판단"),
        ("아이스 커피 레시피 알려줘", "명확한 요청 - LLM 판단"),
    ]
    
    for i, (test_input, expected) in enumerate(test_cases, 1):
        print(f"\n🧪 테스트 {i}: '{test_input}' ({expected})")
        print("-" * 40)
        
        result = app.process_input(test_input)
        
        print(f"✅ 결과:")
        print(f"   - 성공: {result.get('success')}")
        print(f"   - 명확화 필요: {result.get('needs_clarification', False)}")
        print(f"   - 응답: {result.get('response', 'N/A')[:100]}...")
        
        if result.get('needs_clarification'):
            print("   → ❓ LLM이 추가 정보 필요로 판단")
        else:
            print("   → ✅ LLM이 처리 가능으로 판단하여 바로 실행")
        
        print()

if __name__ == "__main__":
    test_interactive_flow()
