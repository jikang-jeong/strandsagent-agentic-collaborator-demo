"""워크샵용 모델 설정 """
import os
from strands.models import BedrockModel


def get_configured_model(model_id: str = None) -> BedrockModel:
    """워크샵용 Bedrock 모델 설정
    
    Args:
        model_id: 사용할 모델 ID (선택사항)
        
    Returns:
        설정된 BedrockModel 인스턴스
    """
    # 모델 ID 결정 (우선순위: 파라미터 > 환경변수 > 기본값)
    final_model_id = (
        model_id or 
        os.getenv("MODEL_ID") or 
        "us.amazon.nova-pro-v1:0"
    )
    
    # AWS 리전 설정
    region = os.getenv("AWS_REGION", "us-west-2")
    
    # Bedrock 모델 생성
    model = BedrockModel(
        model_id=final_model_id,
        region=region,
        temperature=0.7,
        max_tokens=4096,
        streaming=False  # 워크샵에서는 스트리밍 비활성화
    )
    
    # 모델 ID 속성 추가 (호환성)
    if not hasattr(model, 'model_id'):
        model.model_id = final_model_id
    
    return model


# 환경 정보 (표시용)
MODEL_PROVIDER = "bedrock"
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-pro-v1:0")

# 지원되는 모델 목록 (워크샵 참고용)
SUPPORTED_MODELS = {
    "nova_pro": "us.amazon.nova-pro-v1:0",
    "claude_sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "claude_haiku": "anthropic.claude-3-haiku-20240307-v1:0"
}


def get_model_info(model_id: str = None) -> dict:
    """모델 정보 반환"""
    current_model_id = model_id or MODEL_ID
    
    model_names = {
        "us.amazon.nova-pro-v1:0": "Amazon Nova Pro",
        "anthropic.claude-3-5-sonnet-20241022-v2:0": "Claude 3.5 Sonnet",
        "anthropic.claude-3-haiku-20240307-v1:0": "Claude 3 Haiku"
    }
    
    return {
        "model_id": current_model_id,
        "model_name": model_names.get(current_model_id, "Unknown Model"),
        "provider": MODEL_PROVIDER,
        "region": os.getenv("AWS_REGION", "us-west-2")
    }
