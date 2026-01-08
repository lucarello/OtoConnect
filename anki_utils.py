import requests
import os
import config_utils

# AnkiConnect's HTTP server default IP Address
ANKI_CONNECT_URL = 'http://127.0.0.1:8765'


def get_notes():
    '''
    Gets the Anki note IDs of notes that contain no
    audio, based on the user deck and audio field
    set in the config.json file.
    '''
    # These variables are set here in case the content in config.json
    # is updated, preventing the use of stale configuration.
    config = config_utils.get_config()
    deck = config.get('anki_deck')
    audio_field = config.get('audio_field')
    
    # The query uses Anki's search syntax
    # Quotes are used on the deck's name because of ::
    payload = {
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'deck:{deck} {audio_field}:'
        }
    }
    
    try:
        # The 'json=' argument automatically encodes the payload to JSON
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        # The generated response is a dictionary which contains a "result" key.
        return response.json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return


def get_note_info(note_list):
    '''
    Gets notes information based on their IDs, such
    as content on each field.
    
    :param note_list: A list of Anki notes IDs
    '''
    payload = {
        'action': 'notesInfo',
        'version': 6,
        'params': {
            'notes': note_list
        }
    }
    
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        return response.json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return


def file_path_cleaner(raw_file_path):
    '''
    Cleans a file path name, eliminating empty
    spaces and quotes ('' or "") which can be
    automatically added by the terminal.
    
    :param raw_file_path: File path with possible
    quotes or empty spaces surrounding it.
    '''
    clean_file_path = raw_file_path.strip()
     
    # "startswith" and "endswith" were preferred, since folders and 
    # files names may contain quotes.
    if clean_file_path.startswith('"') and clean_file_path.endswith('"'):
        clean_file_path = clean_file_path[1:-1]
    elif clean_file_path.startswith("'") and clean_file_path.endswith("'"):
        clean_file_path = clean_file_path[1:-1]
    
    return clean_file_path


def store_audio_file(file_path, word):
    '''
    Copies an audio file to Anki's media folder and
    renames it based on the word it is assigned.
    
    :param file_path: The (clean) path of an audio
    file
    :param word: The word which the audio is assigned
    '''
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
    
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        return response.json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return
    
    
def update_audio(note_id, word): 
    '''
    Updates the audio field in the Anki note.
    
    :param note_id: The ID of the Anki note being 
    updated.
    :param word: The word to which the audio is 
    assigned.
    '''
    # These variables are set here in case the content in config.json
    # is updated, preventing the use of stale configuration.
    config = config_utils.get_config()
    audio_field = config.get('audio_field')
    
    payload = {
        'action': 'updateNoteFields',
        'version': 6,
        'params': {
            'note': {
                'id': note_id,
                'fields': {
                    # Brackets are used since it's Anki's mandatory format.
                    audio_field: f'[sound:{word}.mp3]'
                }
                    
            }
        }
    }
    
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        return response.json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return