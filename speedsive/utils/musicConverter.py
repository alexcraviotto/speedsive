from moviepy.editor import VideoFileClip  # type: ignore
from pydub import AudioSegment  # type: ignore
from os.path import dirname, join, realpath

# from sys import path, stdin
import urllib.request
import re
from pytube import YouTube  # type: ignore
import os
import shutil
from Path import reducePath

from logger import logger


class MusicConverter:
    """Initialise the Class MusicConversor for
    downloading and exporting songs from Youtube."""

    def __init__(self):
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
        os.remove(mp4)
        BASE_DIR = dirname(realpath(__file__))
        DIR = reducePath(BASE_DIR, 2)

        # Move the audio file to its output directory
        if os.path.exists(join(DIR, "songs")):
            shutil.move("".join([x for x in solution if x != "/"]), join(DIR, "songs"))
        else:
            os.mkdir(join(DIR, "songs"))
            shutil.move("".join([x for x in solution if x != "/"]), join(DIR, "songs"))

    def downloadSongs(self) -> None:
        """
        Download the songs whatever you want from Youtube.
        """
        n_songs = int(input("Nº songs: "))
        # The loop save each token of the song from the Youtube's HTML
        for number in range(n_songs):
            song = input("Name of the song: ")
            url_song = song
            for w in self.ENCODED_WORDS:
                # Encode each word found
                if song.find(w) > 0:
                    url_song = url_song.replace(w, f"%{int(ord(w) - 12)}")

            url_song = url_song.replace(" ", "+")

            html = urllib.request.urlopen(
                f"https://www.youtube.com/results?search_query={url_song}"
            )
            html_decoded = html.read().decode()
            pattern = re.findall(r"watch\?v=(\S{11})", html_decoded)[0]
            link = "https://www.youtube.com/watch?v=" + pattern
            self.songs[song] = link

        # Export each song in its format given
        for song, link in self.songs.items():
            self.export_audiofile(link, song)

    def downloadSingleSong(self, name: str) -> AudioSegment:
        """
        Download the song you want from Youtube.
        """
        url_song = name + " audio"
        for w in self.ENCODED_WORDS:
            # Encode each word found
            if name.find(w) > 0:
                url_song = url_song.replace(w, f"%{int(ord(w) - 12)}")
        url_song = url_song.replace(" ", "+")
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={url_song}"
        )
        html_decoded = html.read().decode()
        pattern = re.findall(r"watch\?v=(\S{11})", html_decoded)[0]
        link = "https://www.youtube.com/watch?v=" + pattern
        self.songs[name] = link
        # Export the song in its format given
        self.export_audiofile(link, name)
        return AudioSegment.from_file(os.getcwd() + "/songs/" + name + ".mp3")

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
