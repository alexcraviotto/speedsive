import requests
import base64
import json
from logger import logger


class Spotify:
    def __init__(self):

        with open("../speedsive/.secret/spotify/client_creds.json", "r") as read_file:
            resp = json.load(read_file)

        self.CLIENT_ID = resp["client_id"]
        self.CLIENT_SECRET = resp["client_secret"]
        self.BASE_API_AUTH_URL = "https://accounts.spotify.com/api/"
        self.BASE_API_URL = "https://api.spotify.com/v1/"
        self.ENCODED_SECRETS = base64.b64encode(
            f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode("ascii")
        ).decode("ascii")

    def getToken(self):

        headers = {"Authorization": "Basic " + self.ENCODED_SECRETS}

        params = {
            "grant_type": "client_credentials",
        }

        try:
            r = requests.post(
                self.BASE_API_AUTH_URL + "token", data=params, headers=headers
            )

            if r.ok:
                token = r.json()["access_token"]
                logger.info("Spotify token generated")
                return token
            else:
                logger.error(f"Failed to make the request for get the token: {r.text}")

        except Exception as e:
            logger.error(f"Failed to generate credentials correctly: {e}")

    def getPlaylistTracklist(self, playlistID: str, limit: int):
        tracklist = {}

        headers = {"Authorization": "Bearer " + self.getToken()}

        try:
            r = requests.get(
                url=self.BASE_API_URL
                + f"playlists/{playlistID}/tracks?limit={str(limit)}",
                headers=headers,
            )
            jsonResponse = r.json()
            i = 0

            for tracks in jsonResponse["items"]:
                tracklist[jsonResponse["items"][i]["track"]["name"]] = jsonResponse[
                    "items"
                ][i]["track"]["artists"][0]["name"]
                i += 1

            logger.info("The tracklist of the playlist has been obtained correctly")
            return tracklist
        except Exception as e:
            logger.error(f"Failed to get the playlist tracklist correctly: {e}")
