from logger import logger
def generatePlaylistID():
    try:
        with open('././speedsive/playlists.txt','r+') as fp:
            lines = fp.readlines()
            fp.seek(0)
            fp.truncate()
            result = lines[0]
            try:
                lines[0] = ""
                fp.writelines(lines[1:])
            except:
                logger.warn('You need to add more playlists ID on the file')
            return result.strip()
    except:
        logger.error('Error on playlistID generation')
