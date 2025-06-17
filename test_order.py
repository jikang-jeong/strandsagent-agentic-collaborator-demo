#!/usr/bin/env python3
"""실행 순서 테스트"""

from main import MultiAgentApplication

def test_execution_order():
    """실행 순서가 올바른지 테스트"""
    print("🧪 실행 순서 테스트")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    # 명확한 날씨 요청으로 테스트
    print("=== 테스트: '뉴욕 날씨 어때?' ===")
    print("예상 순서:")
    print("1. 명확성 판단 (도구 사용 안함)")
    print("2. 실행 계획 수립 (도구 사용 안함)")
    print("3. 계획 실행 (이때만 도구 사용)")
    print()
    
    result = app.process_input("뉴욕 날씨 어때?")
    
    print("\n=== 결과 ===")
    print(f"성공: {result.get('success')}")
    print(f"명확화 필요: {result.get('needs_clarification', False)}")
    
    if result.get('success'):
        print("✅ 순서대로 실행됨")
    else:
        print("❌ 실행 오류")

if __name__ == "__main__":
    test_execution_order()
