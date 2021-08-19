from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
	return render_template('home.html')

def run():
    app.run(host='0.0.0.0',port=8000)


def keep_alive():
    t = Thread(target=run)
    t.start()