from app.shared.application.command_bus import Command


class LoginCommand(Command):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
