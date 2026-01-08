import requests
import json
from enum import Flag, auto

ANKI_CONNECT_URL = 'http://127.0.0.1:8765'
CONFIG_FILE = 'config.json'

# Flag class to facilitate the configuration setup
class Option(Flag):
    NONE = 0
    DECK = auto()
    AUDIO_FIELD = auto()
    WORD_FIELD = auto()
    ALL = DECK | AUDIO_FIELD | WORD_FIELD
    
def get_config():
    '''
    Gets the current configuration in the config.json
    file.
    If it can't find the configuration file or its fields
    are empty, it will generate an empty dictionary and 
    call a function to properly create the config.json
    '''
    # Open the file and loads its content
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    
    except FileNotFoundError:
        print(f"Error: The configuration file was not found!")
        print(f'Creating a new configuration file')
        
        # Sets an empty dictionary to create the config.json file
        config_data = {}
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return
    
    # This block determines which options should the update_config() 
    # function update
    options = Option.NONE
    if not config_data.get('anki_deck'):
        options |= Option.DECK
    
    if not config_data.get('audio_field'):
        options |= Option.AUDIO_FIELD
        
    if not config_data.get('word_field'):
        options |= Option.WORD_FIELD
        
    if options != Option.NONE:
        # the "_" ignores the boolean return value that checks
        # if the update is finished
        config_data, _ = update_config(config_data, options)
        
    return config_data


def update_handler():
    '''
    Initiate the procedure to manually update the 
    config.json file based on the options the users
    choose.
    '''
    print('--- Configuration Update Wizard ---')
    
    config_data = get_config()
    
    # Checks if the configuration update is finished
    is_finished = False
    
    while is_finished == False:
        print('Select one of the following options:\n')
        print('[1] Update Deck')
        print('[2] Update Audio Field')
        print('[3] Update Word Field')
        print('[4] Update All')
        print('[5] Exit\n')
        
        # Stores a Option class value to mitigate possible error 
        # while performing bitwise operations
        options = Option.NONE
        
        try:
            choice = int(input('Option: '))
            
            # Since there are 6 possibilities, match is being used over 
            # nested ifs
            match choice:
                case 1: options = Option.DECK
                case 2: options = Option.AUDIO_FIELD
                case 3: options = Option.WORD_FIELD
                case 4: options = Option.ALL
                case 5: options = Option.NONE
                case _: print('You must enter a valid number!')
                
        except ValueError:
            print('You must enter a valid number!')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return
        
        config_data, is_finished = update_config(config_data, options)
    
    return
            

def update_config(config_data, config_options = Option.NONE): 
    '''
    Defines user configuration in the config.json
    file. 
    Primarily used to update user configuration.
    
    :param config_data: The content of the
    config.json file.
    :param config_options: The configuration flags 
    the program will use to define user configuration.
    '''
    
    # Returning True here means that the update is finished
    if config_options == Option.NONE: 
        return config_data, True
    
    if Option.DECK in config_options:
        deck = select_deck()
        config_data['anki_deck'] = deck
        
    # Checks if the config_options variable contains either audio or word
    # field flags, preventing the necessity of selecting the model twice.
    if config_options & (Option.AUDIO_FIELD | Option.WORD_FIELD):
        model = select_model()
        
    if Option.AUDIO_FIELD in config_options:
        audio_field = select_field(model, 'audio')
        config_data['audio_field'] = audio_field
        
    if Option.WORD_FIELD in config_options:
        word_field = select_field(model, 'word')
        config_data['word_field'] = word_field
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
            # Returns False so the user continues in the Update screen
            # after finishing an update 
            return config_data, False
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        # In case an error occurs, the user can still try to
        # update their configuration.
        return config_data, False


def item_selection(item_list, prompt_word):
    '''
    Selects a determined item in a list. It's
    primarily used by other functions.
    
    :param item_list: The list of items that
    can be chosen by the user.
    :param prompt_word: The word that appears
        when the program lists available items.
        Represents the items.
    '''
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


def select_deck():
    '''
    Gets a list of decks from user's Anki and
    call the item_selection() function, so the
    user can choose a deck to use.
    '''
    payload = {
        "action": "deckNames",
        "version": 6
    }
    
    try:
        deck_list = requests.post(ANKI_CONNECT_URL, json=payload).json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return
    
    selected_deck = item_selection(deck_list, 'deck')
    return selected_deck
      
        
def select_model():
    '''
    Gets a list of models from user's Anki and
    call the item_selection() function, so the
    user can choose a model to look for the fields.
    '''
    payload = {
        'action': 'modelNames',
        'version': 6
    }
    
    try:
        model_list = requests.post(ANKI_CONNECT_URL, json=payload).json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return
    
    selected_model = item_selection(model_list, 'model')
    return selected_model
        
        
def select_field(model, type):
    '''
    Gets a list of fields from user's Anki and
    call the item_selection() function, so the
    user can choose a field to use. It covers
    both word and audio fields.
    
    :param model: The model in which the fields
    are contained.
    :param type: The type of the field (word or
    audio)
    '''
    payload = {
        "action": "modelFieldNames",
        "version": 6,
        "params": {
            "modelName": model
        }
    }
    
    try:
        field_list = requests.post(ANKI_CONNECT_URL, json=payload).json()['result']
    except requests.exceptions.ConnectionError:
        print(f'Connection Error: Check if Anki is open at {ANKI_CONNECT_URL}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return
    
    if type == 'audio':
        selected_audio_field = item_selection(field_list, 'audio field')
        return selected_audio_field
    if type == 'word':
        selected_word_field = item_selection(field_list, 'word field')
        return selected_word_field