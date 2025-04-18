import os
from flask import Flask
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# === FLASK FOR KEEPALIVE ===
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot running 😎"

def run_web():
    port = int(os.environ.get('PORT', 8080))  # Use Render-assigned port or default to 8080
    app_web.run(host='0.0.0.0', port=port)

# === IMAGE PATH FUNCTIONS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ruta_imagen(nombre_archivo):
    return os.path.join(BASE_DIR, "imagenes", nombre_archivo)

# === /start HANDLER ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(ruta_imagen("inicio.jpg"), "rb") as photo:
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
        await update.message.reply_text("❌ Error: No se encontró la imagen de inicio.")

# === BUTTON HANDLER ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'servicio_a':
        text = "🔥 *Servicio VIP*\nCada Sub contiene servicio para cuatro cuentas \n1 mes $10💵\nPermanente $45💵"
        try:
            with open(ruta_imagen("1.jpg"), "rb") as photo:
                pay_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Pagar Servicio", url="https://t.me/P1sh1ng")]
                ])
                await query.message.reply_photo(
                    photo=photo,
                    caption=text,
                    parse_mode="MarkdownV2",
                    reply_markup=pay_button
                )
        except FileNotFoundError:
            await query.message.reply_text("❌ Error: No se encontró la imagen del servicio VIP.")
    elif query.data == 'servicio_b':
        text = "📢 *Entra al grupo VIP haciendo publicidad del nuestro grupo*"
        try:
            with open(ruta_imagen("Vips.jpg"), "rb") as photo:
                pay_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Mandar Referencia", url="https://t.me/P1sh1ng")]
                ])
                await query.message.reply_photo(
                    photo=photo,
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=pay_button
                )
        except FileNotFoundError:
            await query.message.reply_text("❌ Error: No se encontró la imagen del servicio Publicidad.")

# === VALIDATE IMAGES ===
imagenes = ["inicio.jpg", "1.jpg", "Vips.jpg"]
for img in imagenes:
    path = ruta_imagen(img)
    if not os.path.exists(path):
        print(f"⚠️ Imagen faltante: {path}")
    else:
        print(f"✅ Imagen cargada correctamente: {path}")

# === INITIALIZE BOT ===
app = ApplicationBuilder().token("7920704053:AAETSuHmEzTWXvC7zMhi4XuN5S60E_W2akM").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🤖 Bot running...")

# === RUN BOT AND FLASK ===
async def main():
    try:
        # Start Flask in a separate daemon thread
        threading.Thread(target=run_web, daemon=True).start()

        # Initialize and run the bot
        await app.initialize()
        await app.bot.delete_webhook(drop_pending_updates=True)
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        # Ensure proper shutdown
        await app.shutdown()

if __name__ == '__main__':
    # Run the main coroutine in a new event loop
    asyncio.run(main())
