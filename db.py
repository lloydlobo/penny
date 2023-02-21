import sqlite3


class DBHelper:
    def __init__(self, dbname="db_penny.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)  # self.conn = None

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

    def delete_expense(self, uuid, user_id):
        with self.conn:
            print(uuid, user_id)
        pass

    def get_expenses(self, user_id):
        with self.conn:
            c = self.conn.cursor()
            stmt = """SELECT * FROM expenses WHERE user_id=?"""
            c.execute(stmt, (user_id,)
                      )  # Use `,` if only one tuple kind of field.
            return c.fetchall()

    def search_expense(self, user_id, keyword):
        result = ""
        with self.conn:
            # We will get all the expenses.
            expenses = self.get_expenses(user_id=user_id)
            matches = [e for e in expenses if keyword.lower() in str(e).lower]
            if len(matches) == 0:
                result = f"No expenses matching '{keyword}' found"
            else:
                # We need to search each row for a term.
                #    We can use the databases search feature, but we will use not use it for now.
                result = f""
        result = result.strip().upper
        return result

        # print(user_id, search_term)
        # pass

    # def search(term: str):
    #     db_expenses = []
    #     matches = [e for e in db_expenses if term.lower() in str(e).lower()]
    #     if len(matches) == 0:
    #         print(f"No expenses matching '{term}' found")
    #     else:
    #         # total_matches = sum(float(e["amount"]) for e in matches)
    #         total_matches = sum(float(e[2]) for e in matches)
    #         print(matches, total_matches)
    #         pass
    #     pass
