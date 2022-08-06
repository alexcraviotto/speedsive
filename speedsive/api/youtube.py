from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from httplib2 import Credentials
from google.oauth2.credentials import Credentials
import requests
import json
from google.auth.exceptions import RefreshError

from logger import logger


class Youtube:
    def __init__(self):
        self.API_NAME = "youtube"
        self.API_VERSION = "v3"

    def generateCredentials(self) -> Credentials:
        """Generate the necessary credentials to create the Google service.

        Returns:
            Credentials: Credentials using OAuth 2.0 access and refresh tokens.
        """
        try:
            with open("../.secret/youtube/client_creds.json", "r") as read_file:
                resp = json.load(read_file)
            logger.info("Generating credentials...")
            return Credentials(
                resp["access_token"],
                refresh_token=resp["refresh_token"],
                scopes=resp["scope"],
                client_id=resp["client_id"],
                client_secret=resp["client_secret"],
            )
        except Exception as e:
            logger.error(f"Failed to generate credentials correctly: {e}")

    def generateService(self, mustRefresh: bool) -> build:
        """Generates the service necessary to carry out the Google API calls.

        Args:
            mustRefresh (bool): Optional argument indicating whether the token is to be refreshed or not.

        Returns:
            build: Construct a Resource for interacting with an API.
        """
        creds = self.generateCredentials()
        if mustRefresh == True:
            logger.info("Credentials have expired, initiated refresh process")
            self.refreshToken(creds)
            creds = self.generateCredentials()
            logger.info("Generating service....")
        return build(self.API_NAME, self.API_VERSION, credentials=creds)

    def refreshToken(self, creds: Credentials) -> None:
        """Refresh the token once expired.

        Args:
            creds (Credentials): Expired creds as an argument to update them.

        Returns:
            None
        """
        params = {
            "grant_type": "refresh_token",
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "refresh_token": creds.refresh_token,
        }

        authorization_url = "https://oauth2.googleapis.com/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
            try:
                with open("../.secret/youtube/client_creds.json", "r+") as read_file:
                    resp = json.load(read_file)
                    resp["access_token"] = r.json()["access_token"]
                    read_file.seek(0)
                    json.dump(resp, read_file, indent=4)
                    read_file.truncate()
                    read_file.close()
                logger.info("Updated credentials")
            except Exception as e:
                logger.error(
                    f"The refresh_token request was successful but an error occurred while processing the response: {e}"
                )

        else:
            logger.error("The token could not be refreshed")
            return None

    def uploadVideo(
        self,
        videoPath: str,
        title: str,
        category: int,
        description: str,
        tags: list[str],
        privacy: str,
        mustRefresh=False,
    ) -> None:
        """Upload the video to youtube

        Args:
            videoPath (str): Video route.
            title (str): Title of the video.
            category (int): Video category(https://gist.github.com/dgp/1b24bf2961521bd75d6c).
            description (str): Description of the video.
            tags (list[str]): Tags for the video.
            privacy (str): Privacy for the video.
            mustRefresh (bool, optional): Optional argument indicating whether the token is to be refreshed or not. Defaults to False.
        """
        try:
            service = self.generateService(mustRefresh)
            mediaFile = MediaFileUpload(videoPath, chunksize=-1, resumable=True)
            body = {
                "snippet": {
                    "categoryId": category,
                    "title": title,
                    "description": description,
                    "tags": tags,
                },
                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False,
                },
                "notifySubscribers": False,
            }
            logger.info(f"The video: [{title}] has started to be uploaded to YouTube")
            responseUpload = (
                service.videos()
                .insert(part="snippet,status", body=body, media_body=mediaFile)
                .execute()
            )

            # service.thumbnails().set(
            #     videoId=responseUpload.get("id"),
            #     media_body=MediaFileUpload(title + ".png"),
            # ).execute()
            # logger.info(f"The video: [{title}] has been uploaded correctly")

        except RefreshError as e:
            mustRefresh = True
            self.uploadVideo(
                videoPath, title, category, description, tags, privacy, mustRefresh=True
            )
        except Exception as e:
            logger.error(
                f"An error occurred when starting the upload process to Yotutube: {e}"
            )
