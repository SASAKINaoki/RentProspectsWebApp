from flask import Flask, render_template, request
from backend.scraping.scraping import scraping
import batch

app=Flask(__name__, static_folder='./templates/images')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    return render_template('index.html')

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')
    


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')