# ClipDock

ClipDock is a simple offline macOS clipboard history manager built with Python and CustomTkinter.

## Features

- Clipboard history tracking
- Automatic clipboard monitoring
- Search through copied text
- Pin important clips
- Copy text back instantly
- Clear clipboard history
- Local JSON storage
- Offline-first
- Dark mode UI

## Tech Stack

- Python 3.11
- CustomTkinter
- pyperclip

## Project Structure

```bash
clipdock/
├── main.py
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── storage.py
│   ├── clipboard.py
│   └── ui.py
├── data/
│   └── clips.json
└── assets/
    └── icon.png