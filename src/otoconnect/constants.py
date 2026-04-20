from pathlib import Path

HOME_DIR = Path.home()

DATA_DIR = HOME_DIR / '.otoconnect'

CONFIG_FILE = DATA_DIR / 'config.json'
DB_FILE = DATA_DIR / 'oto_connect_data.db'

DOWNLOAD_FOLDER = HOME_DIR / 'Downloads'

AUDIO_EXTENSIONS = ('.mp3', '.wav', '.ogg')

ANKI_CONNECT_URL = 'http://127.0.0.1:8765'