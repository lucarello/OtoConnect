import sqlite3

class DatabaseHandler:
    
    DB_NAME = "oto_connect_data.db"
    
    def __init__(self):
        self.con = sqlite3.connect(self.DB_NAME)
        self.cur = self.con.cursor()

    def table_setup(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS notes(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER NOT NULL UNIQUE,
                word TEXT NOT NULL,
                audio_file TEXT,
                update_date DATE,
                status VARCHAR(20) DEFAULT 'NO AUDIO'
            )
        """)

        self.con.commit()

    def set_tuple(self, note_id, word):
        tuple_data = (note_id, word)
        
        self.cur.execute("""
            INSERT INTO notes (note_id, word)
            VALUES (?, ?)
            ON CONFLICT (note_id) DO NOTHING
        """, tuple_data)
        
        self.con.commit()

    def audio_update(self, audio_file, note_id):
        tuple_data = (audio_file, note_id)
        
        self.cur.execute("""
                    UPDATE notes
                    SET audio_file = (?),
                    update_date = CURRENT_DATE,
                    status = 'UPDATED'
                    WHERE note_id = (?)
        """, tuple_data)
        
        self.con.commit()
        
    def end_connection(self):
        self.con.close()