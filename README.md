# IP Info Bot

A Telegram bot that provides information about IP addresses.

## Requirements
- [pytelegrambotapi](https://pypi.org/project/pytelegrambotapi/)
- [requests](https://pypi.org/project/requests/)

You can install these dependencies using the following command:
```bash
pip install pytelegrambotapi requests
```

## Configuration
Make sure to create a `config.py` file with the following content:

```python
# config.py
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# List of available commands
cmds = ['/start', '/stop', '/help', '/get']
```

Replace `'YOUR_TELEGRAM_BOT_TOKEN'` with your actual Telegram bot token.

## Usage

1. Start the bot by running the script.
2. Type `/start` to initiate a conversation with the bot.
3. Use the `/get` command followed by an IP address to retrieve information about that IP.

Example:
```
/get 8.8.8.8
```

## Commands

- `/start`: Start the conversation and receive a welcome message.
- `/stop`: Stop the conversation and receive a goodbye message.
- `/help`: Get information about available commands.
- `/get {ip}`: Retrieve information about the specified IP address.

## Note
- The bot provides detailed information about the IP address, including continent, country, city, postal code, latitude, longitude, and the provider name.
- It also sends a location map associated with the provided IP address.

Feel free to explore and enhance the functionality of this bot!
