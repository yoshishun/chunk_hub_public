
class BaseConfig(object):
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 5050
    
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'your_secret_key'
    
    DB_HOST = ''
    DB_USER = ''
    DB_PASSWORD = ''
    DB_NAME = ''
