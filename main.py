
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

SERVERS = {
    "de": ("🇩🇪 Германия", "ВСТАВЬ_VLESS_ССЫЛКУ_ГЕРМАНИИ"),
    "pl": ("🇵🇱 Польша", "ВСТАВЬ_VLESS_ССЫЛКУ_ПОЛЬШИ"),
    "sg": ("🇸🇬 Сингапур", "ВСТАВЬ_VLESS_ССЫЛКУ_СИНГАПУРА"),
    "nl": ("🇳🇱 Нидерланды", "ВСТАВЬ_VLESS_ССЫЛКУ_НИДЕРЛАНДОВ"),
    "gb": ("🇬🇧 Великобритания", "ВСТАВЬ_VPN_ССЫЛКУ_БРИТАНИИ"),
    "ca": ("🇨🇦 Канада", "ВСТАВЬ_VLESS_ССЫЛКУ_КАНАДЫ"),
    "se": ("🇸🇪 Швеция", "ВСТАВЬ_VLESS_ССЫЛКУ_ШВЕЦИИ"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 Получить VPN", callback_data="getvpn")],
        [InlineKeyboardButton("🌍 Полный список серверов", callback_data="servers")],
    ]
    await update.message.reply_text(
        "🇷🇺 Добро пожаловать в ПРУФ VPN!\n\nВыбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ("getvpn", "servers"):
        keyboard = [
            [InlineKeyboardButton(name, callback_data=code)]
            for code, (name, link) in SERVERS.items()
        ]
        await query.message.reply_text(
            "🌍 Выбери VPN-сервер:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if query.data in SERVERS:
        name, link = SERVERS[query.data]
        if link.startswith("ВСТАВЬ_"):
            await query.message.reply_text("Этот сервер пока не настроен.")
            return

        keyboard = [[InlineKeyboardButton("🔗 Открыть VPN", url=link)]]
        await query.message.reply_text(
            f"{name}\n\nТвоя VPN-ссылка:\n`{link}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()

