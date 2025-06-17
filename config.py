"""워크샵용 설정 파일 - 단순화"""

# API 설정
NOMINATIM_USER_AGENT = "WorkshopAgents/1.0"
WIKIPEDIA_LANGUAGE = "en"
HTTP_TIMEOUT = 10.0

# 에이전트 설정
AGENT_CONFIG = {
    "search": {
        "name": "search_agent",
        "timeout": 30,
        "max_retries": 2
    },
    "weather": {
        "name": "weather_agent", 
        "timeout": 30,
        "max_retries": 2,
        "supported_regions": ["미국", "US", "USA"]
    },
    "extra": {
        "name": "extra_agent",
        "timeout": 15,
        "max_retries": 1
    },
    "super": {
        "name": "super_agent",
        "timeout": 60,
        "max_retries": 2
    }
}

# 메모리 설정
MEMORY_CONFIG = {
    "max_memories": 50,
    "summary_threshold": 5,  # 5개 이상이면 요약
    "auto_cleanup": True
}

# 응답 형식 설정
RESPONSE_CONFIG = {
    "include_metadata": True,
    "include_timestamps": False,  # 워크샵에서는 단순화
    "format": "json"
}

# 로그 설정
LOG_CONFIG = {
    "use_emojis": True,
    "show_progress": True,
    "verbose": True
}

# 워크샵 설정
WORKSHOP_CONFIG = {
    "interactive_mode": True,
    "show_help": True,
    "demo_queries": [
        "서울에 대해 알려줘",
        "뉴욕 날씨는?", 
        "hello",
        "부산 정보"
    ]
}
