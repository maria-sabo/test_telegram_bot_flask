import requests
import telebot
from flask import Flask
from flask import request
from flask import jsonify
import json

import config

URL = 'https://api.telegram.org/bot' + config.telegram_bot_token + '/'

# https://api.telegram.org/bot<token>/setWebhook?url=https://<...>.ngrok.io/

bot = telebot.TeleBot(config.telegram_bot_token, threaded=False)
app = Flask(__name__)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hello world")


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id


def get_message(data):
    message = data['message']['text']
    return message


def send_message(chat_id, text='hhwhjskd'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    bot.polling()
    if request.method == 'POST':
        data = request.get_json()
        chat_id = get_chat_id(data)
        message = get_message(data)
        write_json(data)
        if 'bitcoin' in message:
            send_message(chat_id, text='денег нет')
        # return jsonify(data)
    return '<h1>Bot welcomes you <3 </h1>'


if __name__ == '__main__':
    app.run()
