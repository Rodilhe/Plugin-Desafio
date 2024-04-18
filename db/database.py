import sqlite3

class Database:
    def __init__(self, db_name='desafio.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS resultados (
                            id INTEGER PRIMARY KEY,
                            well_id INTEGER,
                            diff REAL
                          )''')
        self.conn.commit()
        cursor.close()

    def save_result(self, well_id, diff):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO resultados (well_id, diff) VALUES (?, ?)', (well_id, diff))
        self.conn.commit()
        cursor.close()
