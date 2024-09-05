from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd
import mojito
import logging # pip install logging

# Global variables
# broker = None
broker_mock = None
bot = None
CHAT_ID = None
fav_symbols = set() #{} => dictionary
# {"005930", "373220"}  # 삼성전자, 엔솔; set으로 관리해야 중복값 방지
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
    
    # initalize favorite symbols
    with open("./favourites.txt", "r") as fav_file:
        lines = fav_file.readlines()
        for symbol in lines:
            fav_symbols.add(symbol.strip())
        # fav_symbols = {symbol.strip() for symbol in fav_symbols}

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
                    "/day_info: 오늘의 관심 주식 정보 조회\n"
                    "/find_symbol [주식명]: 주식 종목코드 찾기\n"
                    "/favorites: 관심종목 조회\n"
                    "/add_to_fav [종목코드]: 관심종목 추가\n"
                    "/remove_from_fav [종목코드]: 관심종목 제거\n"
                    "/check_alerts: 설정된 주식 가격 알림 조회\n"
                    "/set_alert [종목코드] [가격]: 주식 가격 알림 설정\n"
                    "/cancel_alert [종목코드]: 주식 가격 알림 취소\n")

    send_message(context.bot, update.message.chat_id, help_message)


def balance(update, context):  # update is the message from the user, context is the bot
    balance = broker_mock.fetch_balance() # broker.fetch_balance()
    
    balance_message = "current balance: \n"
    for comp in balance['output1']:
        balance_message += f"종목이름: {comp['prdt_name']}\n"
        balance_message += f"보유수량: {comp['hldg_qty']}\n"
        balance_message += f"매입금액: {comp['pchs_amt']}\n"
        balance_message += f"평가금액: {comp['evlu_amt']}\n"
        balance_message += "-" * 40 + "\n"
        
    for comp in balance['output2']:
        balance_message += f"예수금: {comp['dnca_tot_amt']}\n"
        balance_message += f"총평가금액: {comp['tot_evlu_amt']}\n"
    
    send_message(context.bot, update.message.chat_id, balance_message)


def day_info(update, context):
    day_message = "오늘의 주식 정보:\n"
    
    for symbol in fav_symbols:
        day_candlestick = broker_mock.fetch_ohlcv(
            symbol=symbol,
            timeframe='D',
            adj_price=True
        )
        
        day_df = pd.DataFrame(day_candlestick['output2'])
        day_dt = pd.to_datetime(day_df['stck_bsop_date'], format="%Y%m%d")
        day_df.set_index(day_dt, inplace=True)
        day_df = day_df[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr']]
        day_df.columns = ['open', 'high', 'low', 'close']
        day_df.index.name = "date"
        
        latest_day = day_df.iloc[0]
        day_message += f"\n종목이름: {day_candlestick['output1']['hts_kor_isnm']}\n"
        day_message += f"시가: {latest_day['open']}\n"
        day_message += f"고가: {latest_day['high']}\n"
        day_message += f"저가: {latest_day['low']}\n"
        day_message += f"종가: {latest_day['close']}\n"
        day_message += '-'*40 + '\n'
        
    send_message(context.bot, update.message.chat_id, day_message)
        
def find_symbol(update, context):
    # Parse the message
    message = update.message.text
    message = message.split(' ')

    # Check if the message is valid
    if len(message) < 2:
        send_message(context.bot, update.message.chat_id, "종목명을 입력해주세요.")
        return

    name = message[1] # 찾고 싶은 종목
    
    # find the symbol
    found_symbols = all_symbols[all_symbols['한글명'].str.contains(name)]
    
    # create message
    response_message = "주식명 (종목코드): \n"
    response_message += "-" * 40 + "\n";
    
    if found_symbols.empty:
        response_message += "해당 종목이름을 찾지 못했습니다"
    else:
        for i in range(len(found_symbols)):
            response_message += f"{found_symbols.iloc[i]['한글명']} ({found_symbols.iloc[i]['단축코드']})\n" #현대차 (001500)
            
    send_message(context.bot, update.message.chat_id, response_message)

def favorites(update, context):
    fav_message = "관심종목: \n"
    fav_message += "-" * 40 + "\n"
    
    for sym in fav_symbols:
        fav_message += f"{all_symbols[all_symbols['단축코드'] == sym]['한글명'].values[0]} "
        fav_message += f"{sym}\n"
    
    send_message(context.bot, update.message.chat_id, fav_message);
    


def add_to_fav(update, context):
    # parse the message
    message = update.message.text
    message = message.split(" ")
    
    # check if message has a code
    if len(message) < 2:
        send_message(context.bot, update.message.chat_id, "종목코드를 입력해주세요")
        return
    
    symbol = message[1]
    
    # check if symbol is valid
    if symbol not in all_symbols['단축코드'].values:
        send_message(context.bot, update.message.chat_id, "유효하지 않은 종목코드입니다")
        return
    
    # add symbol
    fav_symbols.add(symbol)
     
    # update the text file
    with open("./favourites.txt", "a") as fav_file:
        fav_file.write("\n" + symbol) # file 끝에 newline 있으면 안됨
    
    send_message(context.bot, update.message.chat_id, f"{symbol}이/가 관심종목에 추가 되었습니다")
        

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
    dp.add_handler(CommandHandler('help', help)) # '/help' --> help()
    dp.add_handler(CommandHandler('balance', balance)) #'balance' --> balance()
    dp.add_handler(CommandHandler('day_info', day_info))
    dp.add_handler(CommandHandler('find_symbol', find_symbol))
    dp.add_handler(CommandHandler('favorites', favorites))
    dp.add_handler(CommandHandler("add_to_fav", add_to_fav))
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
