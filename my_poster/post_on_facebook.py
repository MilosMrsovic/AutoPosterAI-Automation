import requests
import random
from datetime import datetime
from pathlib import Path

# =========================
# CONFIGURATION
# =========================

# Page User Access Token (hidden for security)
USER_TOKEN = "******************************************************************"

# Project directories and poster path
BASE_DIR = Path("/data/moj_poster")
OUTPUT_DIR = BASE_DIR / "output"
POSTER_PATH = OUTPUT_DIR / "daily-poster.png"

# Caption templates for Facebook posts
CAPTION_TEMPLATES = [
    """🚀 AI-Generated Art from HEAQ Digital Automation

This unique piece was created using our automated AI system that blends technology and creativity.

✨ AI-generated
🤖 Fully automated
📅 {date}

#AI #Automation #DigitalArt #HEAQ #Innovation #TechArt #FutureOfWork""",

    """🎨 Daily AI Poster – HEAQ Digital Automation

A fresh AI-generated visual, created automatically without human intervention.

⚙️ Automation powered
🧠 AI-driven
📅 {date}

#AIgenerated #Automation #HEAQDigital #Tech #Future #DigitalInnovation""",

    """🤖 Where AI meets Automation

Today's poster was generated and published automatically by HEAQ systems.

🧠 AI intelligence
⚡ Automated pipeline
📅 {date}

#Automation #AI #HEAQ #DigitalTransformation #SmartSystems""",

    """✨ The Future of Creative Automation

An automatically generated poster from HEAQ Digital Automation.

🔮 AI creation
⚙️ End-to-end automation
📅 {date}

#AIcreation #Automation #HEAQ #DigitalFuture #TechArt"""
]

# =========================
# HELPER FUNCTIONS
# =========================

def get_page_access_token():
    """
    Retrieve the Facebook Page access token using the user token.
    Returns the first page token found.
    """
    response = requests.get(
        "https://graph.facebook.com/v18.0/me/accounts",
        params={"access_token": USER_TOKEN},
        timeout=10
    )

    if response.status_code != 200:
        raise Exception("Failed to retrieve Facebook Page access token")

    return response.json()["data"][0]["access_token"]


def get_random_caption():
    """
    Returns a randomly selected caption from CAPTION_TEMPLATES.
    The current date is inserted into the caption.
    """
    template = random.choice(CAPTION_TEMPLATES)
    return template.format(date=datetime.now().strftime("%d.%m.%Y"))


def post_poster():
    """
    Uploads the daily poster to Facebook with a random caption.
    Raises an exception if the poster is missing or upload fails.
    """
    if not POSTER_PATH.exists():
        raise FileNotFoundError(f"Poster not found: {POSTER_PATH}")

    caption = get_random_caption()
    page_token = get_page_access_token()

    print("📤 Uploading poster...")
    print("📝 Random caption selected")

    with open(POSTER_PATH, "rb") as img:
        response = requests.post(
            "https://graph.facebook.com/v18.0/me/photos",
            files={"source": img},
            data={
                "message": caption,
                "access_token": page_token
            },
            timeout=30
        )

    if response.status_code != 200:
        print(response.text)
        raise Exception("Facebook upload FAILED")

    post_id = response.json().get("id")
    print("✅ POST SUCCESSFUL")
    print(f"🔗 https://facebook.com/{post_id}")

# =========================
# MAIN EXECUTION
# =========================

if __name__ == "__main__":
    print("🚀 HEAQ AUTO FACEBOOK POSTER SYSTEM")
    print("=" * 50)

    post_poster()

    print("=" * 50)
    print("🎉 DONE — POSTER HAS BEEN PUBLISHED")
