# Agents as Tools 다중 에이전트 시스템

Strands Agents SDK를 사용한 "Agents as Tools" 패턴 구현 예제입니다.

## 시스템 구조

### Sub Agents (하위 에이전트들)

1. **Search Agent** - 지능적 검색 전문
   - Wikipedia API: 백과사전적 정보, 역사, 과학 개념
   - DuckDuckGo API: 기술 정의, 현대적 주제, 실시간 정보
   - **스마트 선택**: LLM이 질문 분석 후 최적 도구 선택
   - **상호 보완**: 첫 번째 결과 부족 시 다른 도구로 보완

2. **Weather Agent** - 날씨 정보 전문  
   - 지역 좌표 검색
   - National Weather Service API 사용 (미국 지역만)
   - 날씨 예보 제공

3. **Conversation Agent** - 일반 대화 전문
   - 인사말, 일상 대화
   - 검색이 필요하지 않은 일반적인 질문 응답

### 오케스트레이터

4. **Orchestrator Agent** - 전체 조정
   - 사용자 요청 분석
   - 요청 명확성 판단 (NEW!)
   - 적절한 하위 에이전트 선택 및 호출
   - 결과 종합 및 최종 응답 생성

## 주요 특징

- **Agents as Tools 패턴**: 각 하위 에이전트가 `@tool` 데코레이터로 도구화
- **계층적 위임**: Orchestrator Agent가 하위 에이전트들을 조정
- **🆕 Interactive 대화 흐름**: 모호한 요청 시 추가 정보 요청
- **2단계 처리**: 1) 명확성 판단 → 2) 계획 수립 → 3) 계획 실행
- **실행 계획 가시성**: Orchestrator Agent가 어떤 계획으로 에이전트들을 실행할지 명시적으로 표시
- **모듈화**: 각 에이전트는 독립적으로 개발/수정 가능
- **LLM 자체 판단**: 하드코딩 없이 LLM이 상황에 맞게 판단

## 🆕 Interactive 대화 흐름

### 모호한 요청 처리
```
사용자: "ice coffee"

[Orchestrator Agent] 🔍 요청 명확성 분석 중...
[Orchestrator Agent] 📝 추가 정보가 필요합니다.

🤖 아이스 커피에 대해 어떤 정보를 원하시나요? 
   - 집에서 만드는 레시피를 알고 싶으신가요?
   - 추천 브랜드나 제품을 찾고 계신가요?
   - 아이스 커피의 일반적인 정보가 궁금하신가요?

💡 더 구체적으로 알려주시면 정확한 정보를 찾아드릴 수 있습니다.
💬 추가 입력: 레시피 알려줘

[System] 결합된 요청으로 다시 처리: 'ice coffee - 레시피 알려줘'

📋 ORCHESTRATOR AGENT 실행 계획
====================================
**📋 실행 계획:**
1. search_agent - 아이스 커피 레시피 검색
2. conversation_agent - 검색 결과를 바탕으로 사용자 친화적 레시피 제공

**🎯 예상 결과:**
집에서 쉽게 만들 수 있는 아이스 커피 레시피 제공
====================================

→ 계획에 따라 각 에이전트가 순차 실행
```

### 명확한 요청 처리
```
사용자: "newyork 날씨 어때?"

[Orchestrator Agent] ✅ 요청이 명확합니다. 실행 계획 수립 중...

📋 ORCHESTRATOR AGENT 실행 계획
====================================
**📋 실행 계획:**
1. weather_agent - newyork 지역 날씨 정보 조회

**🎯 예상 결과:**
뉴욕의 현재 날씨 및 예보 정보 제공
====================================

→ 바로 실행
```

## 빠른 시작

### 1. 환경 설정 (선택사항)
```bash
cp .env.example .env
# .env 파일에서 필요한 환경변수 설정 (모델 설정 등)
```

### 2. 실행
```bash
# 🚀 자동 설정 및 실행 (권장)
./run.sh

# 대화형 모드
./run.sh

# 단일 쿼리 모드  
./run.sh "파리에 대해 알려줘"
./run.sh "뉴욕 날씨 어때?"
```

> **💡 `run.sh`가 자동으로 처리하는 것들:**
> - 가상환경 생성 (venv)
> - 의존성 설치 (requirements.txt)
> - 애플리케이션 실행
 
## 사용 예제

### 🆕 모호한 요청의 Interactive 처리
```
입력: "커피"

🤖 커피에 대해 어떤 정보를 원하시나요?
   - 커피의 역사나 종류에 대한 일반적인 정보
   - 커피 브랜드 추천
   - 커피 만드는 방법이나 레시피
   - 특정 지역의 커피 문화

추가 입력: "역사 알려줘"

→ "커피 - 역사 알려줘"로 재처리하여 Wikipedia 검색 실행
```

### 🆕 지능적 검색 시스템
```
입력: "Albert Einstein"

📋 SUPER AGENT 실행 계획
====================================
**📋 실행 계획:**
1. search_agent - 아인슈타인에 대한 검색
   - 분석: 역사적 인물 → Wikipedia 우선 선택
   - 필요시 DuckDuckGo로 보완

**🎯 예상 결과:**
아인슈타인의 생애, 업적, 이론 등 포괄적 정보
====================================

→ LLM이 질문 성격을 분석하여 최적 도구 선택
```

### 🎯 검색 도구 선택 로직
```
📚 Wikipedia 우선 선택:
- "Napoleon Bonaparte" (역사적 인물)
- "quantum mechanics" (과학 개념)  
- "Renaissance period" (역사적 시대)
- "France geography" (지역 정보)

🦆 DuckDuckGo 우선 선택:
- "what is API" (기술 정의)
- "React framework" (현대 기술)
- "machine learning definition" (현대 개념)
- "cloud computing basics" (최신 기술)

🔄 상호 보완 예시:
- Wikipedia 실패 → DuckDuckGo로 보완
- 결과 부족 → 다른 도구 추가 검색
```

### 복합 요청 처리
```
입력: "파리에 대해 알려주고 날씨도 알려줘"

📋 ORCHESTRATOR AGENT 실행 계획
====================================
**📋 실행 계획:**
1. search_agent - 파리에 대한 기본 정보 검색
2. weather_agent - 파리 날씨 정보 조회 시도
3. conversation_agent - 결과 종합 및 사용자 친화적 응답

**🎯 예상 결과:**
파리의 기본 정보와 날씨 정보를 종합한 답변

**⚠️ 주의사항:**
날씨 API는 미국 지역만 지원하므로 파리 날씨는 제한적
====================================

→ 계획에 따라 각 에이전트가 순차 실행
```

## 파일 구조

```
strands/
├── main.py                 # 메인 애플리케이션
├── orchestrator_agent.py   # Orchestrator Agent (오케스트레이터)
├── sub_agents.py          # Sub Agents (@tool)
├── model_config.py        # 모델 설정
├── mcp_tools.py          # MCP 도구들
├── workshop_test.py      # 워크샵용 테스트 스크립트
├── requirements.txt      # 의존성
├── run.sh               # 실행 스크립트
└── README.md            # 이 파일
```

## 개발 가이드

### 새로운 하위 에이전트 추가

1. `sub_agents.py`에 새 에이전트 함수 추가:
```python
@tool
def new_agent(query: str) -> str:
    """새로운 하위 에이전트"""
    agent = Agent(
        system_prompt="하위 에이전트 전문 영역 프롬프트",
        tools=[필요한_도구들]
    )
    response = agent(query)
    return str(response)
```

2. `orchestrator_agent.py`에서 새 에이전트 import 및 추가:
```python
from sub_agents import ..., new_agent

# tools 리스트에 추가
tools=[..., new_agent]
```

### 모델 변경

`model_config.py`에서 사용할 모델 설정:
```python
MODEL_PROVIDER = "anthropic"  # 또는 "bedrock"
MODEL_ID = "claude-3-5-sonnet-20241022"
```
 

## 지원 기능

- ✅ **지능적 검색 시스템**
  - Wikipedia 검색 (백과사전적 정보)
  - DuckDuckGo 검색 (실시간 웹 정보)
  - LLM 기반 최적 도구 선택
  - 결과 부족 시 자동 보완 검색
  - 날씨 정보 (미국 지역) 

## 제한사항
- 모든 검색 키워드는 영문으로 작성. (API들이 미국서비스)
- 날씨 API는 미국 지역만 지원
- Wikipedia 검색은 영어 위주

## 🆕 Interactive 기능 상세

### LLM 기반 명확성 판단
- **하드코딩 없음**: 키워드 리스트나 규칙 기반이 아닌 LLM이 직접 판단
- **매우 모호한 요청만 질문**: LLM이 "매우 모호함"으로 판단한 경우에만 추가 정보 요청
- **대부분의 요청은 바로 처리**: LLM이 "처리 가능"으로 판단하면 바로 실행

### 대화 흐름
1. **LLM 직접 판단**: Super Agent가 사용자 요청의 명확성을 LLM에게 질의
2. **매우 모호한 경우**: 추가 정보 요청 → 사용자 응답 대기 → 결합하여 재처리
3. **처리 가능한 경우**: 바로 실행 계획 수립 및 실행

### 판단 예시
```
"커피" → LLM 판단 → NEED_MORE → 질문
"ice coffee" → LLM 판단 → PROCEED → 바로 실행
"파리" → LLM 판단 → PROCEED → 바로 실행
"뉴욕 날씨" → LLM 판단 → PROCEED → 바로 실행
```
 
