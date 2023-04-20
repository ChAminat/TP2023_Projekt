import telebot
from telebot import types  # кнопки
from Interface import WorkingSpace
from Banks import Sber

from SystemAccount import Client

bot = telebot.TeleBot('6002259765:AAF4bV8sh2FPOyka9NT2VYBdvxhOiQGWXiE')


class TelegramBot:
    """user_messages = {"name":"", "surname":"",
                 "address": "", "passport":"",
                 "login":"", "password":"", "bank": ""}"""
    user_messages = []
    myAccount = ""
    id = ""
    to_acc_id = ""
    sum=""

    def __init__(self, bot):
        self.bot = bot
        self.bot.polling(none_stop=True, interval=0)

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
        TelegramBot.markup(message=message, bot_message="👋 Hi!\n"
                            "Do you want to log in or register?\n",
                            user_message=["/register", "/log_in"])

        @bot.message_handler(commands=['register'])
        def register(message):
            """@bot.message_handler(func=lambda message: True)
            def echo_message(message):
                TelegramBot.user_messages.append(message.text)"""

            TelegramBot.markup(message=message,
                               bot_message="Please, introduce yourself\n"
                               "enter the following information\n",
                               user_message=[])
            TelegramBot.markup(message=message,
                               bot_message="name\n"
                               "surname\n",
                               user_message=[])
            TelegramBot.markup(message=message,
                               bot_message=
                            "Please, enter the following data(address and passport)\n"
                            " or skip (print No twice)\n"
                            "address\n"
                            "passport\n",
                               user_message=[])
            TelegramBot.markup(message=message,
                               bot_message=
                               "What bank would you like to be registered in?",
                               user_message=[])
            TelegramBot.markup(message=message,
                               bot_message=
                               "Enter login\n"
                               "password\n",
                               user_message=[])

            TelegramBot.myAccount = WorkingSpace.register(user_info=TelegramBot.user_messages)
            TelegramBot.markup(message=message,
                               bot_message=
                               f"Congratulations, you are registered in {TelegramBot.user_messages[6]}!",
                               user_message=[])

            TelegramBot.markup(message=message,
                               bot_message="What do you want to do next?\n",
                               user_message=["show_account", "create_account",
                                             "check_balance", "withdraw",
                                             "top_up", "transfer",
                                             "close_account"])

            @bot.message_handler(content_types=['text'])
            def get_text_messages(message):

                if message.text == "show_account":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                                my_account=TelegramBot.myAccount,
                                                command=message.text),
                                       user_message=[])

                elif message.text == "create_account":
                    TelegramBot.markup(message=message,
                                       bot_message="Select the account type: debit, credit, deposit",
                                       user_message=["debit", "credit", "deposit"])


                elif message.text == "debit":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command="create_account",
                                           type=message.text),
                                       user_message=[])
                elif message.text == "deposit":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command="create_account",
                                           type=message.text),
                                       user_message=[])

                elif message.text == "credit":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command="create_account",
                                           type=message.text,
                                           sum=""),#добавить для кредитного счета сумму
                                       user_message=[])

                elif message.text == "check_balance":#дописать запрос id
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command=message.text,
                                           account_id=TelegramBot.id),
                                       user_message=[])

                elif message.text[:3] == "id ":  # input id account
                    TelegramBot.id = message.text[3:]

                elif message.text[:8] == "to_acc ":
                    TelegramBot.to_acc_id = message.text[8:]

                elif message.text[:4] == "sum ":  # input id account
                    TelegramBot.id = message.text[4:]

                elif message.text == "withdraw":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command=message.text,
                                           type=message.text,
                                           account_id=TelegramBot.id,
                                           sum=TelegramBot.sum),
                                       user_message=[])

                elif message.text == "top_up ":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command=message.text,
                                           type=message.text,
                                           account_id=TelegramBot.id,
                                           sum=TelegramBot.sum),
                                       user_message=[])

                elif message.text[:10] == "transfer ":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command=message.text,
                                           type=message.text,
                                           account_id=TelegramBot.id,
                                           to_account_id=TelegramBot.to_acc_id,
                                           sum=TelegramBot.sum),
                                       user_message=[])

                elif message.text == "close_account":
                    TelegramBot.markup(message=message,
                                       bot_message=WorkingSpace.working_space(
                                           my_account=TelegramBot.myAccount,
                                           command=message.text,
                                           account_id=TelegramBot.id),
                                       user_message=[])
                else:
                    TelegramBot.user_messages.append(message.text)


        @bot.message_handler(commands=['log_in']) #доработать
        def log_in(message):
            TelegramBot.markup(message=message,
                               bot_message="",
                               user_message=[])
