from app import app
from app.config import Configuration

if __name__ == '__main__':
    app.config.from_object(Configuration)
    app.run()
