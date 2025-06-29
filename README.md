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

## 사용법
```bash
python main.py
```

## 프로젝트 구조
- `main.py`: 진입점 스크립트
- `mcp_server/`: Google Calendar 및 MCP 관련 모듈
  - `app.py`: 서버 실행 및 라우팅
  - `gcal_tools.py`: Google Calendar 연동 도구
- `responses_client.py`: Responses API 연동 클라이언트
- `session_manager.py`: 세션 관리 모듈

