"""
Contains user input related functions that gives support to other modules.
"""

def get_choice(min_choice: int, max_choice: int) -> int | None:
    """
    Gets user choice, ensuring it is an integer between 2 values.
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