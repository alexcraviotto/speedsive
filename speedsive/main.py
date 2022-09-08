from utils.musicConverter import MusicConverter
from api.spotify import Spotify
from api.youtube import Youtube
from utils.makeVideo import makeVideo
from logger import logger
from db.database import Database
from apscheduler.schedulers.blocking import BlockingScheduler
from os.path import join

logger.info("__Starting megagigachad Bot__")
db = Database()
md = MusicConverter()
sp = Spotify()
with open(join(md.SPEEDSIVE_FOLDER_PATH, "playlists.txt")) as f:
    playlists = f.readlines()
limit = 10
index = 0


def main():
    global index
    songs = sp.getPlaylistTracklist(playlists[0], limit)
    md.downloadSongs(f"Ejemplo{index+1}", songs, "SL")
    makeVideo(f"Ejemplo{index+1}")
    playlists.pop(0)
    index += 1


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", hours=1)
scheduler.start()
