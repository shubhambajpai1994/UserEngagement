#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/<user_id>')
def index(user_id):
    return user_id

if __name__ == '__main__':
    app.run(debug=True)