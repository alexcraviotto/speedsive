import sys, os

sys.path.append(os.path.abspath(".."))
from db.database import Database


def generateTitle():
    database = Database()
    generatedTitle = "sped up tiktok songs that make you levitate | pt. " + str(
        database.lastNumberOfTitle() + 1
    )
    print(generatedTitle)
    database.uploadTitle(generatedTitle)
    return generatedTitle
