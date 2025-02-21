import os
import telebot
import json
import glob

from datetime import date

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = '@one_day_word'
#CHAT_ID = -1002374309134

check_date = date.today()

tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))

for i, task in enumerate(tasks):
    if task["date"] == check_date.strftime('%Y-%m-%d'):
        folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}/{task['name'].replace('/', ',')}")
        text_file_name = f"{folder_name}/text.txt"

        bot = telebot.TeleBot(BOT_TOKEN)
        if os.path.exists(text_file_name):
            bot.send_message(chat_id=CHAT_ID, text=open(text_file_name, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")
