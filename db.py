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
            INSERT INTO expenses (uuid, user_id, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """
            c.execute(
                stmt,
                (uuid, user_id, amount, category, description),
            )
        pass

    def delete_expense(self, user_id, uuid):
        with self.conn:
            # print(user_id, uuid)
            # expenses = self.search_expense(user_id=user_id, uuid=uuid)
            # if expenses is not None:
            #     print(f"{expenses}")
            # else:
            #     return False
            c = self.conn.cursor()
            c.execute("DELETE FROM expenses WHERE uuid=?", (uuid, ))
            return True

    def get_expenses(self, user_id):
        with self.conn:
            c = self.conn.cursor()
            stmt = """SELECT * FROM expenses WHERE user_id=?"""
            c.execute(stmt,
                      (user_id, ))  # Use `,` if only one tuple kind of field.
            return c.fetchall()

    # We need to search each row for a term.
    # !!!! We can use the databases search feature, but we will use not use it for now.
    def search_expense(self, user_id, keyword=None, uuid=None):
        with self.conn:
            expenses = self.get_expenses(user_id=user_id)
            if uuid is not None:
                matches = [row for row in expenses if uuid == row[0]]
                return matches
                # if matches[0]["user_id"] == user_id:
                #     return matches[0]
            else:
                if keyword is not None:
                    matches = [
                        row for row in expenses
                        if keyword.lower() in str(row).lower()
                    ]
                    if len(matches) == 0:
                        return None
                    else:
                        return matches
                else:
                    return expenses


# pretty, total = [], 0
# for e in expenses:
#     date, category, amount, description = e[5], e[3], e[2], e[4]
#     pretty.append(" ".join([date, category, str(amount), description]))
#     total += float(amount)
# counter = len(pretty)
# pretty_expenses = "\n".join(pretty)
# await ctx.send( f"Total expenses({str(counter)}): {str(total)}{CURRENCY}")
# await ctx.send(f"""```@expenses\n{pretty_expenses}```""")
# print(matches_pretty)
# result = str(matches_pretty)
# return result

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
