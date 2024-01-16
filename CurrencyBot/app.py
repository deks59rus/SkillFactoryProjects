import telebot, pickle, extentions
from config import token, currencies
from background import keep_alive


bot = telebot.TeleBot(token)
try:
    with open('currencies_dictionary.pkl', 'rb') as f:
        currencies = pickle.load(f)
except:
    currencies = currencies


@bot.message_handler(commands=['start', 'help'])
def get_info(message: telebot.types.Message):
    info = "Данный бот переводит валюты по курсу взятому с currencyapi.com\n" \
           "Для данного бота используется бесплатная версия API. Поэтому, актуальность данных составляет" \
           " - сутки. Т.Е. Цена конвертации берется прошлым числом.\n Чтобы начать работу, напишите сообщение боту в виде:\n *<имя валюты, цену которой ты хочешь узнать>*,\n" \
           " *<имя валюты, в которой надо узнать цену первой валюты>*,\n *<количество первой валюты>*. \n(Обратите внимание: писать нужно через запятую)\n" \
           "Также вы можете ввести команду /values, чтобы узнать о всех доступных валютах. При конвертации придерживайтесь названий валют в /values"
    bot.reply_to(message, info, parse_mode='MARKDOWN')


@bot.message_handler(commands=["values"])
def get_values(message: telebot.types.Message):
    currencies_info ="Валюты доступные для конвертации: "
    for currency in currencies.keys():
        currencies_info = "\n".join((currencies_info, currency))
    bot.reply_to(message, currencies_info)

@bot.message_handler(content_types=["text"])
def user_input(message: telebot.types.Message):
    try:
        user_input = message.text.lower().split(",")
        quote, base, amount = user_input[0], user_input[1], user_input[2]
        quote, base, amount = quote.strip(), base.strip(), amount.strip()
        if len(user_input) != 3:
            raise (extentions.APIException("Некорректное число параметров!"))
        if (quote not in currencies) or (base not in currencies):
            raise (extentions.APIException("Такой валюты не существует/ некоректное наименование валюты!"))

        result = extentions.Request_To_API.get_price(currencies[quote], currencies[base], amount)
        answer = f" {amount} {quote} стоят {result} {base}"
    except extentions.APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        bot.send_message(message.chat.id, answer)
keep_alive()
bot.polling(none_stop=True)



