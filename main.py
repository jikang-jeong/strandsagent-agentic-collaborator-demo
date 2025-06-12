"""다중 에이전트 시스템 메인 애플리케이션"""
import asyncio
import json
import os
from typing import Dict, Any
from super_agent import SuperAgent
from model_config import get_configured_model, MODEL_PROVIDER, MODEL_ID

# .env 파일에서 환경 변수 로드
try:
    from dotenv import load_dotenv
    if os.path.exists('.env'):
        load_dotenv()
except ImportError:
    pass  # python-dotenv가 설치되지 않음


class MultiAgentApplication:
    """다중 에이전트 애플리케이션 클래스"""
    
    def __init__(self, model_id: str = None):
        self.model = get_configured_model(model_id)
        self.super_agent = SuperAgent(self.model)
        
        # 모델 정보 표시
        model_name = type(self.model).__name__
        current_model_id = getattr(self.model, 'model_id', 'unknown')
        print(f"[*] 사용 중인 모델: {model_name}, 모델 ID: {current_model_id}")
        print(f"[*] 제공자: {MODEL_PROVIDER}")
        print("=" * 50)
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """사용자 입력을 슈퍼 에이전트를 통해 처리"""
        print(f"\n[*] 입력 처리 중: '{user_input}'")
        print("=" * 50)
        print("[*] 다중 에이전트 조정 시작...")
        
        # 슈퍼 에이전트를 통해 처리
        result = self.super_agent.process_user_input(user_input)
        
        return result
    
    def run_single_query(self, query: str) -> Dict[str, Any]:
        """단일 쿼리 실행"""
        return self.process_input(query)
    
    def format_response(self, response: Dict[str, Any]) -> str:
        """LLM 종합 응답을 강조하여 응답 형식화"""
        # LLM 종합 응답을 눈에 띄게 표시
        output = []
        
        if response.get("llm_synthesis"):
            output.append("[*] AI 어시스턴트 응답:")
            output.append("=" * 50)
            # AgentResult를 문자열로 변환 (필요한 경우)
            synthesis = response["llm_synthesis"]
            if hasattr(synthesis, '__str__'):
                synthesis = str(synthesis)
            output.append(synthesis)
            output.append("\n" + "=" * 50)
            output.append("\n[*] 상세 기술 데이터:")
        
        # 응답을 JSON 직렬화 가능한 형식으로 변환
        try:
            # 직렬화 불가능한 객체를 문자열로 변환
            serializable_response = self._make_json_serializable(response)
            output.append(json.dumps(serializable_response, indent=2, ensure_ascii=False))
        except Exception as e:
            output.append(f"기술 데이터 형식화 오류: {str(e)}")
            # 문자열 표현으로 대체
            try:
                output.append(str(response))
            except:
                output.append("기술 데이터를 표시할 수 없습니다")
        
        return "\n".join(str(item) for item in output)  # 모든 항목이 문자열인지 확인
    
    def _make_json_serializable(self, obj):
        """객체를 JSON 직렬화 가능한 형식으로 변환"""
        if hasattr(obj, '__dict__'):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        else:
            try:
                json.dumps(obj)
                return obj
            except (TypeError, ValueError):
                return str(obj)
    
    def run_interactive(self):
        """대화형 모드 실행"""
        print("[*] LLM 종합 기능을 갖춘 다중 에이전트 시스템 시작!")
        print("=" * 50)
        print("[*] AI 기반 에이전트들:")
        print("- 날씨 예보: LLM 생성 날씨 분석")
        print("- 검색 에이전트: 도구를 사용한 LLM 기반 포괄적 검색")
        print("- 추가 에이전트: LLM 생성 친근한 지원")
        print("- 슈퍼 에이전트: 모든 결과의 LLM 종합")
        print(f"\n[*] 사용 중: {type(self.model).__name__}")
        print("\n포괄적인 AI 기반 정보를 얻으려면 검색 쿼리를 입력하세요.")
        print("종료하려면 'quit'를 입력하세요.\n")
        
        while True:
            try:
                user_input = input("[>] 검색 쿼리 입력: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '종료', '나가기']:
                    print("[*] 다중 에이전트 시스템을 종료합니다. 안녕히 가세요!")
                    break
                
                if not user_input:
                    print("[!] 유효한 검색 쿼리를 입력해주세요.")
                    continue
                
                # 입력 처리
                result = self.process_input(user_input)
                
                # 결과 표시
                print(self.format_response(result))
                print("\n" + "=" * 50 + "\n")
                
            except KeyboardInterrupt:
                print("\n[*] 다중 에이전트 시스템을 종료합니다. 안녕히 가세요!")
                break
            except Exception as e:
                print(f"[!] 오류 발생: {str(e)}")


def main():
    """메인 함수"""
    # 특정 모델 ID로 실행하려면:
    # app = MultiAgentApplication("anthropic.claude-3-5-sonnet-20241022-v2:0")
    
    app = MultiAgentApplication("anthropic.claude-3-5-sonnet-20241022-v2:0")
    
    # 대화형 모드 또는 단일 쿼리로 실행할 수 있습니다
    import sys
    
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
