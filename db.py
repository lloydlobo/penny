import sqlite3


class DBHelper:
    """
    fieldnames = [
        "id",
        "amount",
        "category",
        "description",
        "timestamp",
    ]
    """

    # self.conn = None
    def __init__(self, dbname="db_penny.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)

    def create_connection(self):
        return sqlite3.connect(self.dbname)

    def close(self):
        if self.conn:
            self.conn.close()

    def setup(self):
        with self.conn:
            c = self.conn.cursor()
            c.execute(
                """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER, 
    user_id INTEGER, 
    amount REAL, 
    category TEXT, 
    description TEXT, 
    date TEXT 
    )"""
            )
        pass

    def add_expense(self, user_id, amount, category, description, date):
        with self.conn:
            pass
        pass
