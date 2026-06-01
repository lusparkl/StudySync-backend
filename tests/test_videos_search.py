from app.ai.search_youtube import get_youtube_videos_ids, get_video_information, get_videos_info_by_query, Video

def test_getting_videos_ids_positive():
    ids = get_youtube_videos_ids("Python tutorial")

    assert len(ids) == 5

def test_getting_videos_ids_negative():
    ids = get_youtube_videos_ids("ahfsdklfjsalk;hfoisadhgoihwASOIGFJIANVAIJFVOPAJFKLSADFKLJfdask;ljfasjk;lfdsjkal;fsdajklfsdk;jlafd;klsjaf;jklsdageargeg")

    assert ids == []

def test_getting_video_information():
    video = get_video_information("qh0FkdgieS8")
    
    assert isinstance(video, Video)
    assert video.title == "The Most Talented Man in AI"
    assert video.url == "https://www.youtube.com/watch?v=qh0FkdgieS8"
    assert isinstance(video.views_count, int)

def test_getting_videos_information_positive():
    videos = get_videos_info_by_query("programming")

    assert len(videos) == 5
    for video in videos:
        assert isinstance(video, Video)

def test_getting_videos_information_negative():
    videos = get_videos_info_by_query("")

    assert videos == []