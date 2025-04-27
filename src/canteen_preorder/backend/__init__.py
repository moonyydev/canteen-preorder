import sqlite3

class PreorderBackend:
    def __init__(self, db_path: str = "canteen.db") -> None:
        self.db = sqlite3.connect(db_path)
