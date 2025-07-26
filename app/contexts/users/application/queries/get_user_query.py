from app.shared.application.query_bus import Query


class GetUserQuery(Query):
    def __init__(self, user_id: str):
        self.user_id = user_id
