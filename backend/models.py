from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from backend.config import BaseConfig
import random, string


class DatabaseManager:
    
    def __init__(self):
        self.connection = None
        self.connect()  

    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=BaseConfig.DB_HOST,
                user=BaseConfig.DB_USER,
                password=BaseConfig.DB_PASSWORD,
                database=BaseConfig.DB_NAME
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    
    def execute_query(self, query, params=None):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    
    def fetch_query(self, query, params=None):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
        return result


class User(UserMixin):
    
    def __init__(self, id, name, email, password, active=True):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.active = active

    
    @property
    def is_active(self):
        return self.active

    @staticmethod
    
    def create_user(db_mng, user_id, name, email, password, active):
        hashed_password = generate_password_hash(password)
        query = """
        INSERT INTO tbl_users (id, name, email, password, active)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (user_id, name, email, hashed_password, active)
        db_mng.execute_query(query, params)

    @staticmethod
    
    def get_user_by_email(db_mng, email):
        query = "SELECT * FROM tbl_users WHERE email = %s"
        result = db_mng.fetch_query(query, (email,))
        if result:
            user_data = result[0]
            return User(
                user_data['id'],
                user_data['name'],
                user_data['email'],
                user_data['password'],
                user_data['active']
            )
        return None

    @staticmethod
    
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)



class Folder:
    
    def __init__(self, id, user_id, folder_class, name, notes, create_date, update_date=None):
        self.id = id
        self.user_id = user_id
        self.folder_class = folder_class
        self.name = name
        self.notes = notes
        self.create_date = create_date
        self.update_date = update_date

    @staticmethod
    
    def get_folder_name(db_mng, folder_id, user_id):
        sql = 'SELECT name FROM tbl_folders WHERE id=%s AND user_id=%s'
        params = (folder_id, user_id)
        return db_mng.fetch_query(sql, params)

    @staticmethod
    
    def get_chunk_folders_list(db_mng, user_id, folder_class):
        sql = 'SELECT * FROM tbl_folders WHERE user_id=%s AND class=%s ORDER BY id ASC'
        params = (user_id, folder_class)
        return db_mng.fetch_query(sql, params)

    @staticmethod
    
    def get_folders_list_all(db_mng, user_id):
        sql = 'SELECT * FROM tbl_folders WHERE user_id=%s ORDER BY id ASC'
        params = (user_id,)
        return db_mng.fetch_query(sql, params)

    @staticmethod
    
    def add_folder(db_mng, folder_id, folder_user_id, folder_class, folder_name, folder_notes, folder_create_date):
        sql = 'INSERT INTO tbl_folders (id, user_id, class, name, notes, create_date) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (folder_id, folder_user_id, folder_class, folder_name, folder_notes, folder_create_date)
        db_mng.execute_query(sql, params)
        
    @staticmethod
    def edit_folder(db_mng, folder_id, user_id, name, notes, update_date):
        sql = 'UPDATE tbl_folders SET name=%s, notes=%s, update_date=%s WHERE id=%s AND user_id=%s'
        params = (name, notes, update_date, folder_id, user_id)
        db_mng.execute_query(sql, params)

    @staticmethod
    def delete_folder(db_mng, folder_id, user_id):
        sql = 'DELETE FROM tbl_folders WHERE id=%s AND user_id=%s'
        params = (folder_id, user_id)
        db_mng.execute_query(sql, params)
        
    @staticmethod
    def get_total_pronounced_count(db_mng, folder_id, user_id):
        sql = '''
        SELECT SUM(pronounced_count) as total_count
        FROM tbl_chunks
        WHERE folder_id=%s AND user_id=%s
        UNION ALL
        SELECT SUM(pronounced_count) as total_count
        FROM tbl_chunk_sentences
        WHERE folder_id=%s AND user_id=%s
        '''
        params = (folder_id, user_id, folder_id, user_id)
        result = db_mng.fetch_query(sql, params)
        total_count = sum(row['total_count'] for row in result if row['total_count'] is not None)
        return total_count

    @staticmethod
    def get_item_count(db_mng, folder_id, user_id):
        sql = '''
        SELECT COUNT(*) as item_count
        FROM tbl_chunks
        WHERE folder_id=%s AND user_id=%s
        UNION ALL
        SELECT COUNT(*) as item_count
        FROM tbl_chunk_sentences
        WHERE folder_id=%s AND user_id=%s
        '''
        params = (folder_id, user_id, folder_id, user_id)
        result = db_mng.fetch_query(sql, params)
        item_count = sum(row['item_count'] for row in result if row['item_count'] is not None)
        return item_count
        


class Chunk:
    
    def __init__(self, id, user_id, folder_id, learning_chunk, translating_chunk, pronounced_count=0, politeness=None, nuance=None, situation=None, notes=None, create_date=None, update_date=None):
        self.id = id
        self.user_id = user_id
        self.folder_id = folder_id
        self.learning_chunk = learning_chunk
        self.translating_chunk = translating_chunk
        self.pronounced_count = pronounced_count
        self.politeness = politeness
        self.nuance = nuance  
        self.situation = situation 
        self.notes = notes
        self.create_date = create_date
        self.update_date = update_date

    @staticmethod
    
    def get_all_chunks_list(db_mng, user_id, folder_id=None):
        if folder_id is None:
            sql = 'SELECT * FROM tbl_chunks WHERE user_id=%s ORDER BY id ASC'
            params = (user_id,)
        else:
            sql = 'SELECT * FROM tbl_chunks WHERE user_id=%s AND folder_id=%s ORDER BY id ASC'
            params = (user_id, folder_id)
        return db_mng.fetch_query(sql, params)

    @staticmethod
    
    def add_chunk(db_mng, chunk_id, user_id, folder_id, learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_create_date):
        sql = 'INSERT INTO tbl_chunks (id, user_id, folder_id, learning_chunk, translating_chunk, politeness, nuance, situation, notes, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params = (chunk_id, user_id, folder_id, learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_create_date)
        db_mng.execute_query(sql, params)

    @staticmethod
    
    def edit_chunk(db_mng, learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_update_date, user_id, chunk_id):
        sql = 'UPDATE tbl_chunks SET learning_chunk=%s, translating_chunk=%s, politeness=%s, nuance=%s, situation=%s, notes=%s, update_date=%s WHERE user_id=%s AND id=%s'
        params = (learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_update_date, user_id, chunk_id)
        db_mng.execute_query(sql, params)

    @staticmethod
    
    def delete_chunk(db_mng, user_id, chunk_id):
        sql = 'DELETE FROM tbl_chunks WHERE user_id=%s AND id=%s'
        params = (user_id, chunk_id)
        db_mng.execute_query(sql, params)
        
    @staticmethod
    
    def update_pronounced_count(db_mng, pronounced_count, update_date, user_id, chunk_id):
        sql = 'UPDATE tbl_chunks SET pronounced_count=%s, update_date=%s WHERE user_id=%s AND id=%s'
        params = (pronounced_count, update_date, user_id, chunk_id)
        db_mng.execute_query(sql, params)
        
    @staticmethod
    def nullify_folder_id(db_mng, folder_id, user_id):
        sql = 'UPDATE tbl_chunks SET folder_id=NULL WHERE folder_id=%s AND user_id=%s'
        params = (folder_id, user_id)
        db_mng.execute_query(sql, params)


class ChunkSentence:
    
    def __init__(self, id, user_id, folder_id, chunk_sentence, translating_sentence, pronounced_count=0, politeness=None, situation=None, notes=None, create_date=None, update_date=None):
        self.id = id
        self.user_id = user_id
        self.folder_id = folder_id
        self.chunk_sentence = chunk_sentence
        self.translating_sentence = translating_sentence
        self.pronounced_count = pronounced_count
        self.politeness = politeness
        self.situation = situation
        self.notes = notes
        self.create_date = create_date
        self.update_date = update_date

    @staticmethod
    
    def get_chunk_sentences_list(db_mng, user_id, folder_id=None):
        if folder_id is None:
            sql = 'SELECT * FROM tbl_chunk_sentences WHERE user_id=%s ORDER BY id ASC'
            params = (user_id,)
        else:
            sql = 'SELECT * FROM tbl_chunk_sentences WHERE user_id=%s AND folder_id=%s ORDER BY id ASC'
            params = (user_id, folder_id)
        return db_mng.fetch_query(sql, params)

    @staticmethod
    
    def create_chunk_sentence(db_mng, chunk_sentence_id, user_id, folder_id, chunk_sentence, translating_sentence, politeness, situation, notes, chunk_sentence_create_date):
        sql = 'INSERT INTO tbl_chunk_sentences (id, user_id, folder_id, chunk_sentence, translating_sentence, politeness, situation, notes, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params = (chunk_sentence_id, user_id, folder_id, chunk_sentence, translating_sentence, politeness, situation, notes, chunk_sentence_create_date)
        db_mng.execute_query(sql, params)

    @staticmethod
    
    def edit_chunk_sentence(db_mng, chunk_sentence, translating_sentence, politeness, situation, notes, update_date, user_id, chunk_sentence_id):
        sql = 'UPDATE tbl_chunk_sentences SET chunk_sentence=%s, translating_sentence=%s, politeness=%s, situation=%s, notes=%s, update_date=%s WHERE user_id=%s AND id=%s'
        params = (chunk_sentence, translating_sentence, politeness, situation, notes, update_date, user_id, chunk_sentence_id)
        db_mng.execute_query(sql, params)
        
    @staticmethod
    
    def delete_chunk_sentence(db_mng, user_id, chunk_sentence_id):
        sql = 'DELETE FROM tbl_chunk_sentences WHERE user_id=%s AND id=%s'
        params = (user_id, chunk_sentence_id)
        db_mng.execute_query(sql, params)

    @staticmethod
    
    def update_pronounced_count(db_mng, pronounced_count, update_date, user_id, chunk_sentence_id):
        sql = 'UPDATE tbl_chunk_sentences SET pronounced_count=%s, update_date=%s WHERE user_id=%s AND id=%s'
        params = (pronounced_count, update_date, user_id, chunk_sentence_id)
        db_mng.execute_query(sql, params)
        
    @staticmethod
    def calculate_politeness(db_mng, chunk_sentence_id):
        
        sql = 'SELECT c.politeness FROM tbl_chunks c JOIN tbl_chunk_sentence_links l ON c.id = l.chunk_id WHERE l.sentence_id = %s'
        params = (chunk_sentence_id,)
        chunks = db_mng.fetch_query(sql, params)
        if not chunks:
            return None
        politeness_sum = sum(chunk['politeness'] for chunk in chunks if chunk['politeness'] is not None)
        politeness_count = len([chunk for chunk in chunks if chunk['politeness'] is not None])
        return politeness_sum / politeness_count if politeness_count > 0 else None


class ChunkSentenceLink:
    
    def __init__(self, user_id, chunk_id, sentence_id, create_date, update_date=None):
        self.user_id = user_id
        self.chunk_id = chunk_id
        self.sentence_id = sentence_id
        self.create_date = create_date
        self.update_date = update_date

    @staticmethod
    
    def add_link(db_mng, user_id, chunk_id, chunk_sentence_id, create_date):
        sql = 'INSERT INTO tbl_chunk_sentence_links (user_id, chunk_id, sentence_id, create_date) VALUES (%s, %s, %s, %s)'
        params = (user_id, chunk_id, chunk_sentence_id, create_date)
        db_mng.execute_query(sql, params)

    @staticmethod
    
    def delete_links(db_mng, chunk_sentence_id):
        sql = 'DELETE FROM tbl_chunk_sentence_links WHERE sentence_id=%s'
        params = (chunk_sentence_id,)
        db_mng.execute_query(sql, params)

    @staticmethod
    
    def get_links(db_mng, user_id, chunk_sentence_id):
        sql = 'SELECT chunk_id FROM tbl_chunk_sentence_links WHERE sentence_id=%s AND user_id=%s'
        params = (chunk_sentence_id, user_id)
        return db_mng.fetch_query(sql, params)


class Statistics:
    @staticmethod
    
    def get_chunk_registration_data(db_mng, user_id):
        sql = """
        SELECT DATE(create_date) as registration_date, COUNT(*) as count
        FROM tbl_chunks
        WHERE user_id=%s AND create_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY DATE(create_date)
        """
        return db_mng.fetch_query(sql, (user_id,))

    @staticmethod
    
    def get_chunk_sentence_registration_data(db_mng, user_id):
        sql = """
        SELECT DATE(create_date) as registration_date, COUNT(*) as count
        FROM tbl_chunk_sentences
        WHERE user_id=%s AND create_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY DATE(create_date)
        """
        return db_mng.fetch_query(sql, (user_id,))

    @staticmethod
    def get_chunk_pronounced_counts(db_mng, user_id):
        sql = """
        SELECT DATE(create_date) as date, SUM(pronounced_count) as total_pronounced_count
        FROM tbl_chunk_pronounced_counts
        WHERE user_id=%s AND DATE(create_date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY DATE(create_date)
        """
        return db_mng.fetch_query(sql, (user_id,))

    @staticmethod
    def get_chunk_sentence_pronounced_counts(db_mng, user_id):
        sql = """
        SELECT DATE(create_date) as date, SUM(pronounced_count) as total_pronounced_count
        FROM tbl_chunk_sentence_pronounced_counts
        WHERE user_id=%s AND DATE(create_date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY DATE(create_date)
        """
        return db_mng.fetch_query(sql, (user_id,))



class ChunkPronouncedCount:
    @staticmethod
    def add_or_update_pronounced_count(db_mng, user_id, chunk_id, current_session_count, update_date):
        sql_check = """
        SELECT pronounced_count FROM tbl_chunk_pronounced_counts
        WHERE user_id=%s AND chunk_id=%s AND DATE(create_date)=DATE(%s)
        """
        params_check = (user_id, chunk_id, update_date)
        existing_record = db_mng.fetch_query(sql_check, params_check)

        print("ChunkPronouncedCount existing_record: ", existing_record)
        if existing_record:
            existing_count = existing_record[0]['pronounced_count']
            new_count = existing_count + current_session_count
            
            sql_update = """
            UPDATE tbl_chunk_pronounced_counts
            SET pronounced_count=%s, update_date=%s
            WHERE user_id=%s AND chunk_id=%s AND DATE(create_date)=DATE(%s)
            """
            params_update = (new_count, datetime.now(), user_id, chunk_id, update_date)
            db_mng.execute_query(sql_update, params_update)
        else:
            sql_insert = """
            INSERT INTO tbl_chunk_pronounced_counts (user_id, chunk_id, pronounced_count, create_date, update_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            params_insert = (user_id, chunk_id, current_session_count, update_date, None)
            db_mng.execute_query(sql_insert, params_insert)


class ChunkSentencePronouncedCount:
    @staticmethod
    def add_or_update_pronounced_count(db_mng, user_id, chunk_sentence_id, current_session_count, update_date):
        sql_check = """
        SELECT pronounced_count FROM tbl_chunk_sentence_pronounced_counts
        WHERE user_id=%s AND chunk_sentence_id=%s AND DATE(create_date)=DATE(%s)
        """
        params_check = (user_id, chunk_sentence_id, update_date)
        existing_record = db_mng.fetch_query(sql_check, params_check)

        print("ChunkSentencePronouncedCount existing_record: ", existing_record)
        if existing_record:
            existing_count = existing_record[0]['pronounced_count']
            new_count = existing_count + current_session_count
            
            sql_update = """
            UPDATE tbl_chunk_sentence_pronounced_counts
            SET pronounced_count=%s, update_date=%s
            WHERE user_id=%s AND chunk_sentence_id=%s AND DATE(create_date)=DATE(%s)
            """
            params_update = (new_count, datetime.now(), user_id, chunk_sentence_id, update_date)
            db_mng.execute_query(sql_update, params_update)
        else:
            sql_insert = """
            INSERT INTO tbl_chunk_sentence_pronounced_counts (user_id, chunk_sentence_id, pronounced_count, create_date, update_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            params_insert = (user_id, chunk_sentence_id, current_session_count, update_date, None)
            db_mng.execute_query(sql_insert, params_insert)
