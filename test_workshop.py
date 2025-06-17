"""워크샵용 테스트 스크립트"""
import os
import sys
from main import WorkshopMultiAgentSystem


def test_workshop_system():
    """워크샵 시스템 테스트"""
    print("🧪 워크샵 시스템 테스트 시작")
    print("=" * 50)
    
    # 테스트용 사용자 ID
    test_user_id = "test_workshop_user"
    
    try:
        # 시스템 초기화
        app = WorkshopMultiAgentSystem(user_id=test_user_id)
        
        # 테스트 쿼리들
        test_queries = [
            "hello",                    # ExtraAgent 테스트
            "서울",                     # SearchAgent 테스트  
            "뉴욕 날씨",                # Search + Weather 테스트
            "간단한 질문입니다"         # 직접 응답 테스트
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 테스트 {i}: '{query}'")
            print("-" * 30)
            
            try:
                result = app.process_query(query)
                response = app.format_response(result)
                
                print(f"✅ 성공: {result.get('processing_mode', 'unknown')}")
                print(f"📝 응답: {response[:100]}...")
                
            except Exception as e:
                print(f"❌ 실패: {str(e)}")
        
        # 메모리 테스트
        print(f"\n🧠 메모리 테스트")
        print("-" * 30)
        app._show_memory_status()
        
        print(f"\n🧪 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 시스템 초기화 실패: {str(e)}")


def test_individual_components():
    """개별 컴포넌트 테스트"""
    print("\n🔧 개별 컴포넌트 테스트")
    print("=" * 50)
    
    try:
        # 메모리 매니저 테스트
        from memory_manager import MemoryManager
        memory = MemoryManager("test_user")
        
        print("🧠 메모리 매니저 테스트...")
        memory.store_memory("테스트 메모리")
        count = memory.get_memory_count()
        print(f"✅ 메모리 저장 완료: {count}개")
        
        # 에이전트 테스트
        from agents import SearchAgent, ExtraAgent
        from model_config import get_configured_model
        
        model = get_configured_model()
        
        print("\n🔍 SearchAgent 테스트...")
        search_agent = SearchAgent(model)
        # 간단한 테스트는 실제 API 호출 없이 초기화만 확인
        print("✅ SearchAgent 초기화 완료")
        
        print("\n👋 ExtraAgent 테스트...")
        extra_agent = ExtraAgent(model)
        print("✅ ExtraAgent 초기화 완료")
        
        print("\n🔧 컴포넌트 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 컴포넌트 테스트 실패: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--components":
        test_individual_components()
    else:
        test_workshop_system()
        test_individual_components()
