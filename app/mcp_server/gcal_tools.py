from googleapiclient.discovery import build
from google.oauth2 import service_account
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service-account.json')

class GCalTools:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_events(self, calendar_id: str = 'primary', max_results: int = 10) -> List[Dict]:
        events_result = self.service.events().list(
            calendarId=calendar_id, maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def create_event(self, calendar_id: str = 'primary', event: Optional[Dict] = None) -> Dict:
        if event is None:
            raise ValueError('event 데이터가 필요합니다.')
        created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        return created_event

# .env 파일 예시:
# GOOGLE_SERVICE_ACCOUNT_FILE=/Users/yourname/path/to/service-account.json
