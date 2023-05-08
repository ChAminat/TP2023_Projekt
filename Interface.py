from SystemAccount import Client, SystemAccount
from ex_info import EX_CODE_MESSAGES, ACCOUNT_NUMBER_ERROR, ZERO_OPERATION_ERROR, INCORRECT_ACCOUNT_TYPE_ERROR
from ex_banks import available_banks


class WorkingSpace:
    @staticmethod
    def show_account(my_account):  # changes
        lst = my_account.show_user_accounts()
        if not lst:
            return ("You have no accounts yet")
        ans = [f"id: {i}    type: {lst[i].ac_type}    balance: {lst[i].balance}" for i in lst.keys()]
        return '\n'.join(ans)

    @staticmethod
    def create_account(my_account, acc_type, sum=""):
        ac_type = acc_type
        if not ac_type in ["debit", "credit", "deposit"]:
            return (INCORRECT_ACCOUNT_TYPE_ERROR)
        start_sum = 0
        if ac_type == "credit":
            start_sum = float(sum)
        new_id = my_account.open_new_account(ac_type, start_sum)
        return (f"New {ac_type} account {new_id} created")

    @staticmethod
    def check_balance(my_account, id):
        try:
            ac_id = int(id)
        except Exception:
            return (ACCOUNT_NUMBER_ERROR)
        if ac_id in my_account.MyAccountList:
            return (my_account.balance(ac_id))
        return (ACCOUNT_NUMBER_ERROR)

    @staticmethod
    def stonks(my_account, type, sum, id):
        print(type)
        amount = float(sum)
        acc_id = int(id)
        if acc_id in my_account.MyAccountList:
            if amount < 0: return (ZERO_OPERATION_ERROR)
            operation = my_account.withdraw(amount, acc_id) if type == "withdraw" else my_account.top_up(amount, acc_id)
            return (operation)
        return (ACCOUNT_NUMBER_ERROR)

    @staticmethod
    def transfer(my_account, sum, acc_id, to_acc):
        print("Please, enter some information")
        amount = float(sum)
        from_acc_id = int(acc_id)
        to_acc_id = int(to_acc)
        operation = my_account.transfer(amount, from_acc_id, to_acc_id)
        return operation

    @staticmethod
    def close_account(my_account, id):
        account_id = int(id)
        if account_id in my_account.MyAccountList:
            my_account.close_account(account_id)
            return (f"Now account {account_id} is dead")
        return (ACCOUNT_NUMBER_ERROR)

    @staticmethod
    def update_my_info(my_account):  # new_func
        new_address, new_passport = WorkingSpace.get_add_user_info()
        my_account.update_my_info(new_address, new_passport)
        return True

    @staticmethod
    def show_my_info(my_account):  # new_fUnc
        dct = my_account.show_my_info()
        ans = [f"{i}: {dct[i]}" for i in dct.keys()]
        return '\n'.join(ans)

    @staticmethod
    def working_space(user_info):
        command, ex_code = user_info["operation"], ""
        while command != "exit":
            command = command
            if command == "show_account":
                ex_code = WorkingSpace.show_account(user_info["my_account"])
            elif command == "create_account":
                ex_code = WorkingSpace.create_account(my_account=user_info["my_account"],
                                                      acc_type=user_info["type"],
                                                      sum=user_info["sum"])
            elif command == "check_balance":
                ex_code = WorkingSpace.check_balance(my_account=user_info["my_account"],
                                                     id=user_info["id"])
            elif command == "withdraw":
                ex_code = WorkingSpace.stonks(my_account=user_info["my_account"],
                                              type="withdraw",
                                              sum=user_info["sum"],
                                              id=user_info["id"])
            elif command == "top_up":
                ex_code = WorkingSpace.stonks(my_account=user_info["my_account"],
                                              type="top_up",
                                              sum=user_info["sum"],
                                              id=user_info["id"]
                                              )
            elif command == "transfer":
                ex_code = WorkingSpace.transfer(my_account=user_info["my_account"],
                                                sum=user_info["sum"],
                                                acc_id=user_info["id"],
                                                to_acc=user_info["to_id"])
            elif command == "close_account":
                ex_code = WorkingSpace.close_account(my_account=user_info["my_account"],
                                                     id=user_info["id"])
            elif command == "show_my_info":  # changes
                ex_code = WorkingSpace.show_my_info(my_account=user_info["my_account"])
            return ex_code if not ex_code in EX_CODE_MESSAGES.keys() else EX_CODE_MESSAGES[ex_code]
            """show_my_infoelif command == "update_my_info":  # changes
                ex_code = WorkingSpace.update_my_info(my_account=user_info["my_account"])"""

    @staticmethod
    def get_mand_user_info(type_, user_info):
        print("Please, introduce yourself" if type_ == 0 else "Please, write your login and password")
        while True:
            name = user_info["name"] if type_ == 0 else user_info["login"]  # при авторизации запросить ввод логина
            surname = user_info["surname"] if type_ == 0 else user_info["password"]  # при авторизации запросить ввод пароля
            if name.split() and surname.split():
                return name, surname
            else:
                return "All fields must be filled in!"

    @staticmethod
    def get_add_user_info(info_user):
        print("Please, enter the following data or skip by pressing Enter")
        address = info_user["address"]
        passport = info_user["passport"]
        return address, passport

    @staticmethod
    def get_reg_bank_info(type_, user_info):
        print("What bank would you like to be " + ("registered in?" if type_ == 0 else "logged in?"))
        while True:
            bank_name = user_info["bank"]
            if not bank_name.lower() in available_banks:
                return "Sorry, this Bank is unavailable."
            else:
                return bank_name.lower()

    @staticmethod
    def registration_system(user_info):
        name, surname = WorkingSpace.get_mand_user_info(0, user_info)
        address, passport = WorkingSpace.get_add_user_info(user_info)
        client = Client(name, surname, address, passport)
        bank_name = WorkingSpace.get_reg_bank_info(0, user_info)
        login, password = WorkingSpace.get_mand_user_info(1, user_info)
        if bank_name not in available_banks.keys():
            return 1, bank_name
        my_account = SystemAccount(client, available_banks[bank_name], login, password)
        operation = available_banks[bank_name].add_new_user(login, password, my_account)
        if operation in EX_CODE_MESSAGES.keys():  # changes
            return 1, operation
        print(f"Congratulations, you are registered in {bank_name}!")
        return 0, my_account

    @staticmethod
    def login_system(user_info):
        bank_name = WorkingSpace.get_reg_bank_info(1, user_info)
        login, password = WorkingSpace.get_mand_user_info(1, user_info)
        error = 0
        if bank_name not in available_banks.keys():
            error = 1
        my_account = available_banks[bank_name].find_user(login, password)
        if my_account in EX_CODE_MESSAGES.keys():  # changes
            error = 1
        return error, my_account

    @staticmethod
    def register(user_info):
        error, my_account = WorkingSpace.registration_system(user_info)
        return error, my_account

    @staticmethod
    def log_in(user_info):
        error, my_account = WorkingSpace.login_system(user_info)
        return error, my_account
