import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Obtener token
def get_access_token():
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    print("Token status:", response.status_code)
    print("Token response:", response.text)

    try:
        return response.json().get("access_token")
    except Exception as e:
        raise Exception(f"Error decodificando token: {e} - Respuesta: {response.text}")

# Llamar a API pública de usuario
def get_user_info(username, access_token):
    url = "https://open.tiktokapis.com/v2/research/user/info/"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"username": username}
    response = requests.get(url, headers=headers, params=params)

    print("User info status:", response.status_code)
    print("User info response:", response.text)

    try:
        return response.json()
    except Exception as e:
        raise Exception(f"Error al decodificar JSON: {e} - Respuesta: {response.text}")


def get_user_videos(open_id, access_token, max_count=10):
    url = "https://open.tiktokapis.com/v2/research/video/list/"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "open_id": open_id,
        "max_count": max_count  # puedes ajustar este número según lo que necesites
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_video_comments(video_id, access_token, max_count=10):
    url = "https://open.tiktokapis.com/v2/research/comment/list/"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "video_id": video_id,
        "max_count": max_count
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
