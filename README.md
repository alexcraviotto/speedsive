
# Speedsive

Automate the process and upload videos that compile music with altered speed

In this last year thanks to the rise of tiktok has created a very profitable youtube trend that allows you to gain views and subscribers relatively quickly
This trend consists of uploading videos that compile viral songs that are on tiktok and increase or decrease the speed (sped up or slowed songs)
Speedsive is in charge of automating all this, both video creation and uploading to Youtube


## Features

- Generate videos automatically, with customized images according to parameters and text inside the video
- Implements Spotify API to get the name of the viral tracks 
- Implements Youtube API to automatically upload videos with customizable titles, descriptions, etc
- Implement a database to obtain the number that corresponds to the part of your videos of altered songs
- Customized thumbnails according to parameters
- Logging system to know what is happening at any given moment
## Demo

[You can see here an example of a video created and uploaded automatically with speedsive](https://youtu.be/6E5nKs0DSEo)


## Important

Due to Youtube's policy, videos that are automatically uploaded cannot be set as public because Youtube blocks videos added to their platform through an API that they have not verified
More information about this on the [official website]( https://support.google.com/youtube/answer/7300965)
## Installation

We have used as module manager the [Conda manager](https://docs.conda.io/en/latest/), but there are some modules that were not in this platform and have been installed with Pip

### Windows

```bash
  conda env create -f windows-environment.yml 
  conda activate speedsive-env
  conda install
```

### MacOS and Linux

```bash
  conda env create -f macos-environment.yml 
  conda activate speedsive-env
  conda install
```


## Get your secrets

Speedsive uses Spotify API and Youtube API to work, so you need to get their tokens to make it work

```bash
  mkdir ./secret/spotify
  mkdir ./secret/youtube
```

### Spotify

In spotify it is very simple, just access the [dashboard](
https://developer.spotify.com/dashboard/) provided by Spotify and create an application within it, there we will get our `client_id` and our `client_secret` needed to use the API

Finally we will add them inside the `.secret/spotify` folder in a json called `client_creds.json`
```bash
  {
    client_id: "",
    client_secret: ""
  }
```
Also in the `playlists.txt` file you must add the spotify playlists link, from there the songs will be taken

### Youtube
The process to obtain the Youtube token is different because you have many different ways to obtain it, we can not comment on all of them because there are in google the guides to obtain the tokens
The API version is YoutubeV3, there are many resources on the web to get it

Finally we will add them inside the `.secret/youtube` folder in a json called `client_creds.json`
```bash
{
    "access_token": "",
    "refresh_token": "",
    "scope": "https://www.googleapis.com/auth/youtube.upload",
    "client_id": "",
    "client_secret": ""
}
```
## How to make it work?

Once you have installed all the modules necessary for the operation and configured the API secrets, place yourself inside the folder that includes the `main.py` file and you are ready

```bash
python3 main.py
```
## Authors

- [@Alex Craviotto](https://www.github.com/alexcraviotto)
- [@Miguel Ángel Simón](https://www.github.com/miguel07alm)
