#!/usr/bin/env python3
"""간단한 테스트"""

from main import MultiAgentApplication

def test_simple():
    app = MultiAgentApplication()
    
    # 모호한 요청 테스트
    print("=== 모호한 요청 테스트: '컵' ===")
    result = app.process_input("컵")
    
    if result.get("needs_clarification"):
        print("✅ 추가 정보 요청됨")
        print("응답:", result.get("response", "")[:100])
    else:
        print("❌ 바로 실행됨")
        
    print("\n=== 명확한 요청 테스트: '뉴욕 날씨' ===")
    result2 = app.process_input("뉴욕 날씨")
    
    if result2.get("needs_clarification"):
        print("❌ 추가 정보 요청됨")
    else:
        print("✅ 바로 실행됨")
        print("응답:", result2.get("response", "")[:100])

if __name__ == "__main__":
    test_simple()
