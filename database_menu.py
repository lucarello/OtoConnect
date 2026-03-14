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
            match choice:
                case 1: option = QueryOption.WORD
                case 2: option = QueryOption.WORD_COUNT
                case 3: return None
                
            filters = select_query_filter()
            
            if filters is None:
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
        
    match choice:
        case 1: option = QueryFilter.ALL
        case 2: option = QueryFilter.AUDIOLESS
        case 3: option = QueryFilter.UPDATED
        case 4: return None
            
    return option


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