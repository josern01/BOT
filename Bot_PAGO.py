import os
from flask import Flask
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import asyncio

# === FLASK PARA KEEP ALIVE ===
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot corriendo 😎"

def run_web():
    app_web.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

threading.Thread(target=run_web).start()

# === FUNCIONES DE RUTA DE IMAGEN ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ruta_imagen(nombre_archivo):
    return os.path.join(BASE_DIR, "imagenes", nombre_archivo)

# === HANDLER /start ===
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

# === HANDLER BOTONES ===
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

# === VALIDAR IMÁGENES ===
imagenes = ["inicio.jpg", "1.jpg", "Vips.jpg"]
for img in imagenes:
    path = ruta_imagen(img)
    if not os.path.exists(path):
        print(f"⚠️ Imagen faltante: {path}")
    else:
        print(f"✅ Imagen cargada correctamente: {path}")

# === INICIALIZAR BOT ===
app = ApplicationBuilder().token("7920704053:AAETSuHmEzTWXvC7zMhi4XuN5S60E_W2akM").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🤖 Bot corriendo...")

# === EJECUTAR POLLING SIN CERRAR EL EVENT LOOP ===
async def run_bot():
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.run_polling()

# Usamos create_task para integrarlo al loop que ya corre
asyncio.get_event_loop().create_task(run_bot())
