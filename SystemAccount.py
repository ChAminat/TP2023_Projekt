import random

class Client:
    def __init__(self, name, surname, address='', passport=''):
        self.user_name = name
        self.user_surname = surname
        self.address = address
        self.passport = passport

    def check_status(self):
        if self.address.split() and self.passport.split():
            return True
        return False


class SystemAccount:
    __password = ""
    MuAccountList = {}
    UserID = random.randint(1000000, 9999999)

    def __init__(self, client, bank, password):
        self.MyInfo = client
        self.bank = bank
        self.__password = password

    def edit_sys_account(self, address, passport_data):
        self.MyInfo.address = address
        self.MyInfo.passport = passport_data

    def check_password(self, password):
        if password == self.__password:
            return
        print("incorrect password")
        return False

    def open_new_account(self, t_type, start_sum=0):
        new_acc = self.bank.create_account(self, t_type, start_sum)
        self.MuAccountList[new_acc.account_id] = new_acc
        return new_acc.account_id

    def close_account(self, account_id):
        self.bank.close_account(account_id)
        del self.MuAccountList[account_id]

    def transfer(self, amount, from_acc_id, to_acc_id):
        return self.bank.make_transfer(amount, from_acc_id, to_acc_id, self.MyInfo.check_status())

    def top_up(self, amount, acc_id):
        self.bank.make_top_up(amount, acc_id)

    def withdraw(self, amount, acc_id):
        self.bank.make_withdraw(amount, acc_id, self.MyInfo.check_status())

    def balance(self, acc_id):
        return self.MuAccountList[acc_id].check_balance()
