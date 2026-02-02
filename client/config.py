import sys, os
from pathlib import Path

if getattr(sys, 'frozen', False):
    root = Path(sys.executable).resolve().parent
else:
    root = Path(__file__).resolve().parent

WINDOW_PROFILE_NAME = os.getlogin()
ffmpeg_directory = root / "ffmpeg" / "bin"