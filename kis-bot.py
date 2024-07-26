from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd
import mojito
import logging

# Global variables
# broker = None
broker_mock = None
bot = None
CHAT_ID = None
fav_symbols = {"005930", "373220"}  # 삼성전자, 엔솔; set으로 관리해야 중복값 방지
all_symbols = None


# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Initialize global variables


def initialize_globals():
    global broker, broker_mock, bot, CHAT_ID, all_symbols

    # Read Telegram API key and chat ID from file
    with open("./telegram-key.txt", "r") as key_file:
        lines = key_file.readlines()
        TELEGRAM_BOT_TOKEN = lines[0].strip()
        CHAT_ID = lines[1].strip()  # change this dynamically later

    # Initialize bot
    bot = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    # Read KIS API credentials from file
    # with open("./kis-keys.txt", "r") as kis_file:
    #     lines = kis_file.readlines()
    #     KIS_API_KEY = lines[0].strip()
    #     KIS_API_SECRET = lines[1].strip()
    #     KIS_ACC_NO = lines[2].strip()

    # # Initialize broker
    # broker = mojito.KoreaInvestment(
    #     api_key=KIS_API_KEY,
    #     api_secret=KIS_API_SECRET,
    #     acc_no=KIS_ACC_NO,
    # )

    # Read KIS Mock API credentials from file
    with open("./kis-mock-keys.txt", "r") as kis_mock_file:
        lines = kis_mock_file.readlines()
        KIS_MOCK_API_KEY = lines[0].strip()
        KIS_MOCK_API_SECRET = lines[1].strip()
        KIS_MOCK_ACC_NO = lines[2].strip()

    # Initialize broker for mock API
    broker_mock = mojito.KoreaInvestment(
        api_key=KIS_MOCK_API_KEY,
        api_secret=KIS_MOCK_API_SECRET,
        acc_no=KIS_MOCK_ACC_NO,
        mock=True
    )

    # all_symbols = broker.fetch_symbols()
    all_symbols = broker_mock.fetch_symbols()

# Function to send a message via Telegram bot


def send_message(bot, chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

# Command handlers =============================================================================
def help(update, context):
    help_message = ("kis-bot 도움말:\n"
                    "-------------------------\n"
                    "/balance: 잔액 조회\n"
                    "/day_info: 오늘의 괌심 주식 정보 조회\n"
                    "/find_symbol [주식명]: 주식 종목코드 찾기\n"
                    "/favorites: 관심종목 조회\n"
                    "/add_to_fav [종목코드]: 관심종목 추가\n"
                    "/remove_from_fav [종목코드]: 관심종목 제거\n"
                    "/check_alerts: 설정된 주식 가격 알림 조회\n"
                    "/set_alert [종목코드] [가격]: 주식 가격 알림 설정\n"
                    "/cancel_alert [종목코드]: 주식 가격 알림 취소\n")

    send_message(context.bot, update.message.chat_id, help_message)


def balance(update, context):  # update is the message from the user, context is the bot
    # TODO: implement balance function
    pass


def day_info(update, context):
    # TODO: implement day_info function
    pass


def find_symbol(update, context):
    # Parse the message
    message = update.message.text
    message = message.split(' ')

    # Check if the message is valid
    if len(message) < 2:
        send_message(context.bot, update.message.chat_id, "종목명을 입력해주세요.")
        return

    # TODO: implement find_symbol function


def favorites(update, context):
    # TODO: implement favorites function
    pass


def add_to_fav(update, context):
   # TODO: implement add_to_fav function
    pass


def remove_from_fav(update, context):
    # TODO: implement remove_from_fav function
    pass


def check_alerts(update, context):
    # Read the alerts
    try:
        with open("alerts.txt", "r") as alerts_file:
            alerts = alerts_file.readlines()
    except FileNotFoundError:
        send_message(context.bot, update.message.chat_id, "알림이 없습니다.")
        return

    if not alerts:
        send_message(context.bot, update.message.chat_id, "알림이 없습니다.")
        return

    # Create the response message
    # TODO: implement check_alerts function


def set_alert(update, context):
    # Parse the message
    message = update.message.text
    message = message.split(' ')

    if len(message) < 3:
        send_message(context.bot, update.message.chat_id, "종목 코드와 가격을 입력해주세요.")
        return

    # TODO: implement set_alert function


def cancel_alert(update, context):
    # Parse the message
    message = update.message.text.split(' ')

    if len(message) < 2:
        send_message(context.bot, update.message.chat_id, "종목 코드를 입력해주세요.")
        return

    symbol = message[1]

    # TODO: implement cancel_alert function


# Job handlers ================================================================================
def alerts(context: CallbackContext):
    # Read the alerts
    try:
        with open("alerts.txt", "r") as alerts_file:
            alerts = alerts_file.readlines()
    except FileNotFoundError:
        return

    # TODO: implement alerts function


# Function to update the hourly data
def hourly_update(context: CallbackContext):
    # TODO: implement hourly update
    pass

# Main function
def main():
    initialize_globals()

    dp = bot.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('help', help))
    # TODO: add the rest of the command handlers

    # JobQueue to send hourly updates
    # hourly updates cannot be done through the mock API
    job_queue = bot.job_queue
    # job_queue.run_repeating(hourly_update, interval=3600, first=0) # interval in seconds (3600 for hourly)
    # TODO: add the rest of the job handlers

    # Start the bot
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
