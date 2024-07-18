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
    balance = broker.fetch_balance()
    balance_message = "Current Balance:\n"
    for comp in balance['output1']:
        balance_message += f"Stock Code: {comp['pdno']}\n"
        balance_message += f"Stock Name: {comp['prdt_name']}\n"
        balance_message += f"Holding Quantity: {comp['hldg_qty']}\n"
        balance_message += f"Purchase Amount: {comp['pchs_amt']}\n"
        balance_message += f"Evaluation Amount: {comp['evlu_amt']}\n"
        balance_message += "-" * 40 + "\n"
    
    for comp in balance['output2']:
        balance_message += f"예수금: {comp['dnca_tot_amt']}\n"
        balance_message += f"총평가금액: {comp['tot_evlu_amt']}\n"
    
    send_message(context.bot, update.message.chat_id, balance_message)


# Function to handle /day_info command
def day_info(update, context):
    day_candlestick = broker.fetch_ohlcv(
        symbol="005930",
        timeframe='D',  # D: 일봉, W: 주봉, M: 월봉
        adj_price=True
    )

    day_df = pd.DataFrame(day_candlestick['output2'])
    day_dt = pd.to_datetime(day_df['stck_bsop_date'], format="%Y%m%d")
    day_df.set_index(day_dt, inplace=True)
    day_df = day_df[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr']]
    day_df.columns = ['open', 'high', 'low', 'close']
    day_df.index.name = "date"

    day_message = "Today's Stock Info for 005930:\n"
    latest_day = day_df.iloc[0]
    day_message += f"Date: {day_df.index[0].date()}\n"
    day_message += f"Open: {latest_day['open']}\n"
    day_message += f"High: {latest_day['high']}\n"
    day_message += f"Low: {latest_day['low']}\n"
    day_message += f"Close: {latest_day['close']}\n"
    
    send_message(context.bot, update.message.chat_id, day_message)


# Function to send hourly updates
def hourly_update(context: CallbackContext):
    result = broker.fetch_today_1m_ohlcv("005930")

    df = pd.DataFrame(result['output2'])
    dt = pd.to_datetime(df['stck_bsop_date'] + ' ' + df['stck_cntg_hour'], format="%Y%m%d %H%M%S")
    df.set_index(dt, inplace=True)
    df = df[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_prpr', 'cntg_vol']]
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index.name = "datetime"
    df = df[::-1]

    latest = df.iloc[0]
    update_message = (f"Hourly Update for 005930:\n"
                      f"Datetime: {latest.name}\n"
                      f"Open: {latest['open']}\n"
                      f"High: {latest['high']}\n"
                      f"Low: {latest['low']}\n"
                      f"Close: {latest['close']}\n"
                      f"Volume: {latest['volume']}\n")

    context.bot.send_message(chat_id=CHAT_ID, text=update_message)


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
