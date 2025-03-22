import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ضع التوكن الذي حصلت عليه من BotFather
TOKEN = "7985029575:AAE4Jof7GZD5BhS5AXDYj8KaSeJUUFK_S9c"
bot = telebot.TeleBot(TOKEN)

# معرف الشراكة (Affiliate ID) لكل منصة
AMAZON_AFFILIATE_ID = "your_amazon_id"
ALIEXPRESS_AFFILIATE_ID = "your_aliexpress_id"

# API لجلب عروض الألعاب
GAMES_API_URL = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15"
# API (مؤقتة) لعروض الإلكترونيات (لاحقًا يمكن استبداله بـ AliExpress/Amazon)
ELECTRONICS_API_URL = "https://dummyjson.com/products/category/smartphones"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! 🚀 هذا البوت يرسل لك أحدث العروض والتخفيضات!\nاختر نوع العروض التي تريدها:\n/games - عروض الألعاب 🎮\n/electronics - عروض الهواتف 📱")

@bot.message_handler(commands=['games'])
def send_game_deals(message):
    response = requests.get(GAMES_API_URL)
    if response.status_code == 200:
        deals = response.json()
        for deal in deals[:5]:  # إظهار 5 عروض فقط
            title = deal["title"]
            price = deal["salePrice"]
            base_link = f"https://www.cheapshark.com/redirect?dealID={deal['dealID']}"
            affiliate_link = f"{base_link}&affid={AMAZON_AFFILIATE_ID}"
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("🛒 شراء الآن", url=affiliate_link))
            
            bot.send_message(message.chat.id, f"🎮 {title}\n💰 السعر: ${price}", reply_markup=keyboard)
    else:
        bot.reply_to(message, "❌ حدث خطأ في جلب عروض الألعاب. حاول لاحقًا!")

@bot.message_handler(commands=['electronics'])
def send_electronics_deals(message):
    response = requests.get(ELECTRONICS_API_URL)
    if response.status_code == 200:
        products = response.json()["products"]
        for product in products[:5]:  # إظهار 5 عروض فقط
            title = product["title"]
            price = product["price"]
            base_link = product["thumbnail"]  # رابط تجريبي، لاحقًا نستبدله بـ AliExpress API
            affiliate_link = f"{base_link}?affid={ALIEXPRESS_AFFILIATE_ID}"
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("🛒 شراء الآن", url=affiliate_link))
            
            bot.send_message(message.chat.id, f"📱 {title}\n💰 السعر: ${price}", reply_markup=keyboard)
    else:
        bot.reply_to(message, "❌ حدث خطأ في جلب عروض الهواتف. حاول لاحقًا!")

print("✅ البوت شغال...")
bot.polling()
