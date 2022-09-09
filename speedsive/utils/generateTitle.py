import sys, os

sys.path.append(os.path.abspath(".."))
from db.database import Database


def generateTitle():
    database = Database()
    generatedTitle = "speed up tiktok audios that make you levitate | pt. " + str(
        database.lastNumberOfTitle() + 1
    )
    print(generatedTitle)
    database.uploadTitle(generatedTitle)
    return generatedTitle
