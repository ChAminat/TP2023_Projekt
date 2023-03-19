from imports import *


def working_space(my_account):
    command = ""
    while command != "exit":
        command = input("What do you what to do next?")
        if command == "show_account":
            lst = my_account.MuAccountList
            if not lst:
                print("You have no accounts yet")
            for i in lst:
                print(f"id: {i}    type: {lst[i].ac_type}    balance: {lst[i].balance}")
        elif command == "create_account":
            ac_type = input("Select the account type: debit, credit, deposit").lower()
            start_sum = 0
            if ac_type == "credit":
                start_sum = float(input("Enter start size of credit"))
            new_id = my_account.open_new_account(ac_type, start_sum)
            print(f"New {ac_type} account {new_id} created")
        elif command == "check_balance":
            ac_id = int(input("Your account number: "))
            if ac_id in my_account.MuAccountList:
                print(my_account.balance(ac_id))
            else:
                print("Sorry, an unavailable account number")
        elif command == "withdraw":
            amount = float(input("enter the amount of money: "))
            acc_id = int(input("enter the account id: "))

            if acc_id in my_account.MuAccountList:
                if amount < 0:
                    print(f"amount should be upper than 0")
                    continue
                my_account.withdraw(amount, acc_id)
                print(f"OK")
            else:
                print("Sorry, an unavailable account number")
        elif command == "top_up":
            amount = float(input("enter the amount of money: "))
            acc_id = int(input("enter the account id: "))

            if acc_id in my_account.MuAccountList:
                if amount < 0:
                    print(f"amount should be upper than 0")
                    continue
                my_account.top_up(amount, acc_id)
                print(f"Wow, you have money? ")
            else:
                print("Sorry, an unavailable account number")
        elif command == "transfer":
            print("Please, enter some information")
            while True:  # тут будет проверка на корректность ввода
                amount = float(input("amount of money:"))
                from_acc_id = int(input("from what account (id):"))
                to_acc_id = int(input("to what account (id):"))
                break

            a = my_account.transfer(amount, from_acc_id, to_acc_id)
            if a:
                print("OK")
            else:
                print("Something went wrong, we will tell soon exactly")
        elif command == "close_account":
            account_id = int(input("Enter the id of an account to close"))
            if account_id in my_account.MuAccountList:
                my_account.close_account(account_id)
                print(f"Now account {account_id} is dead")
            else:
                print("Sorry, an unavailable account number")




if __name__ == '__main__':  # будет возвожность войти в существующий аккаунт
    available_banks = {"sber": Sber}
    while True:
        print("Please, introduce yourself")
        while True:
            name = input("name:")
            surname = input("surname:")
            if name.split() and surname.split():
                break
            else:
                print("All fields must be filled in!")
        print("Please, enter the following data or skip by pressing Enter")
        address = input("address:")
        passport = input("passport:")
        client = Client(name, surname, address, passport)

        print("What bank you would like to be registered in?")
        while True:
            bank_name = input("Bank:")
            if not bank_name.lower() in available_banks:
                print("Sorry, this Bank is unavailable.")
            else:
                break
        my_account = SystemAccount(client, available_banks[bank_name.lower()], "1111")
        print(f"Congratulations, you are registered in {bank_name}!")
        working_space(my_account)
        break
