import os
import re

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ["TOKEN"]

def parse_minutes(t):
    h, m = map(int, t.split("-"))
    return h * 60 + m

def calculate(text):
    projects = {}

    for line in text.split("\n"):
        times = re.findall(r"\d{1,2}-\d{2}", line)

        if len(times) >= 2:
            start = parse_minutes(times[0])
            end = parse_minutes(times[1])
            duration = end - start

            # Берем первое слово после времени
            parts = line.split()

            if len(parts) >= 3:
                project = parts[2]
            else:
                project = "Інше"

            projects[project] = projects.get(project, 0) + duration

    return projects

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    projects = calculate(text)

message = "📊 Звіт\n\n"

total = 0

for project, minutes in projects.items():
    h = minutes // 60
    m = minutes % 60

    message += f"📁 {project}: {h}ч {m}хв\n"

    total += minutes

message += "\n──────────────\n"

message += f"🕒 Всього: {total // 60}ч {total % 60}хв"

await update.message.reply_text(message)

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
