
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "If you're seeing this, I'm probably rebuilding the site.  It should be back within seconds... If you just can't wait, go here: http://chimera.labs.oreilly.com/books/1234000000754"

