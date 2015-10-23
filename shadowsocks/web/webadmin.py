from flask import Flask

app = Flask(__name__)



def start():
    app.run(port=23901)
