from dotenv import load_dotenv
from os import getenv
import requests
import isodate
import datetime

load_dotenv()
YOUTUBE_API_TOKEN = getenv("GOOGLE_DATA_API_KEY")

class Video:
    def __init__(self, url: str, title: str, description: str, duration: datetime.timedelta, views_count: int):
        self.url = url
        self.title = title
        self.description = description
        self.duration = duration
        self.views_count = views_count

def get_youtube_videos_ids(query: str) -> list[str]:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "q": query,
        "part": "snippet",
        "type": "video",
        "key": YOUTUBE_API_TOKEN
    }
    
    result = requests.get(url, params)
    video_ids = []
    
    for video in result.json()["items"]:
        video_id = video["id"]["videoId"]
        if video_id:
            video_ids.append(video_id)
    
    return video_ids

def get_video_information(id: str) -> Video:
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "id": id,
        "key": YOUTUBE_API_TOKEN,
        "part": "contentDetails,snippet,statistics"
    }

    result = requests.get(url, params)
    
    
    data = result.json()["items"][0]
    title = data["snippet"]["title"]
    description = data["snippet"]["description"]
    video_url = f"https://www.youtube.com/watch?v={id}"
    duration = isodate.parse_duration(data["contentDetails"]["duration"])
    views_count = data["statistics"]["viewCount"]

    return Video(video_url, title, description, duration, views_count)

def get_videos_info_by_query(query: str) -> list[Video]:
    video_ids = get_youtube_videos_ids(query)

    if not video_ids:
        return []
    
    videos = []
    for video_id in video_ids:
        videos.append(get_video_information(video_id))
    
    return videos

