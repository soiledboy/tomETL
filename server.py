from os import environ
from backend.app import create_app

app = create_app("backend.settings")

if __name__ == "__main__":
    app.run(port=5000)
