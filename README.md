# Telegram Bot

This is a simple Telegram bot built with Python using the `python-telegram-bot` library.

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install python-telegram-bot
   ```

## Usage

1. **Run the bot:**
   ```bash
   python bot.py
   ```
2. **Interact with your bot on Telegram:**
   - Find your bot by its username and send `/start` to receive a welcome message.

## Configuration

- The bot token is hardcoded in `bot.py`. For production, consider using environment variables for security.

## Requirements
- Python 3.7+
- `python-telegram-bot` library 