"""
Sends HTTP requests to AnkiConnect API, allowing the collection
of data, used by diverse modules within the application.
"""

from typing import Any

from requests.exceptions import ConnectionError
from requests import post

ANKI_CONNECT_URL = 'http://127.0.0.1:8765'


def send_request(payload: dict[str, Any]) -> Any | None:
    result = None
    is_successful = False
    
    while not is_successful:
        try:
            # The 'json=' argument automatically encodes the payload to JSON
            response = post(ANKI_CONNECT_URL, json=payload)
            # The generated response is a dictionary which contains a "result" key.
            result = response.json()['result']
            
            is_successful = True
            
        except ConnectionError:
            print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
            input('\nPress Enter to try again...')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            input('\nPress Enter to try again...')

    return result