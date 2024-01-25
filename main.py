# pip install pytelegrambotapi
# pip install requests
import telebot
import json
from time import sleep
import requests
from config import TOKEN, cmds

bot = telebot.TeleBot(TOKEN)

CMD_START = '/start'
CMD_STOP = '/stop'
CMD_HELP = '/help'
CMD_GET = '/get'

MESSAGES = {
    'WELCOME': 'Hello! This bot is designed to get information \
        about the IP address.\nType /help to see available commands.',
    'GOODBYE': 'Bye :(',
    'HELP': 'Get all information about IP - /get {ip}\n',
    'INVALID_IP': 'You didn\'t enter a valid IP!',
    'WAIT_MESSAGE': 'Please, wait about 5 seconds...',
    'COMMAND_NOT_FOUND': 'Command is not found! \
        Type /help to see all commands',
    'INVALID_IP_ADDRESS': 'Invalid IP address! \
        Please, enter a valid IP address.'
}

URLS = {
    'MAPS': "https://www.google.com/maps/@{latitude},{longitude},10z",
    'IPDATA': 'https://ipdb.ipcalc.co/ipdata/{}'
}

INFO_MESSAGE_TEMPLATE = (
    "Info about IP: {ip}\n"
    "Continent: {continent}\n"
    "Country: {country}\n"
    "City: {city}\n"
    "Postal code: {postal_code}\n"
    "Latitude: {latitude}\n"
    "Longitude: {longitude}\n"
    "Provider name: {provider_name}\n"
    "<a href='{location_url}' >LOCATION</a>"
)


def send_message(chat_id, text, parse_mode=None):
    """
    Send a message to the specified chat ID.

    Args:
        chat_id (int): Telegram chat ID.
        text (str): Message text.
        parse_mode (str, optional): The parse mode (e.g., 'HTML').
    """
    bot.send_message(chat_id, text, parse_mode=parse_mode)


def get_ip_info(message, ip):
    """
    Retrieve information about the given IP address.

    Args:
        message (obj): Telegram message object.
        ip (str): IP address to get information about.
    """
    try:
        len_ip = len(ip.split('.'))
        if not ip or ip.isspace() or len_ip != 4:
            send_message(message.chat.id, MESSAGES['INVALID_IP'])
            return

        send_message(message.chat.id, MESSAGES['WAIT_MESSAGE'])
        sleep(5)
        req = requests.get(URLS['IPDATA'].format(ip))
        result = json.loads(req.text)
        url = URLS['MAPS'].format(
            latitude=result['location']['latitude'],
            longitude=result['location']['longitude']
            )
        img_url = URLS['MAPS'].format(
            latitude=result['location']['latitude'],
            longitude=result['location']['longitude']
            )
        info_message = INFO_MESSAGE_TEMPLATE.format(
            ip=ip,
            continent=result['continent']['name'],
            country=result['country']['name'],
            city=result['city']['name'],
            postal_code=result['postal_code'],
            latitude=result['location']['latitude'],
            longitude=result['location']['longitude'],
            provider_name=result['isp']['name'],
            location_url=url
        )
        send_message(message.chat.id, info_message, parse_mode='HTML')
        bot.send_photo(message.chat.id, img_url)
    except Exception:
        send_message(message.chat.id, MESSAGES['INVALID_IP_ADDRESS'])


def check_command(message):
    """
    Check if the command in the message is valid.

    Args:
        message (obj): Telegram message object.
    """
    try:
        text = message.text.split('/')
        if text[1] not in cmds or message.text[1] == '' or message[0] == '':
            send_message(message.chat.id, MESSAGES['COMMAND_NOT_FOUND'])
    except Exception:
        pass


@bot.message_handler(commands=[CMD_START])
def start(message):
    """
    Handle the /start command and send a welcome message.

    Args:
        message (obj): Telegram message object.
    """
    send_message(message.chat.id, MESSAGES['WELCOME'])
    send_message(message.chat.id, MESSAGES['INVALID_IP'])


@bot.message_handler(commands=[CMD_STOP])
def stop(message):
    """
    Handle the /stop command and send a goodbye message.

    Args:
        message (obj): Telegram message object.
    """
    send_message(message.chat.id, MESSAGES['GOODBYE'])


@bot.message_handler(commands=[CMD_HELP])
def help(message):
    """
    Handle the /help command and send information about available commands.

    Args:
        message (obj): Telegram message object.
    """
    send_message(message.chat.id, MESSAGES['HELP'])


@bot.message_handler(commands=[CMD_GET])
def get(message):
    """
    Handle the /get command and retrieve information about IP address.

    Args:
        message (obj): Telegram message object.
    """
    if len(message.text.spit()) < 2:
        return None

    ip = message.text.split()[1]
    get_ip_info(message, ip)


@bot.message_handler(content_types=['text'])
def check(message):
    """
    Check if the command in the message is valid.

    Args:
        message (obj): Telegram message object.
    """
    check_command(message)


bot.polling(none_stop=True, interval=0)
