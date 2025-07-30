import requests
from typing import Optional, Union
import datetime
import json
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('responses_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ResponsesClient:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def send_request(
        self,
        message: Union[str, list],
        previous_response_id: Optional[str] = None,
        approval_request_id: Optional[str] = None,
        file_id: Optional[str] = None
    ) -> dict:
        logger.info(f"=== 새로운 요청 시작 ===")
        logger.info(f"메시지: {message}")
        logger.info(f"이전 응답 ID: {previous_response_id}")
        logger.info(f"승인 요청 ID: {approval_request_id}")
        logger.info(f"파일 ID: {file_id}")
        
        # 오늘 날짜 가져오기
        today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        
        # 사용자 메시지 구성
        user_content = message
        if file_id:
            # 이미지가 있는 경우 content 배열로 구성
            user_content = [
                {"type": "input_text", "text": message},
                {"type": "input_image", "file_id": file_id}
            ]
        
        data = { 
            "model": "gpt-4.1",
            "truncation": "auto",
            "max_output_tokens": 2000,
            "input": [
                {
                    "role": "developer",
                    "content": f"""당신은 스타벅스 매장의 근무 일정을 관리하는 AI 비서입니다.
스타벅스 파트너가 입력한 근무 일정을 구글 캘린더에 입력할 수 있도록 해야합니다.

## 구글 캘린더 설정:
- 캘린더 ID: "bog3g93erjt6fqp52njd88ekro@group.calendar.google.com"
- 모든 일정은 이 캘린더에 추가/수정/삭제됩니다.

## 일정 이름 규칙:
- 일정이 6시 ~ 8시59분 사이인 경우 일정 이름을 "오픈"으로 설정
- 일정이 9시1분 ~ 13시 사이인 경우 일정 이름을 "미들"로 설정  
- 일정이 13시 이후인 경우 일정 이름을 "마감"으로 설정
- 시간대신 "정규휴일"이 입력된 경우 일정 이름을 "휴일"로 설정하고 하루종일로 설정

## 일정 입력 규칙:
- 일정을 추가할 때는 이름, 날짜, 시간만 입력
- 위치(location)와 비고(description)는 입력하지 않음
- 구글 캘린더 도구 사용 시 location과 description 필드는 빈 문자열("")로 설정 (null 대신)
- "정규휴일" 입력 시 시간 없이 하루종일(all-day) 이벤트로 설정

## 주요 역할:
1. 스타벅스 파트너가 입력한 근무 일정을 지정된 구글 캘린더에 자동으로 추가
2. 시간대에 따라 적절한 일정 이름("오픈", "미들", "마감") 자동 설정
3. 근무 일정 조회, 수정, 삭제 요청 처리
4. 스타벅스 매장의 효율적인 근무 일정 관리 지원

## 응답 방식:
- 사용자의 요청을 정확히 이해하고 구글 캘린더 도구를 사용하여 처리
- 근무 일정 추가 시 시간대에 맞는 이름을 자동으로 설정
- 일정 추가 시 이름, 날짜, 시간만 입력하고 위치와 비고는 제외
- 명확하고 친근한 한국어로 응답
- 스타벅스 파트너에게 친근하고 전문적인 톤으로 대화
- 오류 발생 시 사용자에게 명확히 안내
- 일정 조회 시 markdown 표 형식으로 응답
- 이미지가 포함된 경우 이미지에서 근무 일정 정보를 추출하여 처리

## 일정 조회 규칙:
- 일정 조회 시 max_results는 최소 10개 이상으로 설정 (기본값: 10)
- 날짜 범위는 사용자 요청에 따라 적절히 설정:
  * "오늘 일정" → 오늘 00:00 ~ 23:59
  * "내일 일정" → 내일 00:00 ~ 23:59  
  * "이번 주 일정" → 이번 주 월요일 00:00 ~ 일요일 23:59
  * "다음 주 일정" → 다음 주 월요일 00:00 ~ 일요일 23:59
  * "이번 달 일정" → 이번 달 1일 00:00 ~ 말일 23:59
  * 구체적인 날짜 요청 시 → 해당 날짜 00:00 ~ 23:59
- 조회 결과가 없을 경우 "해당 기간에 등록된 일정이 없습니다"라고 안내
- 조회 결과가 있을 경우 markdown 표로 정리하여 응답

## 이전 발화 참조 처리:
- 사용자가 "조금 전에 추가한 일정", "직전에 얘기한 일정", "방금 추가한 일정" 등 이전 발화를 참조하는 경우:
  * 이전 대화에서 추가된 일정의 날짜를 파악하여 해당 날짜로 조회
  * 예: "조금 전에 추가한 일정 보여줘" → 이전에 추가한 일정의 날짜로 조회
  * 예: "직전에 얘기한 일정 정보 알려줘" → 이전 대화에서 언급된 날짜로 조회
  * 이전 발화에서 명확한 날짜를 찾을 수 없는 경우, 오늘 날짜로 조회
- 이전 발화 참조 시에도 max_results는 10개 이상으로 설정하여 충분한 결과 확인

오늘은 {today}입니다."""
                },
                {
                    "role": "user",
                    "content": user_content,
                },
            ],
            "tools": [{
                "type": "mcp",
                "server_label": "google_calendar",
                "server_url": "https://gcalendar-mcp-server.klavis.ai/mcp/?instance_id=5da0238c-d022-45e4-bdd3-e202fe385f69",
                "require_approval": "never"
            }],
        }
        # MCP 승인 시스템 처리
        # 첫 번째 요청: 사용자가 "일정 추가해줘"라고 요청
        #   data["input"] = [
        #       {"role": "developer", "content": "당신은 스타벅스..."},
        #       {"role": "user", "content": "오늘 9시부터 5시까지 근무 일정 추가해줘"}
        #   ]
        #
        # 두 번째 요청: AI가 구글 캘린더 도구 사용을 위해 승인 요청
        #   data["input"] = [{
        #       "type": "mcp_approval_response",
        #       "approve": True,
        #       "approval_request_id": "some_id"
        #   }]
        if previous_response_id and approval_request_id:
            data["previous_response_id"] = previous_response_id
            # 승인 응답이 필요한 경우, 원래 사용자 메시지를 승인 응답으로 덮어씀
            data["input"] = [{
                "type": "mcp_approval_response",
                "approve": True,
                "approval_request_id": approval_request_id
            }]
        elif previous_response_id:
            data["previous_response_id"] = previous_response_id
            
        # 요청 데이터 로깅
        logger.info(f"=== API 요청 데이터 ===")
        logger.info(f"URL: {self.api_url}")
        logger.info(f"Headers: {json.dumps(headers, indent=2, ensure_ascii=False)}")
        logger.info(f"Request Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(self.api_url, json=data, headers=headers)
            logger.info(f"=== API 응답 정보 ===")
            logger.info(f"상태 코드: {response.status_code}")
            logger.info(f"응답 헤더: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error(f"API 오류 발생!")
                logger.error(f"상태 코드: {response.status_code}")
                logger.error(f"응답 내용: {response.text}")
                response.raise_for_status()
                
            result = response.json()
            logger.info(f"응답 데이터: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"=== API 요청 중 예외 발생 ===")
            logger.error(f"예외 타입: {type(e).__name__}")
            logger.error(f"예외 메시지: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"=== JSON 파싱 오류 ===")
            logger.error(f"응답 내용: {response.text}")
            logger.error(f"JSON 오류: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"=== 예상치 못한 오류 ===")
            logger.error(f"오류 타입: {type(e).__name__}")
            logger.error(f"오류 메시지: {str(e)}")
            raise
        # output 리스트 중 content.type이 'output_text'인 content.text만 로깅
        logger.info(f"=== 응답 내용 분석 ===")
        output_list = result.get('output', [])
        for i, output in enumerate(output_list):
            logger.info(f"출력 {i+1}: {json.dumps(output, indent=2, ensure_ascii=False)}")
            contents = output.get('content', [])
            if isinstance(contents, list):
                for j, content in enumerate(contents):
                    if content.get('type') == 'output_text':
                        logger.info(f'[응답 output_text {j+1}] {content.get("text")}')
        
        logger.info(f"=== 요청 완료 ===")
        return result
