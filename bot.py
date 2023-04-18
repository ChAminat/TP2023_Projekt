import telebot
from telebot import types #кнопки
from Interface import WorkingSpace
from Banks import Sber
from SystemAccount import Client

bot = telebot.TeleBot('6002259765:AAF4bV8sh2FPOyka9NT2VYBdvxhOiQGWXiE')

class TelegramBot:

    name = None
    surname = None
    address = None
    passport = None
    client = None
    bank = None
    available_banks = {"sber": Sber}
    myAccount = None

    def __init__(self, bot):
        self.bot = bot
        bot.polling(none_stop=True, interval=0)
    @staticmethod
    def markup(message, bot_message, user_message=""):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if user_message:
            for i in user_message:
                btn = types.KeyboardButton(i)
                markup.add(btn)
        bot.send_message(message.from_user.id, bot_message, reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def start(message):
        TelegramBot.markup(message, "👋 Hi! Choose the right team", ["/registration", "/authorization"])

    @bot.message_handler(commands=['registration'])
    def registration(message):
        TelegramBot.markup(message, "Please, introduce yourself: \n", [])

    @bot.message_handler(commands=['optional'])
    def optional(message):
        TelegramBot.markup(message, "Choose the right team: \n",
                           ["show_account", "create_account",
                            "check_balance",
                            "withdraw", "top_up",
                            "transfer", "close_account"])

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        if message.text == 'authorization':
             pass

        if message.text[:5] == "name ":
            TelegramBot.name = message.text[5:]

        if message.text[:8] == "surname ":
            TelegramBot.surname = message.text[8:]

        if message.text[:8] == "address ":
            TelegramBot.address = message.text[8:]

        if message.text[:9] == "passport ":
            TelegramBot.passport = message.text[9:]
            TelegramBot.markup(message, "What bank would you like to be registered in?")

        if message.text[:5] == "bank ":
            TelegramBot.bank = WorkingSpace.get_reg_bank_info(TelegramBot.available_banks, message.text[5:])
            TelegramBot.myAccount = WorkingSpace.runRegestration(TelegramBot.client, TelegramBot.bank)
            TelegramBot.markup(message, f"Congratulations, you are registered in {message.text[5:]}!", [])
            TelegramBot.markup(message, "What do you want to do next? /optional", [])

        if message.text == "show_account":
             pass

        if message.text == "create_account":
            #credit with start sum
            TelegramBot.markup(message, "Select the account type: debit, credit, deposit",
                               ["debit", "credit", "deposit"])
            TelegramBot.markup(message, "Enter start size of credit", [])

        if (message.text == "debit" or message.text == "deposit"):
            prin = WorkingSpace.optionalBank(my_account=TelegramBot.myAccount,
                                          command=message.text)
            TelegramBot.markup(message, f"New {message.text} account {prin} created", [])

        if message.text[:7] == "credit ":
            WorkingSpace.optionalBank(my_account=TelegramBot.myAcoount,
                                      command=message.text[:6],
                                      ans=message.text[6:])
            TelegramBot.markup(message, f"New {message.text} account {prin} created", [])

        if message.text == "check_balance":
            TelegramBot.markup(message, "input Your account number", [])

        if message.text[:8] == "account ": #input id account
            prin = WorkingSpace.optionalBank(my_account=TelegramBot.myAcoount,
                                      command=message.text, ans=message.text[8:])
            if prin != "error":
                TelegramBot.markup(message, f"your account {message.text[8:]} balance {prin}", [])
            else:
                TelegramBot.markup(message, "unavailable account number", [])

        if message.text == "top_up":
            pass

        if message.text == "transfer":
            pass

        if message.text == "close_account":
            pass

        if message.text == "withdraw":
            pass


