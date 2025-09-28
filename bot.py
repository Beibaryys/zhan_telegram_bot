from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = (
    "8234909588:AAGkeYWIYMKdCNKOCG5x_uSOVjknqdO0l7I"  # вставь свой токен от BotFather
)


# Проверка: админ или нет
async def is_admin(update: Update) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    member = await chat.get_member(user.id)
    return member.status in ["administrator", "creator"]


# Закрыть чат
async def close_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text(
            "🚫 Только админы могут использовать эту команду."
        )
    await update.effective_chat.set_permissions(
        ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text("🔒 Чат закрыт. Писать могут только админы.")


# Открыть чат
async def open_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text(
            "🚫 Только админы могут использовать эту команду."
        )
    await update.effective_chat.set_permissions(ChatPermissions(can_send_messages=True))
    await update.message.reply_text("🔓 Чат открыт. Все участники могут писать.")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("close", close_chat))
    app.add_handler(CommandHandler("open", open_chat))
    print("✅ Бот запущен...")
    app.run_polling()


main()
