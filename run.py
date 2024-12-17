from backend import app
from backend.config import BaseConfig

app.config.from_object(BaseConfig)

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], threaded=True)