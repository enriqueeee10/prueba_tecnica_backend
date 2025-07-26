from app.shared.application.query_bus import Query


class ValidateTokenQuery(Query):
    def __init__(self, token: str):
        self.token = token  # corregido con minúscula
