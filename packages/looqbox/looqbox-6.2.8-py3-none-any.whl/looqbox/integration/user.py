
class User:

    def __init__(self, id=None, group=None, login=None):
        self.id: int | str | None = id
        self.group: int | str | None = group
        self.login: str | None = login
