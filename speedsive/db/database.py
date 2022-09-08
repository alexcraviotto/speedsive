import sqlite3
import os, sys
import sys, os
from os.path import dirname, realpath

sys.path.append(os.path.abspath(".."))
from speedsive.logger import logger


class Database:
    def __init__(self):
        BASE_DIR = dirname(realpath(__file__))
        self.conn = sqlite3.connect(BASE_DIR + "/speedsive.db")
        try:
            self.conn.execute(
                """create table videos (
                                    id integer primary key autoincrement,
                                    title text
                                )"""
            )
            logger.info("The database has been created and connected")
        except sqlite3.OperationalError:
            pass

    def uploadTitle(self, title: str):
        self.conn.execute(f"INSERT INTO videos (title) VALUES (?)", (title,))
        print("done")
        self.conn.commit()
        self.conn.close()

    def lastNumberOfTitle(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM videos")
            return (cursor.execute("SELECT * FROM videos ORDER BY id").fetchall()[-1])[
                0
            ]
        except IndexError:
            return 0
        except Exception as e:
            logger.error(
                "An error occurred when getting the last number of the title: " + {e}
            )
