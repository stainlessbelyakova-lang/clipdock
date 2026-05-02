import json
import uuid
from datetime import datetime
from .config import DATA_DIR, CLIPS_FILE, MAX_CLIPS


def ensure_storage():
    DATA_DIR.mkdir(exist_ok=True)

    if not CLIPS_FILE.exists():
        CLIPS_FILE.write_text("[]", encoding="utf-8")


def load_clips():
    ensure_storage()

    try:
        with open(CLIPS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_clips(clips):
    ensure_storage()

    with open(CLIPS_FILE, "w", encoding="utf-8") as file:
        json.dump(clips[:MAX_CLIPS], file, indent=4, ensure_ascii=False)


def create_clip(text: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "id": str(uuid.uuid4()),
        "text": text,
        "created_at": now,
        "pinned": False
    }