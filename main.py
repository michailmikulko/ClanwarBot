from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

targets = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для Clash of Clans КВ. Используй /занять <номер>")

async def occupy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if not context.args:
        await update.message.reply_text("Укажи номер цели: /занять 5")
        return

    target = context.args[0]
    if target in targets:
        await update.message.reply_text(f"Цель {target} уже занята {targets[target]}")
    else:
        targets[target] = user
        await update.message.reply_text(f"{user} занял цель {target}")

async def release(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if not context.args:
        await update.message.reply_text("Укажи номер цели: /освободить 5")
        return

    target = context.args[0]
    if target in targets and targets[target] == user:
        del targets[target]
        await update.message.reply_text(f"{user} освободил цель {target}")
    else:
        await update.message.reply_text(f"Цель {target} не занята тобой.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not targets:
        await update.message.reply_text("Все цели свободны.")
    else:
        reply = "Занятые цели:
"
        for k, v in targets.items():
            reply += f"Цель {k}: {v}\n"
        await update.message.reply_text(reply)

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("занять", occupy))
    app.add_handler(CommandHandler("освободить", release))
    app.add_handler(CommandHandler("статус", status))
    app.run_polling()
