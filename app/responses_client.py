import requests
from typing import Optional

class ResponsesClient:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def send_request(self, prompt: str, previous_response_id: Optional[str] = None) -> dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'prompt': prompt
        }
        if previous_response_id:
            data['previous_response_id'] = previous_response_id
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
