import sqlite3
import shutil
import os

class Parser:

    def __init__(self):

        self.chrome_history = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History")
        self.temp_history = "History_copy"
        shutil.copy(self.chrome_history, self.temp_history)
        self.conn = sqlite3.connect(self.temp_history)
        self.cursor = conn.cursor()

    def parse(self):

        data = self.cursor.execute("""
        SELECT url, title, last_visit_time
        FROM urls
        ORDER BY last_visit_time DESC
        LIMIT 1000
        """)

        return data


