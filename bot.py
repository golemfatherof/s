import random
import string
import time
import threading
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Define your variables here
ADMIN_ID = 7584228621  # Set your admin ID here
CHANNEL_1 = 'https://t.me/botchnl1'
CHANNEL_2 = 'https://t.me/botchnl2n'
MAX_ATTACKS = 20 # Maximum attacks per user
bots = []
keys = {}
users = {}

# List of 15 bot tokens (replace with your actual bot tokens)
BOT_TOKENS = [
    "7921093614:AAFvmlFfYRGLCbYLpEy4cWfjHqKxB8zrHUc", "7626829450:AAHZcmcFqNukoEK4x3s-s6Pt_n2jH5HGvE8", "7989339807:AAExWVUAdIlvtiMxCCMp4zlDJ-gZZZ8bsUM", 
    "7689914997:AAHT7onkIoXwndOQiDsuM0Z-ubfrYgEN3Ok", "7726337899:AAGmIxER4WRow6gScabwK_EFrV6Oe6ugu_s", "7746324666:AAEhicwuwx9efzdTy7nE1fR4gtYDPBkmW3g", 
    "7612353186:AAHtMWrEUhDJeEY5r1vidhdetcjjgVKEpCw", "7577442370:AAEACgwryC1-YzKO8xEnNW4pMbwnOoDT-3I", "YOUR_BOT_TOKEN_9", 
    "YOUR_BOT_TOKEN_10", "YOUR_BOT_TOKEN_11", "YOUR_BOT_TOKEN_12", 
    "YOUR_BOT_TOKEN_13", "YOUR_BOT_TOKEN_14", "YOUR_BOT_TOKEN_15"
]

# Function to generate a random key
def generate_key():
    return 'golemxddos' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Function to handle /genkey command
def genkey(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        try:
            attack_count = int(context.args[0])
            key = generate_key()
            keys[key] = attack_count
            update.message.reply_text(f'Generated key: {key}')
        except (IndexError, ValueError):
            update.message.reply_text('Please specify the number of attacks, e.g., /genkey 3')

# Function to handle /redeemkey command
def redeemkey(update: Update, context: CallbackContext):
    key = context.args[0]
    if key in keys and keys[key] > 0:
        keys[key] -= 1
        users[update.message.from_user.id] = key
        update.message.reply_text(f'Key redeemed successfully. Attacks left: {keys[key]}')
    else:
        update.message.reply_text('Invalid or expired key.')

# Function to handle /checklogs command
def checklogs(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        logs = "\n".join([f'User ID: {uid}, Key: {key}' for uid, key in users.items()])
        update.message.reply_text(logs)

# Function to handle /broadcast command
def broadcast(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        message = ' '.join(context.args)
        for user_id in users.keys():
            context.bot.send_message(chat_id=user_id, text=message)

# Function to handle /attack command
def attack(update: Update, context: CallbackContext):
    # Basic validation for the attack command format
    try:
        ip = context.args[0]
        port = context.args[1]
        seconds = int(context.args[2])

        if seconds > 90:
            update.message.reply_text('Maximum attack time is 90 seconds.')
            return

        if update.message.from_user.id not in users:
            update.message.reply_text('You need to redeem a key first.')
            return

        # Extract the target username from the message's reply-to message
        if update.message.reply_to_message and update.message.reply_to_message.text:
            target_username = update.message.reply_to_message.text.strip()
        else:
            update.message.reply_text('Please reply to a user’s message with their username.')
            return

        # Display attack info and countdown
        attack_message = f'I have taken your attack\nTarget IP: {ip}\nTarget Port: {port}\nDuration: {seconds} seconds\n'
        update.message.reply_text(attack_message)
        
        # Start a countdown animation from 90 to 1 seconds
        for i in range(90, 0, -1):
            update.message.reply_text(f'Time left: {i} seconds')

        # Simulate sending the attack via the 15 bots
        for bot in bots:
            threading.Thread(target=bot.send_attack, args=(ip, port, target_username, update.message.from_user.id)).start()

    except (IndexError, ValueError):
        update.message.reply_text('Invalid command format. Use: /attack <ip> <port> <seconds>')

# Bot logic for each of the 15 bots
class Bot:
    def __init__(self, token):
        self.token = token
        self.bot = Updater(token, use_context=True)

    def send_attack(self, ip, port, target_username, user_id):
        # Send the exact attack message to the target username
        self.bot.bot.send_message(user_id, f'/attack {ip} {port} {@GOLEM_OWNER}')
        # Simulate some time before sending another message
        time.sleep(random.randint(5, 15))  # Simulate the time it takes for this bot to "attack"

    def join_channels(self):
        # Each bot joins two channels and sends /verify to the target username
        self.bot.bot.send_message(chat_id=CHANNEL_1, text='/verify')
        self.bot.bot.send_message(chat_id=CHANNEL_2, text='/verify')

    def start(self):
        self.bot.start_polling()

# Function to start 15 bots
def start_bots():
    for i in range(15):
        bot_token = BOT_TOKENS[i]  # Get the token for each bot from the list
        bot = Bot(bot_token)
        bot.join_channels()  # Make the bot join channels
        bots.append(bot)  # Append bot to the list of bots
        threading.Thread(target=bot.start).start()  # Start the bot in a separate thread

def main():
    # Initialize the main bot
    updater = Updater("7753232073:AAElmKG_cDoui0BfdhoTr9COVbdg9rg663Y", use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('genkey', genkey))
    dispatcher.add_handler(CommandHandler('redeemkey', redeemkey))
    dispatcher.add_handler(CommandHandler('checklogs', checklogs))
    dispatcher.add_handler(CommandHandler('broadcast', broadcast))
    dispatcher.add_handler(CommandHandler('attack', attack))

    # Start the main bot
    updater.start_polling()

    # Start the 15 bots
    start_bots()

if __name__ == '__main__':
    main()
