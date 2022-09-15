from time import sleep
from utils.generateTitle import generateTitle
from utils.generatePlaylistID import generatePlaylistID
from utils.musicConverter import MusicConverter
from api.spotify import Spotify
from api.youtube import Youtube
from utils.makeVideo import makeVideo
from logger import logger
from db.database import Database
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.removeFile import removeFile
from os.path import join

logger.info("__Starting megagigachad Bot__")
db = Database()
md = MusicConverter()
sp = Spotify()

limit = 10


def main():
    logger.info("Process started")
    title = generateTitle()
    songs = sp.getPlaylistTracklist(generatePlaylistID(), limit)
    md.downloadSongs(title, songs, "SU")
    makeVideo(title)
    removeFile(f"./songs/{title}.mp3")
    removeFile(f"{title}.mp4")
    removeFile(f"{title}.png")
    logger.info("Waiting for the next process")
    sleep(43200)


while True:
    main()
