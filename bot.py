# bot.py
import os
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен берём из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "❌ Ошибка: BOT_TOKEN не найден. Задай переменную окружения BOT_TOKEN."
    )


# Проверка: админ или нет
async def is_admin(update: Update) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    member = await chat.get_member(user.id)
    return member.status in ["administrator", "creator"]


# Команда закрыть чат
async def close_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text(
            "🚫 Только админы могут использовать эту команду."
        )

    try:
        await update.effective_chat.set_permissions(
            ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(
            f"🔒 Чат закрыт админом {update.effective_user.mention_html()}.",
            parse_mode="HTML",
        )
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Ошибка: у меня нет прав для изменения настроек чата.\n{e}"
        )


# Команда открыть чат
async def open_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text(
            "🚫 Только админы могут использовать эту команду."
        )

    try:
        await update.effective_chat.set_permissions(
            ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text(
            f"🔓 Чат открыт админом {update.effective_user.mention_html()}.",
            parse_mode="HTML",
        )
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Ошибка: у меня нет прав для изменения настроек чата.\n{e}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("close", close_chat))
    app.add_handler(CommandHandler("open", open_chat))

    print("✅ Бот запущен...")
    app.run_polling()  # <- без asyncio.run()


if __name__ == "__main__":
    main()
