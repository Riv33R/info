from flask import Flask, render_template, request

import pandas as pd

csvfile = "data.csv"

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('spravka.html')

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=4000, debug=False)

