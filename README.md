# Google Calendar Assistant
이 프로젝트는 Google Calendar MCP와 Responses API를 연동하는 Python 3 기반의 프로젝트입니다.

## 주요 기능
- Google Calendar와의 연동
- Responses API를 통한 자동화 및 응답 처리

## 설치 방법
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 환경 변수 및 .env 파일 설정
Google 서비스 계정 키 파일 경로를 .env 파일에 지정해야 합니다.

```

RESPONSES_API_KEY=your-openaiGOOGLE_SERVICE_ACCOUNT_FILE=/Users/yourname/path/to/service-account.json-api-key
RESPONSES_API_URL=https://api.openai.com/v1/responses
```

## 실행 방법
1. `.env` 파일을 프로젝트 루트에 생성하고 위 예시처럼 환경변수를 설정하세요.
2. 가상환경을 활성화하고 패키지를 설치하세요.
3. 아래 명령어로 main 함수를 실행하면 Responses API와 Google Calendar가 연동됩니다.

```bash
python app/main.py
```

실행 결과로 OpenAI Responses API의 응답과, 생성된 Google Calendar 이벤트의 링크가 출력됩니다.

## 프로젝트 구조
- `main.py`: 진입점 스크립트 (맥락 유지, Responses API 호출, Google Calendar 이벤트 생성)
- `mcp_server/`: Google Calendar 및 MCP 관련 모듈
  - `app.py`: 서버 실행 및 라우팅
  - `gcal_tools.py`: Google Calendar 연동 도구
- `responses_client.py`: Responses API 연동 클라이언트
- `session_manager.py`: 세션 관리 모듈

