# Bedrock 모델 설정 가이드

이 문서는 **Amazon Bedrock** 모델 설정 방법을 설명합니다.

## 🎯 지원되는 모델

**Amazon Bedrock 모델:**
- `us.amazon.nova-pro-v1:0` (Amazon Nova Pro) - 기본값
- `us.amazon.nova-lite-v1:0` (Amazon Nova Lite)
- `anthropic.claude-3-5-sonnet-20241022-v2:0` (Claude 3.5 Sonnet)
- `anthropic.claude-3-haiku-20240307-v1:0` (Claude 3 Haiku)

## 🔧 설정 방법

### 1. 환경 변수 설정

`.env` 파일을 생성하여 모델 설정을 구성하세요:

```bash
cp .env.example .env
```

### 2. 모델 ID 변경

```bash
# .env 파일
MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
AWS_REGION=us-west-2
```

**필요한 설정:**
- AWS 자격 증명 구성 (`aws configure` 또는 IAM 역할)
- Bedrock 모델 액세스 권한 활성화

##  코드에서 모델 설정

### 환경 변수 사용 (권장)

```python
from main import MultiAgentApplication

# .env 파일의 설정을 자동으로 사용
app = MultiAgentApplication()
```

### 직접 모델 ID 지정

```python
from main import MultiAgentApplication

# Claude 3.5 Sonnet 사용
app = MultiAgentApplication("anthropic.claude-3-5-sonnet-20241022-v2:0")

# Nova Lite 사용
app = MultiAgentApplication("us.amazon.nova-lite-v1:0")
```

##  실행 예제

### 기본 Nova Pro 모델로 실행
```bash
python main.py "Seoul"
```

### 특정 모델로 실행
```bash
# Claude 3.5 Sonnet 사용
MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0 python main.py "Seoul"

# Nova Lite 사용
MODEL_ID=us.amazon.nova-lite-v1:0 python main.py "Seoul"
```

## 🔍 모델 정보 확인

실행 시 사용 중인 모델 정보가 표시됩니다:

```
[*] 사용 중인 모델: BedrockModel, 모델 ID: us.amazon.nova-pro-v1:0
[*] 제공자: bedrock
==================================================
```

## ️ 주의사항

1. **AWS 자격 증명**: AWS CLI 구성 또는 IAM 역할 필요
2. **모델 액세스**: Bedrock 콘솔에서 모델 액세스 권한 활성화 필요
3. **지역 설정**: 모델이 지원되는 지역 선택 (기본: us-west-2)
4. **비용 관리**: 모델 사용량 모니터링

## ️ 문제 해결

### AWS Bedrock 관련
- AWS 자격 증명 확인: `aws sts get-caller-identity`
- 모델 액세스 권한 확인: AWS Console > Bedrock > Model access
- 지역 확인: 모델이 해당 지역에서 지원되는지 확인
