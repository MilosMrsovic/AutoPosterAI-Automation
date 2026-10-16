# AI-Powered Facebook Poster Automation System

Built by [Heaq Digital](https://heaqdigital.com), an automation studio for US service businesses. Full write-up: All projects https://heaqdigital.com/projects

This project is a fully automated system for publishing Facebook posts on a daily schedule.  
Content is planned in advance in **Google Sheets**, while the system handles everything else — from content generation to visual creation and publishing.

The goal is simple:  
**plan once, post automatically, stay consistent.**

---

## What This System Does

Manual daily posting is repetitive and hard to maintain long-term.  
This automation removes that burden by turning Google Sheets into a lightweight content planner and letting the system execute everything else.

With this setup:
- content is planned by date
- posts are generated automatically using AI
- visuals are created from predefined templates
- publishing happens without human interaction
- posting history is tracked automatically

---

## How It Works (Simple Flow)

1. A **daily scheduled trigger** runs at a fixed time.
2. The system checks Google Sheets for content scheduled for today.
3. If content exists:
   - AI generates post text (title, body, hashtags)
   - a poster is created using a random template
   - the post is published on Facebook
4. If no content exists:
   - an email notification is sent
5. After publishing, the sheet is updated with `posted`.

---

## Google Sheets as Content Planner

Each row represents one planned post:

- **Date** – exact publishing date  
- **Content Idea** – short guidance for the AI  
- **Notes (optional)** – tone or context  
- **Posted** – filled automatically after publishing  

If the date doesn’t match, nothing gets posted. No surprises.

---

## AI & Poster Generation

- AI generates structured Facebook copy:
  - title
  - main text
  - hashtags
- The system selects **1 of 4 visual templates randomly**.
- Text is injected into the template and saved as a final poster image.
- Posters are organized by date for easy tracking.

---

## Facebook Publishing

- The system sends a POST request via **Facebook Graph API**.
- Image and caption are published automatically.
- Everything runs silently in the background.

---

## Reliability & Notifications

- Missing scheduled content → email notification
- Failed steps can be logged and extended with retries
- Posting status is always visible in Google Sheets

---

## Tech Stack

- Google Sheets API  
- Automation orchestration (e.g. n8n)  
- AI text generation (LLM-based)  
- Image templating system  
- Facebook Graph API  
- Email notifications

---

## Why This Matters

This project reflects real, practical automation work:
- scheduling and condition-based logic
- API integration across multiple systems
- AI used for real business output
- end-to-end automation without manual steps

It’s designed as a **production-ready content automation system**, not a demo.
