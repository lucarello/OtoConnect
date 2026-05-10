"""Main module that executes the main use loop."""

import os
import subprocess
import webbrowser
from enum import Enum, auto
from pathlib import Path

from watchdog.observers import Observer

from otoconnect.monitor.file_monitor import AudioFileHandler
from otoconnect.anki import utils
from otoconnect.database import DatabaseHandler
from otoconnect.configuration import Config
from otoconnect.cli.input_handler import get_choice, clean_file_path
from otoconnect.cli.wizards.config import (update_handler, 
                                           update_config,
                                           get_anki_startup)
from otoconnect.cli.menus.database import (query_handler, 
                                           show_query_results)
from otoconnect.constants import DATA_DIR, AUDIO_EXTENSIONS


class Mode(Enum):
    USE = auto()
    CONFIGURATION = auto()
    DATABASE = auto()
    

def run_anki(config_instance: Config) -> None:
    """
    Launches the Anki application asynchronously.
    """
    anki_dir = os.path.dirname(config_instance.anki_path)
    
    subprocess.Popen(['start', config_instance.anki_path],
                     cwd=anki_dir,
                     shell=True)


def populate_database(database_instance: DatabaseHandler, 
                      config_instance: Config) -> None:
    note_list = utils.get_notes(config_instance)
    
    if not note_list:
        return None
    
    note_info = utils.get_note_info(note_list)
    
    database_instance.update_table(note_info)

def mode_selector() -> Mode:
    """
    Generates a prompt that allows the user to 
    select if they want to use the program for 
    its purpose or configure it.
    """
    # Control variable that checks if the user selected a mode.
    choice = None
    
    while choice is None:
        print('Please, choose a mode between the following\n')
        print('[1] Use Mode')
        print('[2] Configuration Mode')
        print('[3] Data Mode\n')
        
        choice = get_choice(1, 3)
    
    choice_map = {
        1: Mode.USE,
        2: Mode.CONFIGURATION,
        3: Mode.DATABASE
    }
    
    return choice_map.get(choice)

def main() -> None:
    print('--- Welcome to OtoConnect! ---\n')
    
    # Creates the main data folder if it doesn't exist.
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    config = Config()
    
    if config.first_time:    
        config.startup_anki = get_anki_startup()
        
        config.first_time = False 
    
    if not config.is_updated:
        print('There is missing configuration in the config.json file!')
        print('Beginning the configuration update...\n')
        update_config(config, config.missing_options)
    
    if config.startup_anki:
        run_anki(config)
    
    db = DatabaseHandler(config)
    
    db.table_setup()
    
    populate_database(db, config)
    
    # Checks the using mode but also works as a control variable.
    mode = None
    
    # Only stops to ask when the user decides to update their notes audio.
    while mode != Mode.USE:    
        mode = mode_selector()
        
        if mode == Mode.CONFIGURATION:
            config_options = update_handler()
            
            if config_options:
                update_config(config, config_options)
            
                populate_database(db, config)
                
        elif mode == Mode.DATABASE:
            query_data = query_handler()
            
            if query_data is not None:
                option, filters = query_data
                
                show_query_results(db, option, filters)
    
    word_list = db.get_loop_list()
    
    word_count = len(word_list)
    
    if word_count == 0:
        print('No note without audio was found!')
        input("\nPress Enter to end the program.")
        
        db.end_connection()
        return None
    
    observer = Observer()
    handler = AudioFileHandler(AUDIO_EXTENSIONS)
    
    observer.schedule(handler, config.download_folder, recursive=False)
    observer.start()
    try:
        for i, note in enumerate(word_list, 1):
            print('\n---------------------------')
            note_id, word = note
            print(f'Current Word: {word} ({i}/{word_count})\n') #x = current word. y = word_count
            
            # Hardcoded to use Forvo and the Japanese search (#ja). The user may 
            # change the suffix or the entire URL if they find it necessary.
            webbrowser.open_new_tab(f'https://forvo.com/word/{word}/#ja')
            
            print('\nDownload the file or press Ctrl+C to skip to the next word.')
            
            try:
                while not handler.caught_file and observer.is_alive():
                    observer.join(1)
            except KeyboardInterrupt:
                print('\nSkipping to the next word...\n')
                
                # The caught file is cleared for security.
                handler.caught_file = None
                
                continue
            
            raw_path = handler.caught_file
            print(f'Found audio file: {raw_path}')
            
            file_path = clean_file_path(raw_path)

            print('Storing audio file...')
            storage_result = utils.store_audio_file(file_path, word)
            
            if storage_result:
                print('Updating audio field on Anki...')
                utils.update_audio(config, note_id, word)
                
                audio_file_name = f'{word}.mp3'
            
                db.update_entry(audio_file_name, note_id)
                
                print('Update complete!\n')
            else:
                print('Could not store audio file.')
                print('Following to the next word...\n')
            
            # Tries to remove the file after update.
            try:
                # If the file is missing, it continues without errors.
                Path(file_path).unlink(missing_ok=True)
            except Exception as e:
                print(f"An error occurred while trying to delete the file: {e}")
            
            # Cleans the file path so the loop works properly.
            handler.caught_file = None
    finally:
        observer.stop()
        observer.join()
    
    print('All done! Every card without audio was updated!')
    
    db.end_connection()
    
    input("\nPress Enter to end the program.")

if __name__ == "__main__":
    main()