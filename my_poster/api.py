# api.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import os

from generator import generate_poster
from post_on_facebook import post_poster


# PATH CONFIGURATION

PROJECT_ROOT = Path("/data/moj_poster")
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DAILY_POSTER = OUTPUT_DIR / "daily-poster.png"


# FASTAPI APP SETUP

app = FastAPI(
    title="AI Poster Generator API",
    version="1.0.0"
)


# REQUEST MODELS

class PosterRequest(BaseModel):
    ai_text: str
    overwrite: bool = True


# API ENDPOINTS

@app.post("/generate-poster")
async def generate_poster_endpoint(request: PosterRequest):
    """
    Generates a poster image and saves it to:
    /data/moj_poster/output/daily-poster.png
    """
    try:
        print("🖼️ Generating poster...")

        result_path = generate_poster(
            request.ai_text,
            str(DAILY_POSTER)
        )

        if not result_path or not os.path.exists(result_path):
            raise HTTPException(status_code=500, detail="Poster generation failed")

        size_kb = os.path.getsize(result_path) / 1024

        return {
            "status": "success",
            "poster_path": str(DAILY_POSTER),
            "file_size_kb": round(size_kb, 2),
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/post-to-facebook")
async def post_to_facebook_endpoint():
    """
    Posts the daily poster to Facebook using a randomly selected caption
    """
    if not DAILY_POSTER.exists():
        raise HTTPException(
            status_code=404,
            detail="Poster does not exist. Call /generate-poster first."
        )

    try:
        post_poster()

        return {
            "status": "posted",
            "poster": str(DAILY_POSTER),
            "message": "Poster published with a random caption",
            "time": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Facebook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download")
async def download_daily_poster():
    """
    Downloads the generated daily poster
    """
    if not DAILY_POSTER.exists():
        raise HTTPException(status_code=404, detail="Poster does not exist")

    return FileResponse(
        DAILY_POSTER,
        media_type="image/png",
        filename="daily-poster.png"
    )


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "poster_exists": DAILY_POSTER.exists(),
        "poster_path": str(DAILY_POSTER),
        "time": datetime.now().isoformat()
    }


# APPLICATION ENTRY POINT

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
