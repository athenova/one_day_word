import os
import telebot
import json
import requests
import glob

from datetime import date
from datetime import timedelta
from openai import OpenAI
from PIL import Image

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = -1002374309134
AI_TEXT_MODEL = 'chatgpt-4o-latest'
AI_IMAGE_MODEL = 'dall-e-3'

check_date = date.today() + timedelta(days=1)

tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))

for i, task in enumerate(tasks):
    if task["date"] == check_date.strftime('%Y-%m-%d'):
        folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}")
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        folder_name = glob.escape(f"{folder_name}/{task['name'].replace('/', ',')}")
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        text_file_name = f"{folder_name}/text.txt"

        client = OpenAI()
        if not os.path.exists(text_file_name):
            text_prompt = task["text_prompt"]
            text = client.chat.completions.create(
                        model=AI_TEXT_MODEL,
                        messages=[
                            { "role": "system", "content": f"Ты - блогер с 1000000 миллионном подписчиков" },
                            { "role": "user", "content": text_prompt },
                        ]
                    ).choices[0].message.content
            open(text_file_name, 'wt', encoding="UTF-8").write(text)

        bot = telebot.TeleBot(BOT_TOKEN)

        if os.path.exists(text_file_name):
            bot.send_message(chat_id=CHAT_ID, text=open(text_file_name, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")