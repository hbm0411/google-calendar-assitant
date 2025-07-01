from responses_client import ResponsesClient
from session_manager import SessionManager
import datetime
import os

def main():
    # 환경 변수에서 API 키/URL 로드
    RESPONSES_API_KEY = os.getenv('RESPONSES_API_KEY', 'your-api-key')
    RESPONSES_API_URL = os.getenv('RESPONSES_API_URL', 'https://api.openai.com/v1/responses')
    USER_ID = 'test_user'  # 예시 유저 ID
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'path/to/service_account_file.json')

    # 인스턴스 생성
    responses_client = ResponsesClient(RESPONSES_API_KEY, RESPONSES_API_URL)
    session_manager = SessionManager()

    # 이전 response_id 조회
    previous_response_id = session_manager.get_previous_response_id(USER_ID)

    # 프롬프트 예시
    prompt = '내일 오전 10시에 "AI 프로젝트 미팅" 일정을 구글 캘린더에 추가해줘.'

    # Responses API 호출
    response = responses_client.send_request(
        prompt=prompt,
        previous_response_id=previous_response_id
    )
    print('Responses API 응답:', response)

    # 응답에서 response_id 추출 및 세션에 저장
    response_id = response.get('id')
    if response_id:
        session_manager.set_previous_response_id(USER_ID, response_id)

if __name__ == '__main__':
    main()
