from database_manager import DatabaseHandler
import anki_utils
import config_utils
import webbrowser


def mode_selector():
    '''
    Generates a prompt that allows the user to 
    select if they want to use the program for 
    its purpose or configure it.
    '''
    # Control variable that checks if the user selected a mode.
    mode_selected = False
    while mode_selected == False:
        try:
            print('Please, choose a mode between the following\n')
            print('[1] Use Mode')
            print('[2] Configuration Mode\n')
            
            choice = int(input('Option: '))
            
            # Match was chosen over nested ifs to make the code cleaner.
            match choice:
                case 1: return 'use'
                case 2: return 'update'
                case _: print('You must enter a valid number!')
                    
        except ValueError:
            # There is no return here, so the loop continues even if data like
            # strings are entered by the user.
            print('You must enter a valid number!')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return

def main():
    print('--- Welcome to OtoConnect! ---\n')
    
    db = DatabaseHandler()
    
    db.table_setup()
    
    # Checks the using mode but also works as a control variable.
    mode = None
    
    # Only stops to ask when the user decides to update their notes audio.
    while mode != 'use':    
        mode = mode_selector()
        
        if mode == 'update':
            config_utils.update_handler()
    
    # These variables are set here in case the content in config.json
    # is updated, preventing the use of stale configuration.
    config = config_utils.get_config()            
    word_field = config.get('word_field')
    
    note_list = anki_utils.get_notes()
    
    # Stops execution if AnkiConnect is unavailable or an error occurs.
    if note_list is None:
        return
    
    # Stops execution if there are no cards to process
    if not note_list:
        print('No note without audio was found')
        return
    
    note_info = anki_utils.get_note_info(note_list)
    
    for note in note_info:
        word = note['fields'][word_field]['value']
        note_id = note['noteId']
        
        db.set_tuple(note_id, word)
        
    
    for note in note_info:
        print('\n---------------------------')
        word = note['fields'][word_field]['value']
        print(f'Current Word: {word}')
        print(f'')
        
        # Hardcoded to use Forvo and the Japanese search (#ja). The user may 
        # change the suffix or the entire URL if they find it necessary.
        webbrowser.open_new_tab(f'https://forvo.com/word/{word}/#ja')
        
        storage_result = None
        
        # The loop continues until the file is successfully stored
        while storage_result is None:
            raw_path = input("Enter the audio file path or drag the file into the terminal: ")
            file_path = anki_utils.file_path_cleaner(raw_path)
            
            if not file_path:
                print('The file path cannot be empty\n')
            else:
                print('Storing audio file...')
                # If the store_audio_file function returns None, the loop continues.
                # If it returns something different, it stops.
                storage_result = anki_utils.store_audio_file(file_path, word)
        
        print('Updating audio field on Anki...')
        anki_utils.update_audio(note['noteId'], word)
        
        audio_file_name = f'{word}.mp3'
        
        db.audio_update(audio_file_name, note['noteId'])
            
        print('Update complete!\n')
    
    print('All done! Every card without audio was updated!')
    
    db.end_connection()
    
    input("\nPress enter to end the program.")


if __name__ == "__main__":
    main()