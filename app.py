from flask import Flask, render_template, jsonify, request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import time
import threading

app = Flask(__name__)
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
DAILY_LIMIT = 200

# Global variable to store progress
progress = {"total": 0, "updated": 0, "status": "", "details": []}


def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)


def get_uploads_playlist_id(youtube):
    request = youtube.channels().list(part="contentDetails", mine=True)
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def list_private_videos(youtube, uploads_playlist_id, limit=DAILY_LIMIT):
    videos = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        video_ids = [item["contentDetails"]["videoId"] for item in response.get("items", [])]
        titles = {item["contentDetails"]["videoId"]: item["snippet"]["title"] for item in response.get("items", [])}

        if video_ids:
            video_request = youtube.videos().list(part="id,status", id=",".join(video_ids))
            video_response = video_request.execute()
            for item in video_response.get("items", []):
                if item["status"].get("privacyStatus") == "private":
                    vid = item["id"]
                    videos.append({"id": vid, "title": titles.get(vid, "Unknown Title")})
                    if len(videos) >= limit:
                        return videos

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return videos


def update_videos_to_unlisted(youtube, videos):
    progress["total"] = len(videos)
    progress["updated"] = 0
    progress["status"] = "Updating videos..."
    progress["details"] = []

    for vid_data in videos:
        vid = vid_data["id"]
        title = vid_data["title"]
        try:
            youtube.videos().update(
                part="status",
                body={"id": vid, "status": {"privacyStatus": "unlisted"}}
            ).execute()
            progress["updated"] += 1
            progress["details"].append({"id": vid, "title": title, "status": "Unlisted"})
            time.sleep(0.1)
        except Exception as e:
            progress["details"].append({"id": vid, "title": title, "status": f"Error: {e}"})

    progress["status"] = "Completed!"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_update():
    def run_task():
        youtube = get_authenticated_service()
        uploads_playlist_id = get_uploads_playlist_id(youtube)
        private_videos = list_private_videos(youtube, uploads_playlist_id, limit=DAILY_LIMIT)
        if private_videos:
            update_videos_to_unlisted(youtube, private_videos)
        else:
            progress["status"] = "No private videos found."
            progress["details"] = []

    thread = threading.Thread(target=run_task)
    thread.start()
    return jsonify({"message": "Process started"})


@app.route("/progress")
def get_progress():
    return jsonify(progress)


if __name__ == "__main__":
    app.run(debug=True)
