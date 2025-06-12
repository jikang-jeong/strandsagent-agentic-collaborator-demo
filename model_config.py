"""Bedrock 모델 ID 변경을 위한 간단한 모델 구성"""
import os
from strands.models import BedrockModel


def get_configured_model(model_id: str = None) -> BedrockModel:
    """구성된 Bedrock 모델 가져오기
    
    Args:
        model_id: 사용할 모델 ID (선택사항)
        
    Returns:
        BedrockModel 인스턴스
    """
    # 기본 모델 ID 또는 환경 변수에서 가져오기
    default_model_id = model_id or os.getenv("MODEL_ID", "us.amazon.nova-pro-v1:0")
    
    # Bedrock 모델 생성
    model = BedrockModel(
        model_id=default_model_id,
        region=os.getenv("AWS_REGION", "us-west-2"),
        temperature=0.7,
        max_tokens=4096,
        streaming=True
    )
    
    # model_id에 접근 가능하도록 보장
    if not hasattr(model, 'model_id'):
        model.model_id = default_model_id
    return model


# 환경 변수에서 모델 제공자 정보 (표시용)
MODEL_PROVIDER = "bedrock"
MODEL_ID = os.getenv("MODEL_ID", "us.amazon.nova-pro-v1:0")
