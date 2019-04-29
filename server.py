from app import create_app
from app.config import Configuration

app = create_app(config_class=Configuration)

if __name__ == '__main__':
    app.run()
