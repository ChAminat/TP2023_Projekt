from SystemAccount import Client, SystemAccount
from Banks import Sber
from ex_info import ex_code_dct


class WorkingSpace:
    @staticmethod
    def show_account(my_account):
        lst = my_account.MyAccountList
        if not lst:
            return("You have no accounts yet")
        ans = [f"id: {i}    type: {lst[i].ac_type}    balance: {lst[i].balance}" for i in lst]
        return '\n'.join(ans)
        
    @staticmethod
    def create_account(my_account):
        ac_type = input("Select the account type: debit, credit, deposit").lower()
        if not ac_type in ["debit", "credit", "deposit"]:
            return(113)
        start_sum = 0
        if ac_type == "credit":
            start_sum = float(input("Enter start size of credit"))
        new_id = my_account.open_new_account(ac_type, start_sum)
        return(f"New {ac_type} account {new_id} created")

    @staticmethod
    def check_balance(my_account):
        try:
            ac_id = int(input("Your account number: "))
        except Exception:
            return(111)
        if ac_id in my_account.MyAccountList:
            return(my_account.balance(ac_id))
        return(111)
    
    @staticmethod
    def stonks(my_account, type):
        amount = float(input("enter the amount of money: "))
        acc_id = int(input("enter the account id: "))
        if acc_id in my_account.MyAccountList:
            if amount < 0: return(112)
            operation = my_account.withdraw(amount, acc_id) if type == "withdraw" else my_account.top_up(amount, acc_id)
            return(operation)
        return(111)
    
    @staticmethod
    def transfer(my_account):
        print("Please, enter some information")
        amount = float(input("amount of money:"))
        from_acc_id = int(input("from what account (id):"))
        to_acc_id = int(input("to what account (id):"))
        operation = my_account.transfer(amount, from_acc_id, to_acc_id)
        return operation

    @staticmethod
    def close_account(my_account):
        account_id = int(input("Enter the id of an account to close"))
        if account_id in my_account.MyAccountList:
            my_account.close_account(account_id)
            return(f"Now account {account_id} is dead")
        return(111)        

    @staticmethod
    def working_space(my_account):
        command, ex_code = "", ""
        while command != "exit":
            command = input("What do you want to do next?")
            if command == "show_account":
                ex_code = WorkingSpace.show_account(my_account)
            elif command == "create_account":
                ex_code = WorkingSpace.create_account(my_account)
            elif command == "check_balance":
                ex_code = WorkingSpace.check_balance(my_account)
            elif command == "withdraw":
                ex_code = WorkingSpace.stonks(my_account, "withdraw")
            elif command == "top_up":
                ex_code = WorkingSpace.stonks(my_account, "top_up")
            elif command == "transfer":
                ex_code = WorkingSpace.transfer(my_account)
            elif command == "close_account":
                ex_code = WorkingSpace.close_account(my_account)
            print(ex_code if not ex_code in ex_code_dct.keys() else ex_code_dct[ex_code])

    @staticmethod
    def get_mand_user_info(type):
        print("Please, introduce yourself" if type == 0 else "Please, write your login and password")
        while True:
            name = input("name:" if type == 0 else "login:")
            surname = input("surname:" if type == 0 else "password:")
            if name.split() and surname.split():
                return name, surname
            else:
                print("All fields must be filled in!")

    @staticmethod
    def get_add_user_info():
        print("Please, enter the following data or skip by pressing Enter")
        address = input("address:")
        passport = input("passport:")
        return address, passport
    
    @staticmethod
    def get_reg_bank_info(available_banks, type):
        print("What bank would you like to be " + ("registered in?" if type == 0 else "logged in?"))
        while True:
            bank_name = input("Bank:")
            if not bank_name.lower() in available_banks:
                print("Sorry, this Bank is unavailable.")
            else:
                return bank_name.lower() 

    @staticmethod
    def registration_system(available_banks):
        name, surname = WorkingSpace.get_mand_user_info(0)
        address, passport = WorkingSpace.get_add_user_info()
        client = Client(name, surname, address, passport)
        bank_name = WorkingSpace.get_reg_bank_info(available_banks, 0)
        login, password = WorkingSpace.get_mand_user_info(1)
        my_account = SystemAccount(client, available_banks[bank_name], login, password)
        available_banks[bank_name].add_new_user(login, password, my_account)
        print(f"Congratulations, you are registered in {bank_name}!")
        return my_account

    @staticmethod
    def login_system(available_banks):
        bank_name = WorkingSpace.get_reg_bank_info(available_banks, 1)
        login, password = WorkingSpace.get_mand_user_info(1)
        my_account = available_banks[bank_name].find_user(login, password)
        return my_account


    @staticmethod
    def run():
        available_banks = {"sber": Sber}
        while True:
            print("Do you want to log in or register?")
            ans = input("Write 'log_in' or 'register': ")
            if ans == "log_in":
                my_account = WorkingSpace.login_system(available_banks)
                if my_account in ex_code_dct.keys():
                    print(ex_code_dct[my_account])
                    continue
                else:
                    print("You have successfully logged in!")
                    WorkingSpace.working_space(my_account)
            elif ans == "register":
                my_account = WorkingSpace.registration_system(available_banks)
                WorkingSpace.working_space(my_account)
            else:
                print("Unavailable command")
