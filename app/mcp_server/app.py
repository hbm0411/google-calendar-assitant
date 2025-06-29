from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.responses_client import ResponsesClient
from app.session_manager import SessionManager
import os

app = FastAPI()

# 환경 변수 또는 하드코딩으로 API 키/URL 설정
RESPONSES_API_KEY = os.getenv('RESPONSES_API_KEY', 'your-api-key')
RESPONSES_API_URL = os.getenv('RESPONSES_API_URL', 'https://api.openai.com/v1/responses')

responses_client = ResponsesClient(RESPONSES_API_KEY, RESPONSES_API_URL)
session_manager = SessionManager()

class UserRequest(BaseModel):
    user_id: str
    prompt: str

@app.post('/ask')
def ask_gpt(request: UserRequest):
    previous_response_id = session_manager.get_previous_response_id(request.user_id)
    response = responses_client.send_request(
        prompt=request.prompt,
        previous_response_id=previous_response_id
    )
    # 응답에서 response_id 추출(실제 응답 구조에 맞게 수정 필요)
    response_id = response.get('id')
    if response_id:
        session_manager.set_previous_response_id(request.user_id, response_id)
    return response
