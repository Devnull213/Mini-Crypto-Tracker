#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
response_search = 'btc-bitcoin'
url = 'https://api.coinpaprika.com/v1/tickers/btc-bitcoin'


@app.route('/')
def get_price():
    response = requests.get(url).json()
    return render_template('index.html', response=response)


@app.route('/get_query', methods=['POST'])
def get_query():
    search = request.form['coin']
    url_search = f'https://api.coinpaprika.com/v1/search?q={search}'
    global response_search
    response_search = requests.get(url_search).json()['currencies'][0]['id']
    return redirect(url_for('post_render'))


@app.route('/post_render')
def post_render():
    custom_url = f'https://api.coinpaprika.com/v1/tickers/{response_search}'
    custom_url = requests.get(custom_url).json()
    return render_template('index.html', response=custom_url)


@ socketio.on('trigger')
def send_price():
    while True:
        custom_url = f'https://api.coinpaprika.com/v1/tickers/{response_search}'
        response = requests.get(custom_url).json()
        emit('update', response)
        time.sleep(1)


if __name__ == '__main__':
    socketio.run(app, debug=True)
