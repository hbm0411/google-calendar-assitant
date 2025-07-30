from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .responses_client import ResponsesClient
from .session_manager import SessionManager
import datetime
import os
import json
import requests
from typing import Optional

app = FastAPI(title="Google Calendar Assistant", version="1.0.0")

# 템플릿과 정적 파일 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 환경 변수에서 API 키/URL 로드
OPEN_API_KEY = os.getenv('RESPONSES_API_KEY', 'your-api-key')
RESPONSES_API_URL = os.getenv('RESPONSES_API_URL', 'https://api.openai.com/v1/responses')

# 인스턴스 생성
responses_client = ResponsesClient(OPEN_API_KEY, RESPONSES_API_URL)
session_manager = SessionManager()

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """채팅 페이지를 렌더링합니다."""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/send_message")
async def send_message(
    message: str = Form(...), 
    user_id: str = Form("test_user"),
    image: Optional[UploadFile] = File(None),
    previous_response_id: Optional[str] = Form(None)
):
    """사용자 메시지를 받아서 응답을 반환합니다."""
    try:
        print(f"=== 서버에서 메시지 수신 ===")
        print(f"메시지: {message}")
        print(f"이미지: {image}")
        print(f"이미지 파일명: {image.filename if image else 'None'}")
        print(f"이미지 타입: {image.content_type if image else 'None'}")
        
        # 이전 response_id 조회
        current_previous_response_id = session_manager.get_previous_response_id(user_id)
        if previous_response_id:
            current_previous_response_id = previous_response_id
        
        # 이미지 업로드 정보 수집
        image_upload_info = None
        file_id = None
        image_upload_error = None
        
        if image:
            print(f"이미지 업로드 시작: {image.filename}")
            try:
                file_id = await upload_image_to_openai(image)
                print(f"이미지 업로드 완료, file_id: {file_id}")
                
                # 이미지 업로드 성공 정보
                image_upload_info = {
                    "name": "openai_files_upload",
                    "arguments": json.dumps({
                        "filename": image.filename,
                        "content_type": image.content_type,
                        "file_size": "uploaded"
                    }, ensure_ascii=False),
                    "output": json.dumps({
                        "file_id": file_id,
                        "status": "success"
                    }, ensure_ascii=False),
                    "title": "이미지 업로드: OpenAI Files API"
                }
                
            except Exception as e:
                error_msg = f"이미지 업로드 실패: {str(e)}"
                print(error_msg)
                image_upload_error = error_msg
                
                # 이미지 업로드 실패 정보
                image_upload_info = {
                    "name": "openai_files_upload",
                    "arguments": json.dumps({
                        "filename": image.filename,
                        "content_type": image.content_type,
                        "file_size": "uploaded"
                    }, ensure_ascii=False),
                    "output": json.dumps({
                        "error": str(e),
                        "status": "failed"
                    }, ensure_ascii=False),
                    "title": "이미지 업로드: OpenAI Files API (실패)"
                }
        
        # 이미지 업로드 실패 시 에러 응답 반환
        if image_upload_error:
            return {
                "success": False,
                "error": image_upload_error,
                "message": message,
                "image_upload_failed": True,
                "image_upload_info": image_upload_info
            }
        
        # Responses API 호출
        response = responses_client.send_request(
            message=message,
            previous_response_id=current_previous_response_id,
            file_id=file_id
        )
        
        # 응답에서 response_id 추출 및 세션에 저장
        response_id = response.get('id')
        if response_id:
            session_manager.set_previous_response_id(user_id, response_id)
        
        return {
            "success": True,
            "response": response,
            "message": message,
            "image_upload_info": image_upload_info
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": message
        }

async def upload_image_to_openai(image: UploadFile) -> str:
    """이미지를 OpenAI Files API로 업로드합니다."""
    try:
        # 파일 업로드
        files = {
            'file': (image.filename, image.file, image.content_type),
            'purpose': (None, 'vision')
        }
        
        headers = {
            'Authorization': f'Bearer {OPEN_API_KEY}'
        }
        
        response = requests.post(
            'https://api.openai.com/v1/files',
            files=files,
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenAI Files API 오류: {response.status_code} - {response.text}")
        
        result = response.json()
        return result['id']
        
    except Exception as e:
        raise Exception(f"이미지 업로드 실패: {str(e)}")

@app.get("/health")
async def health_check():
    """서버 상태 확인용 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
