import telebot

TOKEN = "8498865676:AAHvFOqY9ZPL-yR3UlqoMrrZaAWZIsv2Qgs"
bot = telebot.TeleBot(TOKEN)

# 🧠 Memory storage (per user)
user_memory = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 Hello! I am your smart bot.\n\n"
        "You can:\n"
        "• Say hi\n"
        "• Tell me your name\n"
        "• Chat with me normally 🙂"
    )

@bot.message_handler(func=lambda message: True)
def smart_reply(message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Initialize memory
    if user_id not in user_memory:
        user_memory[user_id] = {}

    # 🟢 Greeting logic
    if text in ["hi", "hello", "hey"]:
        bot.reply_to(message, "👋 Hi my friend! How are you?")
        return

    # 🟢 Name memory logic
    if "my name is" in text:
        name = text.replace("my name is", "").strip().title()
        user_memory[user_id]["name"] = name
        bot.reply_to(message, f"Nice to meet you, {name} 😊")
        return

    # 🟢 If bot remembers name
    if "name" in user_memory[user_id]:
        name = user_memory[user_id]["name"]
        bot.reply_to(message, f"{name}, you said: {message.text}")
    else:
        bot.reply_to(message, f"You said: {message.text}")

print("🤖 Smart Telegram bot is running...")
bot.infinity_polling()
