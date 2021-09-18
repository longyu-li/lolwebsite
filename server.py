from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Diamond by next April!</p>"
