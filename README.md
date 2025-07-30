# 스타벅스 근무 일정 관리 시스템

이 프로젝트는 스타벅스 근무자의 일정을 자동으로 관리하는 Python 3 기반의 웹 애플리케이션입니다.

## 주요 기능
- Google Calendar와의 연동
- Responses API를 통한 자동화 및 응답 처리
- **스타벅스 근무 일정 자동 관리**: 시간대별 일정 이름 자동 설정
- 웹 기반 채팅 인터페이스
- 실시간 AI와의 대화를 통한 일정 관리
- 아름다운 모던 UI/UX

## 설치 방법
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 환경 변수 및 .env 파일 설정
Google 서비스 계정 키 파일 경로를 .env 파일에 지정해야 합니다.

```env
RESPONSES_API_KEY=your-openai-api-key
RESPONSES_API_URL=https://api.openai.com/v1/responses
GOOGLE_SERVICE_ACCOUNT_FILE=/Users/yourname/path/to/service-account.json
```

## 실행 방법

### 웹 애플리케이션 실행 (권장)
1. `.env` 파일을 프로젝트 루트에 생성하고 위 예시처럼 환경변수를 설정하세요.
2. 가상환경을 활성화하고 패키지를 설치하세요.
3. 아래 명령어로 웹 서버를 실행하세요:

```bash
python run_server.py
```

4. 웹 브라우저에서 `http://localhost:8000`으로 접속하세요.
5. 채팅 인터페이스를 통해 AI와 대화하며 일정을 관리할 수 있습니다.

### 기존 CLI 방식 실행
```bash
python app/main.py
```

## 웹 애플리케이션 기능

### 채팅 인터페이스
- 실시간 AI와의 대화
- 일정 추가, 수정, 조회 요청
- 아름다운 모던 UI
- 반응형 디자인 (모바일 지원)
- 로딩 인디케이터
- 에러 처리 및 사용자 피드백

### 사용 예시
- "내일 오전 7시에 근무 일정 추가해줘" → "오픈"으로 자동 설정
- "다음 주 월요일 오후 2시 근무" → "마감"으로 자동 설정
- "오늘 일정 보여줘"
- "이번 주 교대 일정 조회해줘"

## 프로젝트 구조
```
google-calendar-assistant/
├── app/
│   ├── main.py              # FastAPI 웹 서버
│   ├── responses_client.py  # Responses API 연동 클라이언트
│   └── session_manager.py   # 세션 관리 모듈
├── templates/
│   └── chat.html           # 채팅 인터페이스 템플릿
├── static/
│   ├── css/
│   │   └── style.css       # 스타일시트
│   └── js/
│       └── chat.js         # 채팅 기능 JavaScript
├── run_server.py           # 서버 실행 스크립트
├── requirements.txt        # Python 의존성
└── README.md              # 프로젝트 문서
```

## 기술 스택
- **Backend**: FastAPI, Python 3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Custom CSS (모던 디자인)
- **Icons**: Font Awesome
- **API**: OpenAI Responses API, Google Calendar API

## 3교대 근무 일정 규칙
- **오픈**: 06:00 ~ 08:00 시간대
- **미들**: 08:00 ~ 13:00 시간대  
- **마감**: 13:00 이후 시간대

## 개발 모드
서버는 개발 모드로 실행되며, 코드 변경 시 자동으로 재시작됩니다.

## 문제 해결
- 서버가 시작되지 않는 경우: 포트 8000이 사용 중인지 확인하세요
- API 오류: 환경 변수가 올바르게 설정되었는지 확인하세요
- Google Calendar 연동 오류: service-account.json 파일 경로를 확인하세요

