"""
Contains user input related functions that gives support to other modules.
"""

import os

def get_choice(min_choice: int, max_choice: int) -> int | None:
    """
    Gets user choice ensuring it is an integer between 2 values.
    """
    try:
        choice = int(input('Option: '))
        
        if not min_choice <= choice <= max_choice:
            print('You must enter a valid number!\n')
            return None
        
        return choice        
    except ValueError:
        print('You must enter a valid number!\n')
        return None
    except Exception as e:
        print(f'An unexpected error occurred: {e}\n')
        return None
    
    
def clean_file_path(raw_file_path: str) -> str:
    """
    Cleans a file path name, eliminating empty
    spaces and quotes ('' or "") which can be
    automatically added by the terminal.
    
    :param raw_file_path: File path with possible
    quotes or empty spaces surrounding it.
    """
    clean_path = raw_file_path.strip()
     
    # "startswith" and "endswith" were preferred, since folders and 
    # files names may contain quotes.
    if clean_path.startswith('"') and clean_path.endswith('"'):
        clean_path = clean_path[1:-1]
    elif clean_path.startswith("'") and clean_path.endswith("'"):
        clean_path = clean_path[1:-1]
    
    return clean_path


def validate_path(file_path: str) -> bool:
    """
    Checks if the provided file path exists.
    """
    if not os.path.exists(file_path):
        print('Error: The file was not found. Please try again.\n')
        return False
    
    return True