import sqlite3


class DatabaseLayer(object):
    """Trol"""
    def __init__(self):
        self.sql_statment = ""
        self.dbfile = "database.db"
        self.conn = sqlite3.connect(self.dbfile, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS viewcount
                        (site TEXT primary key,
                        counted INTEGER default 0)
                        """)
        self.conn.commit()

    def inc(self, what):
        self.c.execute("""INSERT OR IGNORE INTO viewcount (site, counted) VALUES(?, 0)""", [what,])
        self.conn.commit()
        self.c.execute("""UPDATE viewcount SET counted = counted + 1 WHERE site=?""", [what,])
        self.conn.commit()

    def fetch(self):
        self.c.execute("SELECT * FROM viewcount")
        result = self.c.fetchall()
        return result

databaselayer = DatabaseLayer()
