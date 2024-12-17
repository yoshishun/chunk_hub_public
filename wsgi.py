
from backend import app as application
from backend.config import BaseConfig

application.config.from_object(BaseConfig) 

if __name__ == "__main__":
    application.run(host=application.config['HOST'], port=application.config['PORT'], threaded=True)