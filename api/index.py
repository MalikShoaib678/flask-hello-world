from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!\n\t Just testing vercel..'

@app.route('/about')
def about():
    return 'About'
