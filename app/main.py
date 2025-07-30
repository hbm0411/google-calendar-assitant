from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .responses_client import ResponsesClient
from .session_manager import SessionManager
import datetime
import os
import json
from typing import Optional

app = FastAPI(title="Google Calendar Assistant", version="1.0.0")

# 템플릿과 정적 파일 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 환경 변수에서 API 키/URL 로드
RESPONSES_API_KEY = os.getenv('RESPONSES_API_KEY', 'your-api-key')
RESPONSES_API_URL = os.getenv('RESPONSES_API_URL', 'https://api.openai.com/v1/responses')

# 인스턴스 생성
responses_client = ResponsesClient(RESPONSES_API_KEY, RESPONSES_API_URL)
session_manager = SessionManager()

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """채팅 페이지를 렌더링합니다."""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/send_message")
async def send_message(message: str = Form(...), user_id: str = Form("test_user")):
    """사용자 메시지를 받아서 응답을 반환합니다."""
    try:
        # 이전 response_id 조회
        previous_response_id = session_manager.get_previous_response_id(user_id)
        
        # Responses API 호출
        response = responses_client.send_request(
            message=message,
            previous_response_id=previous_response_id
        )
        
        # 응답에서 response_id 추출 및 세션에 저장
        response_id = response.get('id')
        if response_id:
            session_manager.set_previous_response_id(user_id, response_id)
        
        return {
            "success": True,
            "response": response,
            "message": message
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": message
        }

@app.get("/health")
async def health_check():
    """서버 상태 확인용 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
