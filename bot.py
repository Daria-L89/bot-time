from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import re

TOKEN = os.environ["TOKEN"]

def parse_minutes(t):
    h, m = map(int, t.split("-"))
    return h * 60 + m

def calculate(text):
    total = 0
    for line in text.split("\n"):
        times = re.findall(r"\d{1,2}-\d{2}", line)
        if len(times) >= 2:
            start = parse_minutes(times[0])
            end = parse_minutes(times[1])
            total += end - start
    return total

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    total = calculate(text)

    h = total // 60
    m = total % 60

    await update.message.reply_text(f"📊 Итого: {h}ч {m}м")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
