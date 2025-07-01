import requests
from typing import Optional, Union

class ResponsesClient:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def send_request(
        self,
        prompt: Union[str, list],
        previous_response_id: Optional[str] = None,
        approval_request_id: Optional[str] = None
    ) -> dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            "model": "gpt-4.1",
            "input": [
                {
                    "role": "developer",
                    "content": "You are a helpful assistant that can help with tasks related to Google Calendar."
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "tools": [{
                "type": "mcp",
                "server_label": "google_calendar",
                "server_url": "https://gcalendar-mcp-server.klavis.ai/mcp/?instance_id=2ed548b8-080a-4c26-aaae-a0ec7dc5b567",
                "require_approval": "never"
            }],
        }
        if previous_response_id and approval_request_id:
            data["previous_response_id"] = previous_response_id
            data["input"] = [{
                "type": "mcp_approval_response",
                "approve": True,
                "approval_request_id": approval_request_id
            }]
        else:
            data["input"] = prompt
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
