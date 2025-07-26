import jwt
from datetime import datetime, timedelta
from typing import Dict, Any


class JWTService:
    def __init__(self, secret_key: str, algorithm: str, expiration_minutes: int):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expiration_minutes = expiration_minutes

    def create_token(self, user_id: str, session_id: str) -> str:
        """Create JWT token"""
        payload = {
            "user_id": user_id,
            "session_id": session_id,
            "exp": datetime.utcnow() + timedelta(minutes=self._expiration_minutes),
            "iat": datetime.utcnow(),
        }

        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode JWT token"""
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
