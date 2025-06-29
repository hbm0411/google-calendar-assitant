from app.mcp_server.gcal_tools import GCalTools
from app.responses_client import ResponsesClient
from app.session_manager import SessionManager
import datetime
import os

def main():
    # 환경 변수에서 API 키/URL 로드
    RESPONSES_API_KEY = os.getenv('RESPONSES_API_KEY', 'your-api-key')
    RESPONSES_API_URL = os.getenv('RESPONSES_API_URL', 'https://api.openai.com/v1/responses')
    USER_ID = 'test_user'  # 예시 유저 ID

    # 인스턴스 생성
    gcal = GCalTools()
    responses_client = ResponsesClient(RESPONSES_API_KEY, RESPONSES_API_URL)
    session_manager = SessionManager()

    # 이전 response_id 조회
    previous_response_id = session_manager.get_previous_response_id(USER_ID)

    # 프롬프트 예시
    prompt = '내일 오전 10시에 "AI 프로젝트 미팅" 일정을 구글 캘린더에 추가해줘.'

    # Responses API 호출
    response = responses_client.send_request(prompt=prompt, previous_response_id=previous_response_id)
    print('Responses API 응답:', response)

    # 응답에서 response_id 추출 및 세션에 저장
    response_id = response.get('id')
    if response_id:
        session_manager.set_previous_response_id(USER_ID, response_id)

    # (예시) 응답에서 이벤트 정보 추출 - 실제로는 OpenAI 응답 포맷에 맞게 파싱 필요
    # 여기서는 임의로 이벤트 정보를 생성
    event = {
        'summary': 'AI 프로젝트 미팅',
        'location': '온라인',
        'description': 'OpenAI Assistant가 생성한 이벤트',
        'start': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=10-datetime.datetime.utcnow().hour)).isoformat() + 'Z',
            'timeZone': 'Asia/Seoul',
        },
        'end': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=11-datetime.datetime.utcnow().hour)).isoformat() + 'Z',
            'timeZone': 'Asia/Seoul',
        },
        'attendees': [
            {'email': 'sample@example.com'},
        ],
    }
    created = gcal.create_event(event=event)
    print('생성된 Google Calendar 이벤트:', created.get('htmlLink'))

if __name__ == '__main__':
    main()
