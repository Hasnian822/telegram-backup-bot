import telebot
import requests
import time
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot('6708098949:AAEzb1OKxRQpMlCnPbcFOyJmZ5QWZESX1fA')

ids = {}
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Message ka sender ID
    chat_id = message.chat.id
    # Aapka response
    response = "Sorry for the inconvenience, but the bot is currently undergoing maintenance. We are working hard to improve your experience and will be back online soon. Thank you for your patience!"
    # Response ko sender ko bhejein
    bot.send_message(chat_id, response)

def stop_this_instance():
    bot.stop_polling()
    print("bot stopped")
    
# Variables to control bot polling
start_flag = True
stop_flag = False

def check_web_app(url):
    try:
        global stop_flag
        global start_flag
        response = requests.get(url)
        if response.status_code == 200:
            print("Web app is up and running!")
            if stop_flag:
                time.sleep(30)
                print("stopping bot")
                stop_this_instance()
                print("bot stopped")
                admin_id = 5766884382
                bot.send_message(admin_id, "<b>⚠ Warning</b>\n\nBackup Bot is stopped and main bot should start now", parse_mode='HTML')
                stop_flag = False

        else:
            print("Web app is down!")
            stop_flag = True
            print("starting bot")
            # Run bot.polling() in a separate thread
            polling_sub_thread = threading.Thread(target=bot_polling)
            polling_sub_thread.start()
            print("bot  started")

    except requests.ConnectionError:
        print("Connection error. Web app may be down.")

def checker():
    while True:
        flask_url = f"https://clicks4clicks-bot-hasnain.koyeb.app/"  # Change this to your Flask web app URL

        print("checking web app")
        polling_thread = threading.Thread(target=check_web_app, args=(flask_url,))
        polling_thread.start()
        time.sleep(40)  # Check every 10 seconds
        
# Function to start the polling thread
def start_polling_thread():
    polling_thread = threading.Thread(target=checker)
    polling_thread.start()
    
# Start the bot polling thread
start_polling_thread()

# Function to start bot polling in a separate thread
def bot_polling():
    # Run bot.polling() in a separate thread
    admin_id = 5766884382
    bot.send_message(admin_id, "<b>🚨 Error</b>\n\nMain bot is down and Backup Bot is started!", parse_mode='HTML')
    bot.polling(none_stop=True)

# Keep the main thread alive
while True:
    try:
        time.sleep(3600)
    except KeyboardInterrupt:
        logger.debug("Bot stopped manually.")
        break
