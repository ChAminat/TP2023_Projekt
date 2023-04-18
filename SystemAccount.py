import uuid


class Client:
    def __init__(self, name, surname, address='', passport=''):
        self.user_name = name
        self.user_surname = surname
        self.address = address
        self.passport = passport


class UserInfo:
    def __init__(self, client):
        self.client = client

    def userName(self):
        return self.client.user_name

    def userSurname(self):
        return self.client.user_surname

    def userAddress(self):
        return self.client.address

    def userPassport(self):
        return self.client.passport

    def check_status(self):
        if self.client.address.split() and self.client.passport.split():
            return True
        return False


class SystemAccount:
    __password = ""
    MyAccountList = {}
    UserID = str(uuid.uuid4())

    def __init__(self, client, bank, password):
        self.user = UserInfo(client)
        self.bank = bank
        self.__password = password

    def edit_sys_account(self, address, passport_data):
        self.user.userAddress = address
        self.user.userPassport = passport_data

    def check_password(self, password):
        if password == self.__password:
            return True
        return False  # your password is incorrect

    def open_new_account(self, t_type, start_sum=0):
        new_acc = self.bank.create_account(self, t_type, start_sum)
        self.MyAccountList[new_acc.account_id] = new_acc
        return new_acc.account_id

    def close_account(self, account_id):
        self.bank.close_account(account_id)
        del self.MyAccountList[account_id]

    def transfer(self, amount, from_acc_id, to_acc_id):
        return self.bank.make_transfer(amount, from_acc_id, to_acc_id, self.user.check_status())

    def top_up(self, amount, acc_id):
        return self.bank.make_top_up(amount, acc_id)

    def withdraw(self, amount, acc_id):
        return self.bank.make_withdraw(amount, acc_id, self.user.check_status())

    def balance(self, acc_id):
        return self.MyAccountList[acc_id].check_balance()
