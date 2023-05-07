import telebot
from telebot import types  # кнопки
from Interface import WorkingSpace
from my_token import TOKEN_BOT

bot = telebot.TeleBot(TOKEN_BOT)

user_ans = {"name": "", "surname": "", "address": "",
            "passport": "", "bank": "", "login": "",
            "password": "", "operation": "", "type": "",
            "id": "", "to_id": "", "sum": "", "my_account": None}

class TelegramBot:

    def __init__(self, bot=bot):
        self.bot = bot
        self.bot.polling(none_stop=True, interval=3)

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
        bot.send_message(chat_id=message.chat.id,
                         text="👋 Hi!\n"
                            "Follow the instructions further.\n"
                            "Please do not flood the chat and\n"
                            "write answers clearly and each time with a new message!\n"
                            "So, let's begin...\n"
                            "Do you want to /log_in or /register?\n")

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(chat_id=message.chat.id,
                         text="At the start, you select two commands /register if you are not registered in the system or /log_in if you are registered in any bank.\n"
                    "In the first case, you need to further enter information about yourself by clicking the command\n"
                    "/change_information_user - enter the following 4 messages separated by a space (or if you are already registered, but want to add information or change it):\n"
                    "first name: your first name\n"
                    "last name: your last name\n"
                    "address: your address\n"
                    "passport: your passport number\n"
                    "/choice_bank - select bank from the available (enter its name) for example:\n"
                    "bank: bank name\n"
                    "/username - enter the following 2 messages separated by a space to register in the system or log in (after the command /log_in):\n"
                    "login: your login\n"
                    "password: your password\n"
                    "In the second case, to log in, select which bank you are registered with\n"
                    "and enter your username and password\n")

    @bot.message_handler(commands=['register'])
    def register(message):
        user_ans["operation"] = "register"
        bot.send_message(chat_id=message.chat.id,
                         text="Use the following commands in turn (you can read more about them in /help):\n"
                              "/change_information_user\n"
                              "/choice_bank\n"
                              "/username\n")

    @bot.message_handler(commands=['log_in'])  # доработать
    def log_in(message):
        user_ans["operation"] = "log_in"
        bot.send_message(chat_id=message.chat.id,
                         text="Use the following commands in turn (you can read more about them in /help):\n"
                              "/choice_bank\n"
                              "/username\n")

    @bot.message_handler(commands=['change_information_user'])
    def change_info(message):
        bot.send_message(chat_id=message.chat.id,
                         text="Please, introduce yourself\n"
                              "Enter the following data(address and passport)\n"
                              "or skip (print No twice)\n")

    @bot.message_handler(commands=['choice_bank'])
    def choice_bank(message):
        bot.send_message(chat_id=message.chat.id,
                         text="What bank would you like to be registered in?")

    @bot.message_handler(commands=['username'])
    def enter_username(message):
        bot.send_message(chat_id=message.chat.id,
                         text="Perfectly!"
                              "To log in, enter your username and password")

    @bot.message_handler(commands=['show_account'])
    def show_acc(message):
        user_ans["operation"] = "show_account"
        bot.send_message(chat_id=message.chat.id,
                         text=WorkingSpace.working_space(user_info=user_ans))

    @bot.message_handler(commands=['create_credit_account'])
    def create_credit_account(message):
        user_ans["operation"] = "create_account"
        user_ans["type"] = "credit"
        bot.send_message(chat_id=message.chat.id,
                         text="Enter sum: <sum>  for create credit account")

    @bot.message_handler(commands=['create_debit_account'])
    def create_debit_account(message):
        user_ans["operation"] = "create_account"
        user_ans["type"] = "debit"
        bot.send_message(chat_id=message.chat.id,
                         text=WorkingSpace.working_space(user_info=user_ans))

    @bot.message_handler(commands=['create_deposit_account'])
    def create_deposit_account(message):
        user_ans["operation"] = "create_account"
        user_ans["type"] = "deposit"
        bot.send_message(chat_id=message.chat.id,
                         text=WorkingSpace.working_space(user_info=user_ans))

    @ bot.message_handler(commands=['check_balance'])
    def check_balance(message):
        user_ans["operation"] = "check_balance"
        bot.send_message(chat_id=message.chat.id,
                         text="Enter id: <id_your_account>")

    @bot.message_handler(commands=['withdraw', 'top_up', 'transfer'])
    def withdraw(message):
        user_ans["operation"] = "withdraw"
        bot.send_message(chat_id=message.chat.id,
                         text="Enter sum: <sum>\n")

    @bot.message_handler(commands=['close_account'])
    def close_account(message):
        user_ans["operation"] = "close_account"
        bot.send_message(chat_id=message.chat.id,
                         text="Enter id: <id>\n")

    @bot.message_handler(commands=["show_my_info"])
    def show_my_info(message):
        user_ans["operation"] = "show_my_info"
        bot.send_message(chat_id=message.chat.id,
                         text=WorkingSpace.working_space(user_info=user_ans))

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text[:6] == "name: ":
            user_ans["name"] = message.text[6:]
        elif message.text[:9] == "surname: ":
            user_ans["surname"] = message.text[9:]
        elif message.text[:9] == "address: ":
            if message.text[9:] != "No":
                user_ans["address"] = message.text[9:]
            else:
                user_ans["address"] = ""
        elif message.text[:10] == "passport: ":
            if message.text[10:] != "No":
                user_ans["passport"] = message.text[10:]
            else:
                user_ans["passport"] = ""
        elif message.text[:6] == "bank: ":
            user_ans["bank"] = message.text[6:].lower()
        elif message.text[:7] == "login: ":
            user_ans["login"] = message.text[7:]
        elif message.text[:10] == "password: ":
            user_ans["password"] = message.text[10:]
            error = 0
            if user_ans['operation'] == "register":
                error, user_ans["my_account"] = WorkingSpace.register(user_info=user_ans)
            elif user_ans['operation'] == "log_in":
                error, user_ans["my_account"] = WorkingSpace.log_in(user_info=user_ans)
            if error:
                bot.send_message(chat_id=message.chat.id,
                                 text=f"Error: {user_ans['my_account']}\n"
                                      "Go back and repeat the steps again")
            else:
                TelegramBot.markup(message=message,
                                   bot_message="Select the following buttons on the keyboard \n"
                                               "(read the description in /help)",
                                   user_message=["/show_account", "/create_debit_account",
                                                 "/create_deposit_account", "/create_credit_account",
                                                 "/check_balance", "/withdraw", "/top_up", "/transfer",
                                                 "/close_account", "/show_my_info"])
        elif message.text[:5] == "sum: ":
            user_ans["sum"] = message.text[5:]
            if user_ans["operation"] == "create_account":
                bot.send_message(chat_id=message.chat.id,
                                 text=WorkingSpace.working_space(user_info=user_ans))
            elif user_ans["operation"] == "withdraw" or "top_up" or "transfer":
                bot.send_message(chat_id=message.chat.id,
                                 text="Enter id: <id_your_account>\n")

        elif message.text[:4] == "id: ":
            user_ans["id"] = message.text[4:]
            if user_ans["operation"] == "check_balance":
                bot.send_message(chat_id=message.chat.id,
                                 text=WorkingSpace.working_space(user_info=user_ans))
            elif user_ans["operation"] == "withdraw" or "top_up":
                bot.send_message(chat_id=message.chat.id,
                                 text=WorkingSpace.working_space(user_info=user_ans))
            elif user_ans["operation"] == "transfer":
                bot.send_message(chat_id=message.chat.id,
                                 text="Enter to_acc: <to_acc>")
            elif user_ans["operation"] == "close_account":
                bot.send_message(chat_id=message.chat.id,
                                 text=WorkingSpace.working_space(user_info=user_ans))
        elif message.text[:7] == "to_id: ":
            user_ans["to_id"] = message.text[7:]
            bot.send_message(chat_id=message.chat.id,
                             text=WorkingSpace.working_space(user_info=user_ans))

