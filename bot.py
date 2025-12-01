from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

# Majburiy kanallar
REQUIRED_CHANNELS = [
    "t.me/soqqanibosamzz",
    "t.me/signalprogramma",
    "t.me/orginalkontoralar"
]

# /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "⚠️ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:\n\n"
    for i, ch in enumerate(REQUIRED_CHANNELS, start=1):
        text += f"{i}-kanal: {ch}\n"

    # Inline tugma
    keyboard = [[InlineKeyboardButton("✅ Tekshirish", callback_data="check")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)

# Inline tugma bosilganda tekshirish
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    not_subscribed = []
    for i, channel in enumerate(REQUIRED_CHANNELS, start=1):
        try:
            member = await context.bot.get_chat_member(channel.replace("t.me/", "@"), user_id)
            if member.status in ["left", "kicked"]:
                not_subscribed.append(f"{i}-kanal: {channel}")
        except BadRequest:
            not_subscribed.append(f"{i}-kanal: {channel}")

    if not_subscribed:
        text = "⚠️ Siz quyidagi kanallarga obuna bo‘lmadingiz:\n\n"
        text += "\n".join(not_subscribed)
        text += "\n\nObuna bo‘lgach, /start ni qayta bosing."
        await query.message.reply_text(text)
    else:
        await query.message.reply_text("🎉 Xush kelibsiz! Siz barcha kanallarga obuna bo‘lgansiz.")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token("8412177416:AAEUmfElBemGtwrJZvSqdDq28ZdHITk1WzI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="check"))

    print("Bot ishga tushdi...")
    app.run_polling()
