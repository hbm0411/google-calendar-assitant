#!/usr/bin/env python3
"""
Google Calendar Assistant 웹 서버 실행 스크립트
"""

import uvicorn
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

if __name__ == "__main__":
    print("🚀 Google Calendar Assistant 서버를 시작합니다...")
    print("📱 웹 브라우저에서 http://localhost:8000 으로 접속하세요")
    print("🛑 서버를 종료하려면 Ctrl+C를 누르세요")
    print("-" * 50)
    
    # 개발 모드로 서버 실행
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 코드 변경 시 자동 재시작
        log_level="info"
    ) 