import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, InlineQueryHandler, ContextTypes

BOT_TOKEN = "8913475001:AAE85LF0FO3glIi7tvuB2QtMq2hedvkAKfE"
WEBHOOK_URL = "https://tiktok-production-69c9.up.railway.app"

messages = {}

async def inline_query(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    
    parts = query.split(" ", 1)
    if len(parts) < 2:
        return
    
    target = parts[0].replace("@", "")
    text = parts[1]
    msg_id = str(uuid.uuid4())
    messages[msg_id] = {"text": text, "target": target}
    
    results = [
        InlineQueryResultArticle(
            id=msg_id,
            title=f"@{target} üçün gizli mesaj",
            input_message_content=InputTextMessageContent(f"🔒 @{target} üçün gizli mesaj var!"),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Mesajı aç 🔓", callback_data=f"open_{msg_id}")
            ]])
        )
    ]
    await update.inline_query.answer(results, cache_time=0)

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    msg_id = query.data.replace("open_", "")
    
    if msg_id not in messages:
        await query.answer("Mesaj tapılmadı!", show_alert=True)
        return
    
    msg = messages[msg_id]
    username = query.from_user.username or ""
    
    if username.lower() != msg["target"].lower():
        await query.answer("Bu mesaj sən üçün deyil! 🚫", show_alert=True)
        return
    
    await query.answer(msg["text"], show_alert=True)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button))

app.run_webhook(
    listen="0.0.0.0",
    port=8080,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
)
