from fastapi import FastAPI, HTTPException
from tiktok_api import get_access_token, get_user_info, get_user_videos, get_video_comments

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TikTok Researcher API - Consulta extendida"}

@app.get("/user-full/{username}")
def full_user_data(username: str):
    token = get_access_token()
    if not token:
        raise HTTPException(status_code=500, detail="Token no disponible")

    user_data = get_user_info(username, token)
    if "data" not in user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    open_id = user_data["data"]["open_id"]
    follower_count = user_data["data"].get("follower_count")
    user_meta = {
        "username": username,
        "open_id": open_id,
        "follower_count": follower_count
    }

    video_data = get_user_videos(open_id, token)
    videos_info = []

    for video in video_data.get("data", {}).get("videos", []):
        video_id = video["video_id"]
        description = video.get("description", "")
        create_time = video.get("create_time")  # Epoch timestamp

        hashtags = [word for word in description.split() if word.startswith("#")]

        comments_data = get_video_comments(video_id, token)
        comments_info = []
        for comment in comments_data.get("data", {}).get("comments", []):
            comments_info.append({
                "text": comment.get("text"),
                "create_time": comment.get("create_time")
            })

        videos_info.append({
            "video_id": video_id,
            "description": description,
            "create_time": create_time,
            "hashtags": hashtags,
            "comments": comments_info
        })

    return {
        "user": user_meta,
        "videos": videos_info
    }

