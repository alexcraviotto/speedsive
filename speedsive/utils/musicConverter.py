from moviepy.editor import VideoFileClip  # type: ignore
from pydub import AudioSegment  # type: ignore
from os.path import dirname, join, realpath

# from sys import path, stdin
import urllib.request
import re
from pytube import YouTube  # type: ignore
import os
from utils.removeFile import removeFile
import shutil
from utils.Path import reducePath

from logger import logger


class MusicConverter:
    """Initialise the Class MusicConversor for
    downloading and exporting songs from Youtube."""

    def __init__(self):
        self.BASE_DIR = dirname(realpath(__file__))
        self.SPEEDSIVE_FOLDER_PATH = reducePath(self.BASE_DIR, 1)
        self.songs = {}
        self.ENCODED_WORDS = [
            "&",
            "!",
            "#",
            "$",
            "%",
            "'",
            "(",
            ")",
            "*",
            "+",
            ",",
            ".",
            "/",
            ":",
            ";",
            "<",
            "=",
            ">",
            "?",
            "@",
            "^",
            "_",
            "{",
            "}",
            "¬",
            "€",
            "~",
            "¿",
            "¡",
        ]
        self.output = "mp3"

    def export_audiofile(self, url: str, name: str) -> None:
        """
        Export the audiofile in a output directory\n

        Args:
            url (str): Url of the videoclip in Youtube
            name (str): Name of the song
        """

        logger.info(f"Exporting [{name} to mp3]")
        # Download the mp4 video from Youtube
        mp4 = YouTube(url).streams.get_highest_resolution().download()

        # Pick up the name of the videoclip
        # name = mp4.replace("\\", ";").split(";")[-1][:-4]

        solution = f"{name}.{self.output}"

        # Pick up the audio from the mp4 video
        # and write it in the output format you chose
        video_clip = VideoFileClip(mp4)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(solution)

        audio_clip.close()
        video_clip.close()

        # Delete the mp4 video in between for saving the audio file
        removeFile(mp4)

        # Move the audio file to its output directory
        if os.path.exists(join(self.SPEEDSIVE_FOLDER_PATH, "songs")):
            shutil.move(
                "".join([x for x in solution if x != "/"]),
                join(self.SPEEDSIVE_FOLDER_PATH, "songs"),
            )
        else:
            os.mkdir(join(self.SPEEDSIVE_FOLDER_PATH, "songs"))
            shutil.move(
                "".join([x for x in solution if x != "/"]),
                join(self.SPEEDSIVE_FOLDER_PATH, "songs"),
            )

    def downloadSongs(self, title: str, songs: dict, speedTag: str = "NULL") -> None:
        """
        Download the songs whatever you want from Youtube.\n
        speedTag can be "SU"(Speed Up) or "SL"(Slow Down) or "NULL"(Remains the same)
        """
        n_songs = len(songs.keys())
        speedRate = 1.0
        if speedTag != "NULL":
            speedRate = 1.25 if speedTag == "SU" else 0.77

        combined = AudioSegment.empty()
        # The loop save each token of the song from the Youtube's HTML
        for number in range(n_songs):
            individualSong = songs.popitem()
            song = str(individualSong[0]) + " " + str(individualSong[1])
            combined += self.speedChange(self.downloadSingleSong(song), speedRate)
            removeFile(join(os.getcwd(),"songs") + f"/{song}.mp3")

        file_handle = combined.export(os.getcwd() + "/songs/" + title + ".mp3")
        logger.info("Audio files combined")

    def downloadSingleSong(self, name: str) -> AudioSegment:
        """
        Download the song you want from Youtube.
        """
        url_song = name + " audio"
        for w in self.ENCODED_WORDS:
            # Encode each word found
            if name.find(w) > 0:
                url_song = url_song.replace(w, f"%{int(ord(w) - 12)}")
        print(url_song)
        url_song = url_song.replace(" ", "+")
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={url_song}"
        )
        html_decoded = html.read().decode()
        pattern = re.findall(r"watch\?v=(\S{11})", html_decoded)[0]
        link = "https://www.youtube.com/watch?v=" + pattern
        self.songs[name] = link
        # Export the song in its format given
        if not os.path.exists(
            join(join(self.SPEEDSIVE_FOLDER_PATH, "songs"), f"{name}.mp3")
        ):
            self.export_audiofile(link, name)
        return AudioSegment.from_file(
            os.getcwd() + "/songs/" + name + ".mp3"
        )

    # ***SLOW DOWN AND SPEED UP FUNCTION***

    def speedChange(self, sound: AudioSegment, speed: float) -> AudioSegment:
        """
        Change the framerate of an AudioSegment.\n
        Ex. if speed = 0.75 it converts the sound
        in slowed down song and viceversa.\n
        Args:
            sound (AudioSegment): Sound chose.
            speed (float, optional): Defaults to 1.0.

        Returns:
            AudioSegment: Sound's frame rate changed.
        """
        # Manually override the frame_rate. This tells the computer how many
        # samples to play per second
        sound_with_altered_frame_rate = sound._spawn(
            sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)}
        )
        logger.info(f"Sound rate altered correctly")
        # convert the sound with altered frame rate to a standard frame rate
        # so that regular playback programs will work right. They often only
        # know how to play audio at standard frame rate (like 44.1k)
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
