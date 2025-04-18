import os
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "7920704053:AAHbRxIcB9ipOC7eYr2FtjFmk6g0MmAXIds"
BOT_URL = "https://bot-vq8s.onrender.com"

# Inicializamos la app de Flask
flask_app = Flask(__name__)

# Creamos el bot pero lo inicializamos más abajo
app_bot = ApplicationBuilder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("imagenes/inicio.jpg", "rb") as photo:
            keyboard = [
                [InlineKeyboardButton("Servicio VIP", callback_data='servicio_a')],
                [InlineKeyboardButton("Por publicidad", callback_data='servicio_b')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_photo(
                photo=photo,
                caption='Selecciona un servicio:',
                reply_markup=reply_markup
            )
    except FileNotFoundError:
        await update.message.reply_text("Error: No se encontró la imagen de inicio.")

# Botones
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'servicio_a':
        text = "🔥 *Servicio VIP*\nCada Sub contiene servicio para cuatro cuentas \n1 mes $10💵\nPermanente $45💵"
        try:
            with open("imagenes/1.jpg", "rb") as photo:
                pay_button = InlineKeyboardMarkup([[
                    InlineKeyboardButton("💳 Pagar Servicio", url="https://t.me/P1sh1ng")
                ]])
                await query.message.reply_photo(
                    photo=photo,
                    caption=text,
                    parse_mode="MarkdownV2",
                    reply_markup=pay_button
                )
        except FileNotFoundError:
            await query.message.reply_text("Error: No se encontró la imagen del servicio VIP.")

    elif query.data == 'servicio_b':
        text = "*Entra al grupo VIP haciendo publicidad de nuestro grupo*"
        try:
            with open("imagenes/Vips.jpg", "rb") as photo:
                pay_button = InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Mandar Referencia", url="https://t.me/P1sh1ng")
                ]])
                await query.message.reply_photo(
                    photo=photo,
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=pay_button
                )
        except FileNotFoundError:
            await query.message.reply_text("Error: No se encontró la imagen del servicio Phishing.")

# Agregamos los handlers
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CallbackQueryHandler(button))

# Ruta principal
@flask_app.route("/")
def index():
    return "Bot activo y en línea 🔥", 200

# Ruta para recibir updates desde Telegram
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot.bot)

    import asyncio
    asyncio.run(process_update_async(update))

    return "OK", 200

# Inicializa el bot manualmente
async def process_update_async(update):
    if not app_bot.running:
        await app_bot.initialize()
        await app_bot.start()
    await app_bot.process_update(update)

# Ruta opcional para registrar el webhook desde el navegador
@flask_app.route("/setwebhook")
def set_webhook():
    bot = Bot(TOKEN)
    bot.set_webhook(f"{BOT_URL}/{TOKEN}")
    return "✅ Webhook registrado correctamente"

# Ejecutamos todo
if __name__ == "__main__":
    import asyncio

    async def setup():
        print("🔧 Configurando webhook e iniciando bot...")
        await app_bot.initialize()
        await app_bot.start()
        await app_bot.bot.set_webhook(url=f"{BOT_URL}/{TOKEN}")

    asyncio.run(setup())
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
