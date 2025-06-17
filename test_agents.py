"""Agents as Tools 시스템 테스트"""
import os
from main import MultiAgentApplication


def test_search_agent():
    """Search Agent 테스트"""
    print("=" * 50)
    print("🔍 Search Agent 테스트")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    test_queries = [
        "파리에 대해 알려줘",
        "인공지능이란 무엇인가?",
        "파이썬 프로그래밍 언어"
    ]
    
    for query in test_queries:
        print(f"\n📝 테스트 쿼리: {query}")
        result = app.run_single_query(query)
        print(f"✅ 결과: {app.format_response(result)[:200]}...")
        print("-" * 30)


def test_weather_agent():
    """Weather Agent 테스트"""
    print("=" * 50)
    print("🌤️ Weather Agent 테스트")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    test_queries = [
        "뉴욕 날씨 어때?",
        "로스앤젤레스 날씨 알려줘",
        "시카고 날씨 정보"
    ]
    
    for query in test_queries:
        print(f"\n📝 테스트 쿼리: {query}")
        result = app.run_single_query(query)
        print(f"✅ 결과: {app.format_response(result)[:200]}...")
        print("-" * 30)


def test_conversation_agent():
    """Conversation Agent 테스트"""
    print("=" * 50)
    print("💬 Conversation Agent 테스트")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    test_queries = [
        "안녕하세요",
        "오늘 기분이 좋아요",
        "도움이 필요해요",
        "고마워요"
    ]
    
    for query in test_queries:
        print(f"\n📝 테스트 쿼리: {query}")
        result = app.run_single_query(query)
        print(f"✅ 결과: {app.format_response(result)[:200]}...")
        print("-" * 30)


def test_memory_agent():
    """Memory Agent 테스트"""
    print("=" * 50)
    print("🧠 Memory Agent 테스트")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    # 메모리 저장 테스트
    print("\n📝 메모리 저장 테스트")
    result = app.run_single_query("내 이름은 김철수야")
    print(f"✅ 결과: {app.format_response(result)[:200]}...")
    
    # 메모리 활용 테스트
    print("\n📝 메모리 활용 테스트")
    result = app.run_single_query("내 이름이 뭐였지?")
    print(f"✅ 결과: {app.format_response(result)[:200]}...")


def test_integration():
    """통합 테스트"""
    print("=" * 50)
    print("🔄 통합 테스트")
    print("=" * 50)
    
    app = MultiAgentApplication()
    
    # 복합 요청 테스트
    test_queries = [
        "안녕하세요, 파리 날씨 알려주세요",  # 인사 + 날씨 (미국 외 지역)
        "뉴욕에 대해 알려주고 날씨도 알려주세요",  # 검색 + 날씨
        "내 이름은 홍길동이고, 인공지능에 대해 알고 싶어요"  # 메모리 + 검색
    ]
    
    for query in test_queries:
        print(f"\n📝 테스트 쿼리: {query}")
        result = app.run_single_query(query)
        print(f"✅ 결과: {app.format_response(result)[:300]}...")
        print("-" * 30)


def main():
    """테스트 실행"""
    print("🧪 Agents as Tools 시스템 테스트 시작")
    
    try:
        test_search_agent()
        test_weather_agent()
        test_conversation_agent()
        test_memory_agent()
        test_integration()
        
        print("\n" + "=" * 50)
        print("✅ 모든 테스트 완료!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
