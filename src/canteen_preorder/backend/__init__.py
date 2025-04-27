import sqlite3

class PreorderBackend:
    def __init__(self, db_path: str = "canteen.db") -> None:
        self.db = sqlite3.connect(db_path)
        self.__prepare()
    
    def __prepare(self) -> None:
        cur = self.db.cursor()
        cur.execute("""
        create table if not exists users (
            id int primary key,
            name text not null,
            email text not null unique,
            password text not null,
            staff int
        );
        """)

        cur.execute("""
        create table if not exists meals (
            id int primary key,
            name text not null unique,
            cost int not null,
            category int not null,
            stock int not null,
            available int not null
        );
        """)

        cur.execute("""
        create table if not exists orders (
            id int primary key,
            user int not null,
            order_time int not null,
            data text not null
        );
        """)

        self.db.commit()
