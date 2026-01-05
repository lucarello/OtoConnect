import anki_utils
import webbrowser


def main():
    print('--- Welcome to OtoConnect! ---')
    
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
        print('\n---------------------------')
        word = note['fields']['Expression']['value']
        print(f'Current Word: {word}')
        
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
            
        print('Update complete!\n')
        
    print('All done! Every card without audio was updated!')


if __name__ == "__main__":
    main()