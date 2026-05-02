import pyperclip


def get_clipboard():
    try:
        return pyperclip.paste().strip()
    except Exception:
        return ""


def set_clipboard(text: str):
    try:
        pyperclip.copy(text)
    except Exception:
        pass