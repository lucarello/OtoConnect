"""
Contains various functions that collect and manage data from Anki.
"""

import os
from typing import Any

from otoconnect.anki.client import send_request
from otoconnect.configuration import Config


def get_notes(config_instance: Config) -> list[int]:
    """
    Gets the Anki note IDs of notes that contain no
    audio, based on the user deck and audio field
    set in the config.json file.
    """
    # These variables are set here in case the content in config.json
    # is updated, preventing the use of stale configuration.
    
    # The query uses Anki's search syntax
    # Quotes are used on the deck's name because of ::
    payload = {
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'deck:"{config_instance.deck}" {config_instance.audio_field}:'
        }
    }
    
    return send_request(payload)


def get_note_info(note_list: list[int]) -> list[dict[str, Any]]:
    """
    Gets notes information based on their IDs, such
    as content on each field.
    
    :param note_list: A list of Anki notes IDs
    """
    payload = {
        'action': 'notesInfo',
        'version': 6,
        'params': {
            'notes': note_list
        }
    }
    
    return send_request(payload)


def store_audio_file(file_path: str, word: str) -> Any | None:
    """
    Copies an audio file to Anki's media folder and
    renames it based on the word it is assigned.
    
    :param file_path: The (clean) path of an audio
    file
    :param word: The word which the audio is assigned
    """
    if not os.path.exists(file_path):
        print(f'Error: No such file as "{file_path}" was found.\n')
        return None
    
    payload = {
        'action': 'storeMediaFile',
        'version': 6,
        'params': {
            'filename': f'{word}.mp3',
            'path': file_path
        }
    }
    
    return send_request(payload)    
    
    
def update_audio(config_instance: Config, 
                 note_id: int, 
                 word: str) -> None:
    """
    Updates the audio field in the Anki note.
    
    :param note_id: The ID of the Anki note being 
    updated.
    :param word: The word to which the audio is 
    assigned.
    """
    # These variables are set here in case the content in config.json
    # is updated, preventing the use of stale configuration.
    
    payload = {
        'action': 'updateNoteFields',
        'version': 6,
        'params': {
            'note': {
                'id': note_id,
                'fields': {
                    # Brackets are used since it's Anki's mandatory format.
                    config_instance.audio_field: f'[sound:{word}.mp3]'
                }
                    
            }
        }
    }
    
    send_request(payload)