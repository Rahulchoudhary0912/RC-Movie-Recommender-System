# 🎬 Movie Recommender System

A smart, responsive movie recommendation app powered by machine learning and the TMDB API. Get suggestions based on movie titles or genres — complete with posters, trailers, and a modern UI.

## 🚀 Features

- 🔍 Search by Movie or Genre
- 📽️ Movie Posters & Trailers from TMDB
- 🧠 ML-Based Recommendations (Cosine Similarity)
- 🌞 Time-Based Greetings
- 🌓 Dark/Light Mode toggle
- 📱 Mobile-Friendly UI

---

## 📂 Project Structure

```
movie-recommend-System/
├── model/
│   ├── similarity.pkl
│   ├── movie_list.pkl
│   ├── movies.csv
│   └── credits.csv
├── server.py
├── requirements.txt
├── render.yaml
└── static/
    └── index.html
```

---

## ⚙️ Backend Deployment (Render)

1. Ensure your `model/` folder (with all 4 files) is present in the project root.
2. Add your TMDB API key to `render.yaml` or the Render dashboard.
3. Deploy to [Render.com](https://render.com) as a new Web Service (upload the zipped folder or connect your repo).

---

## ⚡ Frontend Deployment (Vercel/Netlify)

1. Upload the contents of the `static/` folder to [Vercel](https://vercel.com) or [Netlify](https://netlify.com).
2. Update API URLs in your JS to point to your deployed backend (e.g., `https://movie-recommender-backend.onrender.com/api/...`).

---

## 🔑 TMDB API Key
- Required for fetching posters/trailers.
- Store securely in backend environment variables and/or frontend as needed.

---

## 🛠️ Usage
- Start the backend: `python server.py`
- Open the frontend: `static/index.html` (or deploy as above)

---

## 👨‍💻 Developers
- Ujjal
- Rahul 

This message means your Flask backend is running, but you visited a URL (like `/` or `/static/index.html`) that Flask does not have a route for.

**By default, your current `server.py` only serves API endpoints** (like `/api/movies`, `/api/genres`, etc.), not the frontend HTML.

---

## How to Fix: Serve the Frontend from Flask

Add these routes to your `server.py` (at the bottom, before `if __name__ == "__main__":`):

```python
from flask import send_from_directory

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
```

**What this does:**
- Visiting `http://127.0.0.1:5000/` will show your `static/index.html` (your frontend).
- All static assets (CSS, JS, images) will be served from the `static/` folder.
- Your API endpoints (`/api/...`) will continue to work.

---

## Steps

1. **Edit `server.py`** and add the above code.
2. **Restart your Flask server** (`python server.py`).
3. **Visit** `http://127.0.0.1:5000/` in your browser.

---

**Now you will see your web app and all API calls will work locally!**

Let me know if you want me to make this edit for you. 