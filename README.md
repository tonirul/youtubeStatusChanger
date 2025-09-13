# 📺 YouTube Private Video Updater

A simple **Flask web app** that automatically finds your **private YouTube videos** and updates them to **unlisted**.  
Built using the **YouTube Data API v3** with Google OAuth2 authentication.

---

## 🚀 Features
- Authenticate with Google via OAuth2
- Detects **all private videos** in your channel’s uploads
- Updates privacy status from **Private → Unlisted**
- Web UI with a **Start Update** button and **real-time progress**
- Saves login session locally (`token.pickle`) so you don’t have to re-login each time

---

## 🛠️ Requirements
- Python **3.8+**
- Google Cloud Project with **YouTube Data API v3** enabled
- OAuth2 credentials (`client_secret.json`)

---

## 📂 Project Structure
.
├── app.py # Flask backend
├── templates/
│ └── index.html # Frontend UI
├── client_secret.json # Google API OAuth2 credentials
├── token.pickle # Generated after first login (stores session)
├── requirements.txt # Python dependencies

yaml
Copy code

---

## 📦 Installation

1. **Clone this repo** (or download the files):

```bash
git clone https://github.com/yourusername/youtube-private-updater.git
cd youtube-private-updater
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
🔑 Setup Google API Credentials
Go to Google Cloud Console

Create a project → Enable YouTube Data API v3

Go to APIs & Services → Credentials

Create OAuth client ID → Choose Desktop app

Download the JSON file

Rename it to client_secret.json and place it in the project root

⚠️ Never share client_secret.json or token.pickle publicly!

▶️ Run the App
bash
Copy code
python app.py
The app starts at: http://127.0.0.1:5000

On first run:

A Google login window opens

Sign in with your YouTube account

Allow permissions for YouTube Data API

A token.pickle file is saved so you don’t need to log in again

🌐 Usage
Open http://127.0.0.1:5000

Click Start Update

The app will:

Fetch your uploads playlist

Detect private videos

Convert them to unlisted

Progress appears on screen in real time ✅

⚙️ Configuration
By default, up to 200 videos per run are processed.
You can change this in app.py:

python
Copy code
DAILY_LIMIT = 200
🧹 Resetting Login
If you want to re-authenticate or use another YouTube account:

bash
Copy code
rm token.pickle
Restart the app, and you’ll be prompted to log in again.

⚠️ Notes
Works only on your own YouTube account (OAuth required).

Respect YouTube API quota limits (10,000 units/day by default).

Do not share your API keys or tokens publicly.

📜 License
This project is for personal use only.
Use responsibly and in compliance with YouTube API Terms of Service.
