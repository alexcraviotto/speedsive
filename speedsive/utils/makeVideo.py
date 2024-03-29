from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip

from utils.musicConverter import MusicConverter

from api.youtube import Youtube

from logger import logger  # type: ignore
from utils.makeThumbnail import makeThumbnail


def makeVideo(name: str):
    """Create and save a video file to output_path after
    combining a static image that is located in image_path
    with an audio file in audio_path"""

    converter = MusicConverter()
    # fileAudioSegment = converter.downloadSingleSong(name)
    # slow = converter.speedChange(fileAudioSegment, 1.2)

    # with open(f"./songs/{name}_speedup.mp3", "wb") as out_f:
    #    slow.export(out_f, format="mp3")
    # create the audio clip object
    audio_clip = AudioFileClip(f"./songs/{name}.mp3")

    # create the thumbnail
    makeThumbnail(name, 1920, 1080, ["aesthetic"])
    # create the image clip object
    image_clip = ImageClip(f"{name}.png")

    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.set_duration(audio_clip.duration)
    # set the FPS to 1
    video_clip.fps = 1

    txt_clip = TextClip(
        "levitate with\nspeed up tiktok audios",
        fontsize=125,
        color="white",
        font="Helvetica-bold",
        kerning=0.7,
    )
    txt_clip = txt_clip.set_pos("center")
    authorName = TextClip(
        "luvder", fontsize=40, color="white", font="Helvetica-bold", kerning=0.5
    ).set_position(("center", "bottom"))
    # write the resuling video clip
    video = CompositeVideoClip([video_clip, txt_clip, authorName]).set_duration(
        audio_clip.duration
    )

    video.write_videofile(f"./{name}.mp4", codec="libx264", fps=24, threads=4)

    logger.info(f"[{name}] video is done")

    yt = Youtube()

    yt.uploadVideo(
        f"./{name}.mp4",
        name,
        10,
        "Automatically uploaded by speedsive",
        ["speedsive"],
        "private",
    )
