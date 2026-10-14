"""Portable Velxio launcher: serves backend + built frontend on localhost and opens the browser."""
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

PORT = int(os.environ.get("VELXIO_PORT", "3080"))

APP_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent / "dist-portable"
DATA_DIR = APP_DIR / "data"
TOOLS_DIR = APP_DIR / "tools"
FRONTEND_DIR = APP_DIR / "frontend"

for sub in ("arduino15", "Arduino", "work"):
    (DATA_DIR / sub).mkdir(parents=True, exist_ok=True)

os.environ["PATH"] = str(TOOLS_DIR) + os.pathsep + os.environ.get("PATH", "")
os.environ["ARDUINO_DIRECTORIES_DATA"] = str(DATA_DIR / "arduino15")
os.environ["ARDUINO_DIRECTORIES_USER"] = str(DATA_DIR / "Arduino")
os.environ.setdefault("FRONTEND_URL", f"http://127.0.0.1:{PORT}")
os.environ.setdefault("VELXIO_NEWS", "off")
os.chdir(DATA_DIR / "work")

import uvicorn  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from app.main import app  # noqa: E402

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="spa")


def _open_browser():
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:{PORT}")


if __name__ == "__main__":
    threading.Thread(target=_open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")
