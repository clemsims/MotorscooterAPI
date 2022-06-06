from app import create_app
from flask import Flask

app = create_app()
if __name__ == '__main__':

    app.secret_key = "motorscooter"  # Key
    app.run()