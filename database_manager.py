"""
Contains database related classes that manages general 
database CRUD.
"""

import sqlite3
from typing import Any

from enum import Flag, auto
from config_manager import Config

type DatabaseEntry = tuple[int, str, str | None, str | None, str]


class QueryFilter(Flag):
    NONE = 0
    AUDIOLESS = auto()
    UPDATED = auto()
    ALL = AUDIOLESS | UPDATED


class DatabaseHandler:
    """
    Main class for database connections.
    Contains a set of methods that allow database manipulation.
    """
    
    DB_NAME = "oto_connect_data.db"
    
    def __init__(self, config_instance: Config) -> None:
        self.con = sqlite3.connect(self.DB_NAME)
        self.cur = self.con.cursor()
        self._config = config_instance
    
    def table_setup(self) -> None:
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS notes(
                note_id INTEGER NOT NULL PRIMARY KEY,
                word TEXT NOT NULL,
                audio_file TEXT,
                update_date DATE,
                status VARCHAR(20) DEFAULT 'NO AUDIO'
            )
        """)

        self.con.commit()
        
    def update_table(self, note_info: list[dict[str, Any]]) -> None:
        """
        Updates the database inserting new words fetched from Anki.
        
        :param note_info: A list in the AnkiConnect API pattern is 
        expected.
        """
        for note in note_info:
            word = note['fields'][self._config.word_field]['value']
            note_id = note['noteId']
            
            self._store_note_data(note_id, word)

    def update_entry(self, audio_file: str, note_id: int) -> None:
        """
        Updates an entry in the database when an audio is stored,
        adding an update date and an audio file as well as changing
        its status to 'UPDATED'.
        """
        tuple_data = (audio_file, note_id)
        
        self.cur.execute("""
                    UPDATE notes
                    SET audio_file = (?),
                    update_date = CURRENT_DATE,
                    status = 'UPDATED'
                    WHERE note_id = (?)
        """, tuple_data)
        
        self.con.commit()
        
    def get_word_list(self, filter_type: QueryFilter) -> list[DatabaseEntry]:
        query_filters = {
            QueryFilter.ALL:       "SELECT * FROM notes",
            QueryFilter.AUDIOLESS: "SELECT * FROM notes WHERE status = 'NO AUDIO'",
            QueryFilter.UPDATED:   "SELECT * FROM notes WHERE status = 'UPDATED'",
        }
        
        sql_query = query_filters.get(filter_type)
        
        return self.cur.execute(sql_query).fetchall()
    
    def get_word_count(self, filter_type: QueryFilter) -> int:
        query_filters = {
            QueryFilter.ALL:       "SELECT Count(*) FROM notes",
            QueryFilter.AUDIOLESS: "SELECT Count(*) FROM notes WHERE status = 'NO AUDIO'",
            QueryFilter.UPDATED:   "SELECT Count(*) FROM notes WHERE status = 'UPDATED'",
        }
        
        sql_query = query_filters.get(filter_type)
        
        query_result = self.cur.execute(sql_query).fetchone()
        
        return query_result[0]
    
    def get_loop_list(self) -> list[tuple[int, str]]:
        """
        Returns a list of words used in the main program loop.
        """
        sql_query = "SELECT note_id, word FROM notes WHERE status = 'NO AUDIO'" 
        
        return self.cur.execute(sql_query).fetchall()
        
    def end_connection(self) -> None:
        self.con.close()
        
    def _store_note_data(self, note_id: int, word: str) -> None:
        """
        Stores data regarding audioless Anki notes unless a conflict 
        occurs.
        """
        tuple_data = (note_id, word)
        
        self.cur.execute("""
            INSERT INTO notes (note_id, word)
            VALUES (?, ?)
            ON CONFLICT (note_id) DO NOTHING
        """, tuple_data)
        
        self.con.commit()