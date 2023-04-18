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
        print("Please, introduce yourself" if type == 0 else "Please, come up with a login and password")
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
    def get_reg_bank_info(available_banks):
        print("What bank would you like to be registered in?")
        while True:
            bank_name = input("Bank:")
            if not bank_name.lower() in available_banks:
                print("Sorry, this Bank is unavailable.")
            else:
                return bank_name.lower()      

    @staticmethod
    def run():
        available_banks = {"sber": Sber}
        while True:
            name, surname = WorkingSpace.get_mand_user_info(0)
            address, passport = WorkingSpace.get_add_user_info()
            client = Client(name, surname, address, passport)
            bank_name = WorkingSpace.get_reg_bank_info(available_banks)
            login, password = WorkingSpace.get_mand_user_info(1)
            available_banks[bank_name].add_new_user(login, password)
            my_account = SystemAccount(client, available_banks[bank_name], login, password)
            print(f"Congratulations, you are registered in {bank_name}!")
            WorkingSpace.working_space(my_account)
            break
