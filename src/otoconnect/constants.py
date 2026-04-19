from pathlib import Path

MAIN_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = MAIN_DIR / 'data'

CONFIG_FILE = DATA_PATH / 'config.json'
DB_FILE = DATA_PATH / 'oto_connect_data.db'

DOWNLOAD_FOLDER = Path.home() / 'Downloads'

AUDIO_EXTENSIONS = ('.mp3', '.wav', '.ogg')

ANKI_CONNECT_URL = 'http://127.0.0.1:8765'