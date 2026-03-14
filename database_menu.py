"""Adds an interactive menu that supports limited database queries."""

from enum import Enum, auto

from tabulate import tabulate

from database_manager import QueryFilter, DatabaseHandler


class QueryOption(Enum):
    WORD = auto()
    WORD_COUNT = auto()


def query_handler(database_instance: DatabaseHandler) -> None:
    print('--- Database Queries ---\n')
    
    option = None
    
    while option is None:
        print('Select one of the following options:\n')
        print('[1] Word Query')
        print('[2] Word Count Query')
        print('[3] Exit\n')
        
        try:
            choice = int(input('Option: '))

            match choice:
                case 1: option = QueryOption.WORD
                case 2: option = QueryOption.WORD_COUNT
                case 3: return
                case _: 
                    print('You must enter a valid number!\n')
                    continue
            
        except ValueError:
            print('You must enter a valid number!\n')
            continue
        except Exception as e:
            print(f'An unexpected error occurred: {e}\n')
            continue
            
        filters = select_query_filter()
        
        if filters is None:
            option = None
    
    if option == QueryOption.WORD:
        word_list = database_instance.get_word_list(filters)
        
        headers = ['Note Id', 'Word', 'Audio File', 'Update Date', 'Status']
        
        print(tabulate(word_list, headers, tablefmt="simple_grid"))
    else:
        word_count = database_instance.get_word_count(filters)
        
        print(f'There are {word_count} entries matching this filters in the database\n')
        
    input("Press Enter to continue.")

            
def select_query_filter() -> QueryFilter | None:
    option = None
    
    while option is None:
        print('Select the kind of words you want to search for:\n')
        print('[1] All Words')
        print('[2] Audioless Words')
        print('[3] Updated Words')
        print('[4] Exit\n')
        
        try:
            choice = int(input('Option: '))
            
            match choice:
                case 1: option = QueryFilter.ALL
                case 2: option = QueryFilter.AUDIOLESS
                case 3: option = QueryFilter.UPDATED
                case 4: return None
                case _: print('You must enter a valid number!\n')
        
        except ValueError:
            print('You must enter a valid number!\n')
        except Exception as e:
            print(f'An unexpected error occurred: {e}\n')
            
    return option