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
            stmt = """
            CREATE TABLE IF NOT EXISTS expenses (
                uuid TEXT,
                user_id INTEGER, 
                amount REAL, 
                category TEXT, 
                description TEXT, 
                date TEXT
                )
            """
            c.execute(stmt)
        pass

    def add_expense(self, uuid, user_id, amount, category, description):
        with self.conn:
            c = self.conn.cursor()
            stmt = """
            INSERT INTO expenses ( uuid, user_id, amount, category, description, date) 
                VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """
            c.execute(
                stmt,
                (uuid, user_id, amount, category, description),
            )
        pass

    def get_expenses(self, user_id):
        with self.conn:
            c = self.conn.cursor()
            stmt = """SELECT * FROM expenses WHERE user_id=?"""
            c.execute(stmt, (user_id,)
                      )  # Use `,` if only one tuple kind of field.
            return c.fetchall()
