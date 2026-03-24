# PixelShift — JPG ↔ PNG Converter

A lightweight Flask web app to convert images between JPG and PNG formats. No files are stored on the server — everything is processed in memory and returned instantly.

## Features
- JPG → PNG conversion (with transparency support)
- PNG → JPG conversion (transparency flattened to white background)
- Drag & drop or click-to-upload
- Image preview before conversion
- Max 16MB file size
- Mobile-friendly UI

---

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000

---

## Deploy to the Internet (Free Options)

### Option 1: Render.com (Recommended — Free tier available)
1. Push this project to a GitHub repository
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
   - **Environment:** Python 3
5. Click Deploy — you'll get a public URL like `https://your-app.onrender.com`

### Option 2: Railway.app
1. Push to GitHub
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Select your repo — Railway auto-detects the Procfile
4. Add a domain under Settings → Networking

### Option 3: Heroku
```bash
heroku create your-app-name
git push heroku main
```
Make sure you have the Heroku CLI installed.

### Option 4: Fly.io (Free tier)
```bash
fly launch
fly deploy
```

---

## Project Structure
```
image-converter/
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Frontend UI
├── requirements.txt    # Python dependencies
├── Procfile            # For Heroku/Render/Railway
└── README.md
```

## Notes
- Files are **never saved to disk** — conversion happens in RAM
- HTTPS is handled automatically by Render/Railway/Heroku
- No database or cloud storage needed
