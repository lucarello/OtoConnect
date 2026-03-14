"""Adds an interactive menu that supports limited database queries."""

from enum import Enum, auto

from tabulate import tabulate

from input_handler import get_choice
from database_manager import QueryFilter, DatabaseHandler


class QueryOption(Enum):
    WORD = auto()
    WORD_COUNT = auto()


def query_handler() -> tuple[QueryOption, QueryFilter] | None:
    print('--- Database Queries ---\n')
    
    choice = None 
    
    while choice is None:
        print('Select one of the following options:\n')
        print('[1] Word Query')
        print('[2] Word Count Query')
        print('[3] Exit\n')
        
        choice = get_choice(1, 3)
        
        if choice is not None:
            choice_map = {
                1: QueryOption.WORD,
                2: QueryOption.WORD_COUNT,
                3: None
            }
            option = choice_map.get(choice)
            
            if option is None:
                return None
                
            filters = select_query_filter()
            
            if filters is None:
                # Keeps the loop running if the user exits filter selection.
                choice = None

    return option, filters
    
            
def select_query_filter() -> QueryFilter | None:
    choice = None
    
    while choice is None:
        print('Select the kind of words you want to search for:\n')
        print('[1] All Words')
        print('[2] Audioless Words')
        print('[3] Updated Words')
        print('[4] Exit\n')
        
        choice = get_choice(1, 4)
    
    choice_map = {
        1: QueryFilter.ALL,
        2: QueryFilter.AUDIOLESS,
        3: QueryFilter.UPDATED,
        4: None
    }
            
    return choice_map.get(choice)


def show_query_results(database_instance: DatabaseHandler, 
                       option: QueryOption,
                       filters: QueryFilter) -> None:
    if option == QueryOption.WORD:
        word_list = database_instance.get_word_list(filters)
        
        headers = ['Note Id', 'Word', 'Audio File', 'Update Date', 'Status']
        
        print(tabulate(word_list, headers, tablefmt="simple_grid"))
    else:
        word_count = database_instance.get_word_count(filters)
        
        print(f'There are {word_count} entries matching these filters in the database\n')
        
    input("Press Enter to continue.")