from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CLIPS_FILE = DATA_DIR / "clips.json"

APP_NAME = "ClipDock"
WINDOW_SIZE = "1000x650"
MAX_CLIPS = 100
POLL_INTERVAL = 800