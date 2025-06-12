# Multi-Agent System with Strands Agents

이 프로젝트는 **Strands Agents SDK**를 사용하여 구현된 다중 에이전트 시스템입니다.

## [*] 시스템 구조

### 에이전트들
1. **Weather Forecaster Agent**: 위도/경도를 받아 날씨 정보를 반환
2. **Search Agent**: 지역명을 받아 Wikipedia 정보와 좌표를 반환
3. **Extra Agent**: 간단한 "hello" 메시지를 반환
4. **Super Agent**: 모든 에이전트를 조정하고 결과를 통합

### MCP 도구들 (Strands Tools)
1. **get_position**: 지역명을 위도/경도로 변환하는 도구
2. **wikipedia_search**: Wikipedia API를 사용한 지역 정보 검색 도구

### [*] LLM Foundation Model 지원
- **Amazon Bedrock** (기본값): Nova Pro, Claude 3.5 Sonnet 등

## [*] 설치 및 실행

### 1. 의존성 설치
```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

자세한 모델 설정은 [MODEL_SETUP.md](MODEL_SETUP.md)를 참조하세요.

### 2. 실행 방법

#### 실행 스크립트 사용
```bash
./run.sh "서울?"
```

#### 대화형 모드
```bash
python main.py
```

#### 단일 쿼리 실행
```bash
python main.py "서울"
```


### 3. 테스트 실행
```bash
python test_agents.py
```

## [*] 응답 형식

모든 응답은 LLM 응답과 WEB UI 처리를 위한 다음과 같은 JSON 형식으로 반환됩니다:

```json
{
  "success": true,
  "agent": "super_agent",
  "model_info": {
    "provider": "BedrockModel",
    "model_id": "us.amazon.nova-pro-v1:0"
  },
  "user_input": "Seoul",
  "timestamp": "2025-06-12T16:41:25.013932",
  "llm_synthesis": "종합된 AI 응답...",
  "agents_called": ["search", "weather_forecaster"],
  "agent_results": {
    "search": {
      "success": true,
      "agent": "search",
      "query": "Seoul",
      "wikipedia_info": {...},
      "position_info": {...}
    },
    "weather_forecaster": {
      "success": true,
      "agent": "weather_forecaster",
      "data": {...}
    }
  },
  "summary": {
    "query": "Seoul",
    "wikipedia_found": true,
    "coordinates_found": true,
    "weather_available": true,
    "overall_success": true,
    "intelligent_selection": true
  }
}
```

## [*] 구성 요소

### 파일 구조
```
strands/
├── main.py              # 메인 애플리케이션
├── super_agent.py       # 슈퍼 에이전트
├── agents.py            # 개별 에이전트들
├── agent_planner.py     # 지능적 에이전트 계획자
├── mcp_tools.py         # Tools (MCP 도구들)
├── model_config.py      # LLM 모델 설정
├── config.py            # 일반 설정 파일
├── test_agents.py       # 테스트 스크립트
├── run.sh              # 실행 스크립트
├── requirements.txt     # 의존성 목록
├── .env.example        # 환경 변수 예제
├── MODEL_SETUP.md      # 모델 설정 가이드
└── README.md           # 이 파일
```

## [+] 주요 기능

1. **지능적 에이전트 선택**: LLM이 사용자 요청을 분석하여 필요한 에이전트만 실행
2. **LLM 기반 문맥 이해**: 패턴 매칭이 아닌 LLM을 통한 자연어 이해
3. **다양한 LLM 지원**: Amazon Bedrock 모델들 지원
4. **Strands Tools 통합**: @tool 데코레이터를 사용한 도구 구현
5. **LLM 종합 응답**: 모든 에이전트 결과를 LLM이 종합하여 자연어 응답 생성
6. **표준화된 JSON 응답**: 모든 응답이 일관된 형식으로 제공
7. **모델 정보 추적**: 각 응답에 사용된 모델 정보 포함
8. **한글 지원**: 한국어 프롬프트 및 응답 지원
9. **이모지 없는 출력**: 모든 PC 환경에서 호환 가능

## [*] 작동 흐름

1. 사용자가 쿼리 입력 (예: "서울 날씨")
2. Agent Planner가 LLM을 통해 필요한 에이전트 결정
3. 선택된 에이전트들만 순차 실행:
   - Search Agent: Wikipedia 및 Position 도구 사용
   - Weather Agent: 좌표 기반 날씨 정보 생성
4. Super Agent가 모든 결과를 LLM으로 종합
5. 사용자 친화적인 자연어 응답 생성

## [*] 테스트 결과

### 날씨 검색 ("서울 날씨는?")
- [+] LLM Planning: search + weather 에이전트 선택
- [+] Search Agent: 서울 좌표 정보 획득 성공
- [+] Weather Agent: LLM 기반 날씨 정보 생성 성공
- [+] Super Agent: 종합적인 한국어 응답 생성
- [+] 모델 정보 추적 (BedrockModel, us.amazon.nova-pro-v1:0)

### 일반 검색 ("서울")
- [+] LLM Planning: search 에이전트만 선택
- [+] Search Agent: 서울 정보 수집 성공
- [+] Weather Agent: 실행 안됨 (불필요)
- [+] Extra Agent: 실행 안됨 (불필요)

### 인사말 ("hello")
- [+] LLM Planning: extra 에이전트만 선택
- [+] Extra Agent: 친근한 응답 생성
- [+] 다른 에이전트들: 실행 안됨 (불필요)

## [*] 기술 스택

- **Strands Agents 0.1.7**: 메인 에이전트 프레임워크
- **Strands Agents Tools**: 추가 도구 패키지
- **Amazon Bedrock**: (Nova Pro, Claude 등)
- **Wikipedia API**: 지역 정보 검색
- **OpenStreetMap Nominatim**: 위경도 가져오기 지오코딩 서비스
- **httpx**: 비동기 HTTP 클라이언트
- **Pydantic**: 데이터 검증
- **python-dotenv**: 환경 변수 관리

## [*] 커스터마이징

- `.env` 파일에서 MODEL_ID 설정으로 Bedrock 모델 변경
- `model_config.py`에서 모델 구성 수정
- `mcp_tools.py`에서 새로운 도구 추가 (@tool 데코레이터 사용)
- `agents.py`에서 새로운 에이전트 구현
- `agent_planner.py`에서 에이전트 선택 로직 수정
- `super_agent.py`에서 에이전트 조정 로직 수정

## [*] 참고사항

- **기본 모델**: Amazon Bedrock Nova Pro (AWS 자격 증명 필요)
- **Wikipedia API**: 무료 사용 가능
- **날씨 정보**: LLM 생성 모의 데이터 사용
- **지오코딩**: OpenStreetMap Nominatim API 사용 (무료)
- **Bedrock 액세스**: AWS 콘솔에서 모델 액세스 권한 활성화 필요

## [>] 실행 예제

```bash
# 프로젝트 디렉토리로 이동
cd /Users/jikjeong/Develop/python/strands

# 가상환경 활성화
source venv/bin/activate

# 기본 Nova Pro 모델로 서울 정보 검색
python main.py "서울"

# Claude 3.5 Sonnet 모델로 실행
MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0 python main.py "부산 날씨"

# 대화형 모드 실행
python main.py
```

## [*] 실행 시 출력 예제

```
[*] 사용 중인 모델: BedrockModel, 모델 ID: us.amazon.nova-pro-v1:0
[*] 제공자: bedrock
==================================================

[*] 입력 처리 중: '서울 날씨'
==================================================
[*] 에이전트 조정 시작...
[*] 실행 계획 생성 중...
[*] 선택된 에이전트: search, weather
[>] SEARCH 에이전트 실행 중...
[+] SEARCH 에이전트 완료
[>] WEATHER 에이전트 실행 중...
[+] WEATHER 에이전트 완료
[*] 완료: search, weather

[*] AI 어시스턴트 응답:
==================================================
서울 날씨에 대한 종합적인 정보를 제공해드리겠습니다...
```

이제 완전히 작동하는 **지능적 다중 에이전트 시스템**이 준비되었습니다!
