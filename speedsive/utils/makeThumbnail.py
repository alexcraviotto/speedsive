import requests
import shutil


def makeThumbnail(name: str, width: int, height: int, topics: list[str]):
    """
    Create the thumbnail for the video just putting the topics you wish.\n

    Args:
        width (int): Image's width
        height (int): Image's height
        topics (list[str]): Whatever you want to see in the thumbnail
    Return:
        None
    """
    string = ",".join(topics)
    r = requests.get(
        f"https://source.unsplash.com/random/{width}x{height}/?{string}", stream=True
    )
    if r.status_code == 200:
        with open(f"{name}.png", "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
