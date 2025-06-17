"""효율적인 메모리 관리 시스템"""
import json
from typing import List, Optional
from strands import Agent
from strands_tools import mem0_memory, use_llm


class MemoryManager:
    """워크샵용 효율적인 메모리 관리자"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id

        self.memory_agent = Agent(
            system_prompt="당신은 사용자 대화 기록을 관리하는 user prompt context(history) log 전문가입니다.",
            tools=[mem0_memory, use_llm]
        )
        
        # 요약 에이전트 - 메모리 컨텍스트 생성용
        self.summary_agent = Agent(
            system_prompt="당신은 대화 기록을 간결하게 요약하는 전문가입니다. 핵심 정보만 추출하세요."
        )

    def store_memory(self, content: str) -> bool:
        """메모리 저장 - 효율적인 단일 호출"""
        try:
            print("[memoryManager] 요청 내용 대화 저장 중...")
            
            # 메모리 저장
            result = self.memory_agent.tool.mem0_memory(
                action="store", 
                user_id=self.user_id, 
                content=content
            )
            
            if result.get('status') == 'success':
                print("[메모리 저장 완료]")
                return True
            else:
                print("  ❌ 메모리 저장 실패")
                return False
                
        except Exception as e:
            print(f"  ❌ 메모리 저장 오류: {str(e)}")
            return False

    def get_relevant_memory(self) -> Optional[str]:
        """관련 메모리 검색 및 요약"""
        try:
            # 메모리 목록 조회
            result = self.memory_agent.tool.mem0_memory(
                action="list", 
                user_id=self.user_id
            )
            
            if not (result.get('status') == 'success' and result.get('content')):
                return None
            
            # JSON 파싱
            json_text = result['content'][0]['text']
            memories = json.loads(json_text)
            
            if not memories:
                return None
            
            # 메모리 내용 추출
            memory_contents = []
            for memory in memories:
                if memory.get('memory'):
                    memory_contents.append(memory['memory'])
            
            if not memory_contents:
                return None

            combined_memory = "\n".join(memory_contents)
            summary_prompt = f"다음 대화 기록들을 핵심 정보만 간결하게 요약하세요:\n{combined_memory}"
            summary = self.summary_agent(summary_prompt)
            return str(summary)
                
        except Exception as e:
            print(f"  ❌ 메모리 검색 오류: {str(e)}")
            return None

    def list_memories(self) -> List[str]:
        """메모리 목록 반환"""
        try:
            result = self.memory_agent.tool.mem0_memory(
                action="list", 
                user_id=self.user_id
            )
            
            if result.get('status') == 'success' and result.get('content'):
                json_text = result['content'][0]['text']
                memories = json.loads(json_text)
                
                return [memory.get('memory', '') for memory in memories if memory.get('memory')]
            
            return []
            
        except Exception as e:
            print(f"❌ 메모리 목록 조회 오류: {str(e)}")
            return []

    def clear_all_memories(self) -> int:
        """모든 메모리 삭제"""
        try:
            # 메모리 목록 조회
            result = self.memory_agent.tool.mem0_memory(
                action="list", 
                user_id=self.user_id
            )
            
            if not (result.get('status') == 'success' and result.get('content')):
                return 0
            
            json_text = result['content'][0]['text']
            memories = json.loads(json_text)
            
            deleted_count = 0
            for memory in memories:
                memory_id = memory.get('id')
                if memory_id:
                    try:
                        delete_result = self.memory_agent.tool.mem0_memory(
                            action="delete",
                            memory_id=memory_id,
                            user_id=self.user_id
                        )
                        
                        if delete_result.get('status') == 'success':
                            deleted_count += 1
                            
                    except Exception as e:
                        print(f"  ❌ 메모리 삭제 실패: {memory_id}")
            
            return deleted_count
            
        except Exception as e:
            print(f"❌ 메모리 삭제 오류: {str(e)}")
            return 0

    def get_memory_count(self) -> int:
        """메모리 개수 반환"""
        return len(self.list_memories())
