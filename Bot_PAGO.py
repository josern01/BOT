import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'servicio_a':
        text = "🔥 *Servicio VIP*\nCada Sub contiene servicio para cuatro cuentas \n1 mes $10💵\nPermanente $45💵"
        try:
            with open("imagenes/1.jpg", "rb") as photo:
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
            await query.message.reply_text("Error: No se encontró la imagen del servicio VIP.")

    elif query.data == 'servicio_b':
        text = "*Entra al grupo VIP haciendo publicidad de nuestro grupo*"

        try:
            with open("imagenes/Vips.jpg", "rb") as photo:
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
            await query.message.reply_text("Error: No se encontró la imagen del servicio Phishing.")

TOKEN = ("7920704053:AAHbRxIcB9ipOC7eYr2FtjFmk6g0MmAXIds")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
