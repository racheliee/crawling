from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd
import requests
import time
import mojito

# Read Telegram API key and chat ID from file
key_file = open("./telegram-key.txt", "r")
lines = key_file.readlines()

TELEGRAM_BOT_TOKEN = lines[0].strip()
CHAT_ID = lines[1].strip()  # change this dynamically later

key_file.close()

# Read KIS API credentials from file
kis_file = open("./kis-keys.txt", "r")
lines = kis_file.readlines()

KIS_API_KEY = lines[0].strip()
KIS_API_SECRET = lines[1].strip()
KIS_ACC_NO = lines[2].strip()

kis_file.close()

# Initialize broker
broker = mojito.KoreaInvestment(
    api_key=KIS_API_KEY,
    api_secret=KIS_API_SECRET,
    acc_no=KIS_ACC_NO,  # 계좌번호
    mock=False  # 모의투자로 진행
)

# Function to send a message via Telegram bot
def send_message(bot, chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)


# Function to handle /balance command
def balance(update, context):
    # TODO: implement balance function and send message
    pass


# Function to handle /day_info command
def day_info(update, context):
    # TODO: implement day_info function and send message
    pass


# Function to send hourly updates
def hourly_update(context: CallbackContext):
    #TODO: implement hourly_update function
    pass


# Main function to start the bot
def main():
    # Initialize the bot
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('balance', balance))
    dp.add_handler(CommandHandler('day_info', day_info))
    
    # JobQueue to send hourly updates
    job_queue = updater.job_queue
    job_queue.run_repeating(hourly_update, interval=3600, first=0) # interval in seconds

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
