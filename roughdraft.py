from flask import Flask

app = Flask(__name__)

print('top ', __name__)

@app.route('/')
def hello():
    return 'Hello All'

@app.route('/welcome')
def welc():
    return 'Welcome!'

if __name__ == "__main__":
    app.run(debug=1, host='0.0.0.0', port=5000)