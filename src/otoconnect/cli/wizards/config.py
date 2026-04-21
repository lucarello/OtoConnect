"""
Manages user configuration updates, allowing customization of decks and
audio and word fields.
"""

from otoconnect.anki.client import send_request
from otoconnect.configuration import ConfigOption, Config
from otoconnect.cli.input_handler import (get_choice, 
                                          clean_file_path, 
                                          validate_path)


def update_handler() -> ConfigOption | None:
    """
    Initiate the procedure to manually update the 
    config.json file based on the options the users
    choose.
    """
    print('--- Configuration Update Wizard ---')
    
    # Checks if the configuration update is finished
    choice = None
    
    while choice is None:
        print('Select one of the following options:\n')
        print('[1] Update Deck')
        print('[2] Update Audio Field')
        print('[3] Update Word Field')
        print('[4] Update Anki Path')
        print('[5] Update Download Folder')
        print('[6] Update All')
        print('[7] Exit\n')
        
        choice = get_choice(1, 7)
    
    choice_map = {
        1: ConfigOption.DECK,
        2: ConfigOption.AUDIO_FIELD,
        3: ConfigOption.WORD_FIELD,
        4: ConfigOption.ANKI_PATH, 
        5: ConfigOption.DOWNLOAD_FOLDER,
        6: ConfigOption.ALL,
        7: None
    }
    
    return choice_map.get(choice)


def update_config(config_instance: Config, config_options: ConfigOption) -> None: 
    """
    Defines user configuration in the config.json
    file. 
    Primarily used to update user configuration.
    
    :param config_instance: The Config class instance
    that carries configuration data.
    :param config_options: The configuration flags 
    the program will use to define user configuration.
    """
    if ConfigOption.DECK in config_options:
        new_deck = select_deck()
        config_instance.deck = new_deck
        
    # Checks if the config_options variable contains either audio or word
    # field flags, preventing the necessity of selecting the model twice.
    if config_options & (ConfigOption.AUDIO_FIELD | ConfigOption.WORD_FIELD):
        model = select_model()
        
        if not model:
            return
        
    if ConfigOption.AUDIO_FIELD in config_options:
        new_audio_field = select_field(model, 'audio')
        config_instance.audio_field = new_audio_field
        
    if ConfigOption.WORD_FIELD in config_options:
        new_word_field = select_field(model, 'word')
        config_instance.word_field = new_word_field
        
    if ConfigOption.ANKI_PATH in config_options:
        new_anki_path = get_path('Anki')
        config_instance.anki_path = new_anki_path
    
    if ConfigOption.DOWNLOAD_FOLDER in config_options:
        new_download_folder = get_path('Download Folder')
        config_instance.download_folder = new_download_folder


def item_selection(item_list: list[str], prompt_word: str) -> str | None:
    """
    Selects a determined item in a list. It's
    primarily used by other functions.
    
    :param item_list: The list of items that
    can be chosen by the user.
    :param prompt_word: The word that appears
        when the program lists available items.
        Represents the items.
    """
    print(f'Available {prompt_word}s:\n')
    for index, item in enumerate(item_list):
        # Index is incremented by one so the selection
        # number becomes more user-friendly.
        print(f'[{index + 1}]     {item}')
    
    # The selected item. Works as a control variable.
    choice = None
    
    while choice is None:        
        choice = get_choice(1, len(item_list))
        
    index = choice - 1
    
    return item_list[index]


def select_deck() -> str | None:
    """
    Gets a list of decks from user's Anki and
    call the item_selection() function, so the
    user can choose a deck to use.
    """
    payload = {
        "action": "deckNames",
        "version": 6
    }
    
    deck_list = send_request(payload)
    
    selected_deck = item_selection(deck_list, 'deck')
    return selected_deck
      
        
def select_model() -> str | None:
    """
    Gets a list of models from user's Anki and
    call the item_selection() function, so the
    user can choose a model to look for the fields.
    """
    payload = {
        'action': 'modelNames',
        'version': 6
    }

    model_list = send_request(payload)
    
    selected_model = item_selection(model_list, 'model')
    
    return selected_model
        
  
def select_field(model: str, select_mode: str) -> str | None:
    """
    Gets a list of fields from user's Anki and
    call the item_selection() function, so the
    user can choose a field to use. It covers
    both word and audio fields.
    
    :param model: The model in which the fields
    are contained.
    :param select_mode: The type of the field (word or
    audio)
    """
    
    payload = {
        "action": "modelFieldNames",
        "version": 6,
        "params": {
            "modelName": model
        }
    }
    
    field_list = send_request(payload)
    
    if select_mode == 'audio':
        selected_field = item_selection(field_list, 'audio field')
        
    if select_mode == 'word':
        selected_field = item_selection(field_list, 'word field')
        
    return selected_field


def get_anki_startup():
    """
    Gets user preference in whether or not to open Anki
    during OtoConnect startup.
    """
    choice = None
    
    while choice is None:
        print('Would you like to open Anki on OtoConnect startup?\n')
        print('[1] Yes')
        print('[2] No\n')
        
        choice = get_choice(1, 2)
        
    choice_map = {
        1: True,
        2: False
    }
    
    return choice_map.get(choice)


def get_path(prompt_word: str) -> str:
    """
    Prompts the user for a determined path.
    
    The user can either type the path directly or drag and drop
    it into the terminal.
    """
    is_path_valid = False
    
    while not is_path_valid:
        raw_path = input(f'Please enter your {prompt_word} path: ')
        clean_path = clean_file_path(raw_path)
        
        is_path_valid = validate_path(clean_path)
    
    return clean_path