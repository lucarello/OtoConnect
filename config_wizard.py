"""
Manages user configuration updates, allowing customization of decks and
audio and word fields.
"""

import anki_client
from config_manager import ConfigOption, Config


def update_handler() -> ConfigOption | None:
    """
    Initiate the procedure to manually update the 
    config.json file based on the options the users
    choose.
    """
    print('--- Configuration Update Wizard ---')
    
    # Checks if the configuration update is finished
    options = None
    
    while options is None:
        print('Select one of the following options:\n')
        print('[1] Update Deck')
        print('[2] Update Audio Field')
        print('[3] Update Word Field')
        print('[4] Update All')
        print('[5] Exit\n')
        
        # Stores a Option class value to mitigate possible error 
        # while performing bitwise operations
        
        try:
            choice = int(input('Option: '))
            
            # Since there are 6 possibilities, match is being used over 
            # nested ifs
            match choice:
                case 1: options = ConfigOption.DECK
                case 2: options = ConfigOption.AUDIO_FIELD
                case 3: options = ConfigOption.WORD_FIELD
                case 4: options = ConfigOption.ALL
                case 5: return
                case _: print('You must enter a valid number!\n')
                
        except ValueError:
            print('You must enter a valid number!\n')
        except Exception as e:
            print(f'An unexpected error occurred: {e}\n')
            return
    
    return options


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
    selection = None
    
    while selection is None:
        # Stores the user input before turning it into an integer.
        choice = (input(f'Insert the number of the {prompt_word} you want to use: '))
        
        try:
            # Since index of a list begins at 0, subtracts one from the choice, 
            # that was adjusted to become user-friendly.
            index = int(choice) - 1   
            
            if 0 <= index < len(item_list):
                selection = item_list[index]
            else:
                print('Please, enter a valid number')
            
        except ValueError:
            print('\nYou must enter a valid number!\n')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return
    
    return selection


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
    
    deck_list = None
    
    while deck_list is None:
        deck_list = anki_client.send_request(payload)
    
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

    model_list = None
    
    while model_list is None:
        model_list = anki_client.send_request(payload)
    
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
    
    field_list = None
    
    while field_list is None:
        field_list = anki_client.send_request(payload)
    
    if select_mode == 'audio':
        selected_audio_field = item_selection(field_list, 'audio field')
        return selected_audio_field
    if select_mode == 'word':
        selected_word_field = item_selection(field_list, 'word field')
        return selected_word_field