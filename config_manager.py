"""
Contains classes related to user configuration, allowing storage and
manipulation of data from the config.json file.
"""

import json
from typing import Any
from enum import Flag, auto


# Flag class to facilitate the configuration setup
class ConfigOption(Flag):
    NONE = 0
    DECK = auto()
    AUDIO_FIELD = auto()
    WORD_FIELD = auto()
    ALL = DECK | AUDIO_FIELD | WORD_FIELD
    
    
class Config:
    """Stores and maintains information about user configuration."""
    
    def __init__(self, config_file: str = 'config.json') -> None:
        self._config_file = config_file
        self._data = self._get_config()
        self.is_updated, self.missing_options = self._check_config_state()
    
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
            
    def _check_config_state(self) -> tuple[bool, ConfigOption | None]:
        options = ConfigOption.NONE
        
        if not self.deck:
            options |= ConfigOption.DECK
            
        if not self.audio_field:
            options |= ConfigOption.AUDIO_FIELD
            
        if not self.word_field:
            options |= ConfigOption.WORD_FIELD
        
        if options != ConfigOption.NONE:
            return False, options
        
        return True, None