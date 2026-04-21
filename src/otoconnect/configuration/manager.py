"""
Contains classes related to user configuration, allowing storage and
manipulation of data from the config.json file.
"""

import json
import sys
import os
from typing import Any, Tuple
from pathlib import Path
from enum import Flag, auto
from otoconnect.constants import CONFIG_FILE, HOME_DIR


# Flag class to facilitate the configuration setup
class ConfigOption(Flag):
    NONE = 0
    DECK = auto()
    AUDIO_FIELD = auto()
    WORD_FIELD = auto()
    ANKI_PATH = auto()
    DOWNLOAD_FOLDER = auto()
    ALL = DECK | AUDIO_FIELD | WORD_FIELD | ANKI_PATH | DOWNLOAD_FOLDER
    
    
class Config:
    """Stores and maintains information about user configuration."""
    
    def __init__(self) -> None:
        self._config_file = CONFIG_FILE
        self._data = self._get_config()
        self.is_updated, self.missing_options = self._check_config_state()    
    
    @property
    def first_time(self) -> bool:
        return self._data.get('first_time', True)
    
    @first_time.setter
    def first_time(self, value: bool) -> None:
        self._data['first_time'] = value
        
        self._save_config()
        
    @property
    def startup_anki(self) -> bool | None:
        return self._data.get('startup_anki')
    
    @startup_anki.setter
    def startup_anki(self, value: bool) -> None:
        self._data['startup_anki'] = value
        
        self._save_config()
    
    @property
    def anki_path(self) -> str | None:
        return self._data.get('anki_path')
    
    @anki_path.setter
    def anki_path(self, value: str | None) -> None:
        self._data['anki_path'] = value
        
        self._save_config()
        
    @property
    def download_folder(self) -> str | None:
        return self._data.get('download_folder')
    
    @download_folder.setter
    def download_folder(self, value: str | None) -> None:
        self._data['download_folder'] = value

        self._save_config()
    
    @property
    def deck(self) -> str | None:
        return self._data.get('anki_deck')
    
    @deck.setter
    def deck(self, value: str) -> None:
        self._data['anki_deck'] = value
        
        self._save_config()
    
    @property
    def audio_field(self) -> str | None:
        return self._data.get('audio_field')
    
    @audio_field.setter
    def audio_field(self, value: str) -> None:
        self._data['audio_field'] = value
        
        self._save_config()
    
    @property
    def word_field(self) -> str | None:
        return self._data.get('word_field')
    
    @word_field.setter
    def word_field(self, value: str) -> None:
        self._data['word_field'] = value
        
        self._save_config()
        
    def _get_config(self) -> dict[str, Any]:
        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Sets an empty dictionary to create the config.json file
            return {}
    
    def _save_config(self) -> None:
        with open(self._config_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)
            
    def _check_config_state(self) -> Tuple[bool, ConfigOption | None]:
        options = ConfigOption.NONE
        
        if not self.deck:
            options |= ConfigOption.DECK
            
        if not self.audio_field:
            options |= ConfigOption.AUDIO_FIELD
            
        if not self.word_field:
            options |= ConfigOption.WORD_FIELD
            
        if not self.anki_path or not Path(self.anki_path).exists():
            if not self._try_set_anki():
                options |= ConfigOption.ANKI_PATH
            
        if not self.download_folder or not Path(self.download_folder).exists():
            if not self._try_set_download():
                options |= ConfigOption.DOWNLOAD_FOLDER
        
        if options != ConfigOption.NONE:
            return False, options
        
        return True, None
    
    def _try_set_anki(self) -> bool:
        local_app_data = os.getenv('LOCALAPPDATA')
        
        if local_app_data:
            win32_path = Path(local_app_data) / 'Programs' / 'Anki' / 'anki.exe'
        else:
            win32_path = None
        
        default_anki_options = {
            'win32': win32_path,
            'darwin': Path('/Applications/Anki.app/Contents/MacOS/anki'),
            'linux': Path('/usr/local/bin/anki')
        }
        
        default_anki = default_anki_options.get(sys.platform)
        
        if default_anki and default_anki.exists():
            print(f'Found default anki file at: {default_anki}')
            
            self.anki_path = str(default_anki)
            return True
        
        return False

    def _try_set_download(self) -> bool:
        default_download = HOME_DIR / 'Downloads'

        if default_download.exists():
            print(f'Found default download folder at: {default_download}.')
            
            self.download_folder = str(default_download)
            return True
        
        return False