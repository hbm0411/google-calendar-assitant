from typing import Dict, Optional

class SessionManager:
    def __init__(self):
        self.user_sessions: Dict[str, str] = {}

    def get_previous_response_id(self, user_id: str) -> Optional[str]:
        return self.user_sessions.get(user_id)

    def set_previous_response_id(self, user_id: str, response_id: str):
        self.user_sessions[user_id] = response_id
