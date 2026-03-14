"""
Contains various functions that collect and manage data from Anki.
"""

import os
from typing import Any

import anki_client
from config_manager import Config


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
    
    result = None
    
    while result is None:
        result = anki_client.send_request(payload)
        
    return result


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
    
    result = None
    
    while result is None:
        result = anki_client.send_request(payload)
    
    return result


def file_path_cleaner(raw_file_path: str) -> str:
    """
    Cleans a file path name, eliminating empty
    spaces and quotes ('' or "") which can be
    automatically added by the terminal.
    
    :param raw_file_path: File path with possible
    quotes or empty spaces surrounding it.
    """
    clean_file_path = raw_file_path.strip()
     
    # "startswith" and "endswith" were preferred, since folders and 
    # files names may contain quotes.
    if clean_file_path.startswith('"') and clean_file_path.endswith('"'):
        clean_file_path = clean_file_path[1:-1]
    elif clean_file_path.startswith("'") and clean_file_path.endswith("'"):
        clean_file_path = clean_file_path[1:-1]
    
    return clean_file_path


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
        return
    
    payload = {
        'action': 'storeMediaFile',
        'version': 6,
        'params': {
            'filename': f'{word}.mp3',
            'path': file_path
        }
    }
    
    result = None
    
    while result is None:
        result = anki_client.send_request(payload)    

    return result
    
    
def update_audio(config_instance: Config, 
                 note_id: int, 
                 word: str) -> Any | None:
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
    
    result = None
    
    while result is None:
        result = anki_client.send_request(payload)
    
    return result