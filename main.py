# pip install pytelegrambotapi
# pip install requests
import telebot
import json
from time import sleep
from config import *
import requests

bot = telebot.TeleBot(TOKEN)


def extract_arg(message):
    arg = message.split()
    if len(arg) >= 2:
        return arg[1]
    else:
        return ValueError


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Hello! This bot is designed to get information about the IP address.\nType /help to see available commands.')
    bot.send_message(message.chat.id, 'The data received may be incorrect.')


@bot.message_handler(commands=["stop"])
def stop(message):
    bot.send_message(message.chat.id, 'Bye :(')


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Get all information about IP - /get {ip}\n")


@bot.message_handler(commands=['get'])
def get(message):
    try:
        ip = extract_arg(message.text)

        len_ip = len(ip.split('.'))

        if not ip or ip == '' or ip == ' ' or len_ip != 4:
            bot.send_message(message.chat.id, 'You didn\'t enter an ip!')
        else:
            bot.send_message(message.chat.id, f'Please, wait about 5 seconds...')
            sleep(5)
            req = requests.get(f'https://ipdb.ipcalc.co/ipdata/{ip}')
            result = json.loads(req.text)
            url = f"https://www.google.com/maps/@{result['location']['latitude']},{result['location']['longitude']},10z"
            img_url = f"https://www.google.com/maps/@{result['location']['latitude']},{result['location']['longitude']},10z"
            bot.send_message(message.chat.id, f"Info about ip: {ip}\nContinent: {result['continent']['name']}\nCountry: {result['country']['name']}\nCity: {result['city']['name']}\nPostal code: {result['postal_code']}\nLatitude: {result['location']['latitude']}\nLongitude: {result['location']['longitude']}\nProvider name: {result['isp']['name']}\n<a href='{url}' >LOCATION</a>", parse_mode='HTML')
            bot.send_photo(message.chat.id, img_url)
            # bot.send_message(message.chat.id, f'<a href="{url}" >LOCATION</a>', parse_mode="HTML")
    except Exception as ex:
        # bot.send_message(message.chat.id, f'Invalid IP address! Do not use local IP addresses!')
        bot.send_message(message.chat.id, 'You didn\'t enter an ip!')


@bot.message_handler(content_types=['text'])
def check(message):
    try:
        text = message.text.split('/')
        if text[1] in cmds and message.text[1] != '' and message[0] != '':
            pass
        else:
            bot.send_message(message.chat.id, 'Command is not found! Type /help to see all commands')
    except:
        pass


bot.polling(none_stop=True, interval=0)
