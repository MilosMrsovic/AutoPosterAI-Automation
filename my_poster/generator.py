import os
import json
import base64
from datetime import datetime
from pathlib import Path
import subprocess
import random
import re


# BASE PATHS

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT.parent / "output"  # all generated files are stored here
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# CONFIG LOADING

def load_brand_config():
    """
    Loads brand configuration from config/brand.json
    """
    config_path = CONFIG_DIR / "brand.json"
    print(f"🔍 Looking for config at: {config_path}")

    if not config_path.exists():
        print("❌ Config file does not exist")
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            print(f"✅ Config loaded: {config.get('company_name')}")
            return config
    except Exception as e:
        print(f"❌ Error while reading config: {e}")
        return {}


# LOGO HANDLING

def encode_logo_to_base64(logo_path: str):
    """
    Converts a logo image to a base64 string
    Path is relative to the project root
    """
    logo_file = PROJECT_ROOT / logo_path
    print(f"🔍 Looking for logo: {logo_file}")

    if not logo_file.exists():
        print("⚠️ Logo file does not exist")
        return ""

    try:
        image_data = logo_file.read_bytes()

        if image_data[:8] == b"\x89PNG\r\n\x1a\n":
            file_type = "png"
        elif image_data[:3] == b"\xff\xd8\xff":
            file_type = "jpeg"
        elif logo_file.suffix.lower() == ".gif":
            file_type = "gif"
        else:
            file_type = "png"

        b64 = base64.b64encode(image_data).decode("utf-8")
        print(f"✅ Logo encoded ({file_type.upper()})")
        return f"data:image/{file_type};base64,{b64}"

    except Exception as e:
        print(f"❌ Error while encoding logo: {e}")
        return ""


# TEMPLATE SELECTION

def choose_random_template():
    """
    Randomly selects an HTML template from the templates directory
    """
    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Templates directory does not exist: {TEMPLATES_DIR}")

    html_files = list(TEMPLATES_DIR.glob("*.html"))
    if not html_files:
        raise FileNotFoundError("No HTML templates found")

    chosen = random.choice(html_files)
    print(f"🎲 Selected template: {chosen.name}")
    return chosen


# HTML GENERATION

def create_poster_html(ai_text: str):
    """
    Generates final HTML for the poster by injecting brand config and AI text
    """
    brand = load_brand_config()
    if not brand:
        raise ValueError("Brand configuration could not be loaded")

    date_str = datetime.now().strftime("%d.%m.%Y")
    logo_base64 = encode_logo_to_base64(
        brand.get("logo_path", "static/logo.png")
    )

    escaped_ai_text = (
        ai_text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )

    template_path = choose_random_template()
    html_content = template_path.read_text(encoding="utf-8")

    # Remove existing CONFIG block if present
    html_content = re.sub(
        r"const CONFIG = \{.*?\};",
        "",
        html_content,
        flags=re.DOTALL
    )

    js_config = f"""
const CONFIG = {{
    primary_color: "{brand.get('primary_color', '#0976EA')}",
    secondary_color: "{brand.get('secondary_color', '#00F08E')}",
    logo_base64: "{logo_base64}",
    company_name: "{brand.get('company_name', 'HEAQ Automation')}",
    slogan: "{brand.get('slogan', 'Daily Signal')}",
    contact: "{brand.get('contact', 'heaqdigital.com')}",
    ai_text: "{escaped_ai_text}",
    date: "{date_str}"
}};
"""

    html_content = html_content.replace(
        "<script>",
        f"<script>\n{js_config}"
    )

    return html_content


# SCREENSHOT GENERATION

def generate_poster_screenshot(ai_text: str, output_file: str = None):
    """
    Generates a poster image using Puppeteer and Chromium
    """
    print("🎨 Generating poster...")

    if output_file is None:
        output_file = OUTPUT_DIR / "daily-poster.png"
    else:
        output_file = Path(output_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    temp_html = BASE_DIR / f"temp_{int(datetime.now().timestamp())}.html"
    node_file = BASE_DIR / "puppeteer_temp.js"

    try:
        html = create_poster_html(ai_text)
        temp_html.write_text(html, encoding="utf-8")

        html_path = temp_html.as_posix()
        out_path = output_file.as_posix()

        node_script = f"""
const puppeteer = require('puppeteer');

(async () => {{
    const browser = await puppeteer.launch({{
        executablePath: '/usr/bin/chromium',
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ]
    }});

    const page = await browser.newPage();
    await page.setViewport({{
        width: 1080,
        height: 1350,
        deviceScaleFactor: 2
    }});

    await page.goto('file:///{html_path}', {{
        waitUntil: 'networkidle0'
    }});

    await new Promise(r => setTimeout(r, 2000));

    await page.screenshot({{
        path: '{out_path}'
    }});

    await browser.close();
    process.exit(0);
}})();
"""
        node_file.write_text(node_script, encoding="utf-8")

        result = subprocess.run(
            ["node", str(node_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0 and output_file.exists():
            print(f"✅ Poster generated: {output_file}")
            return str(output_file)

        print("❌ Puppeteer execution failed")
        print(result.stderr)
        return None

    finally:
        if temp_html.exists():
            temp_html.unlink()
        if node_file.exists():
            node_file.unlink()


# PUBLIC API FUNCTION

def generate_poster(ai_text: str, output_file: str = None):
    """
    Public entry point used by the API
    """
    return generate_poster_screenshot(ai_text, output_file)


# LOCAL TEST

if __name__ == "__main__":
    test_text = (
        "Automation is not just speed.\n"
        "It is control and scalability.\n\n"
        "#automation #ai #growth"
    )

    generate_poster(test_text)
