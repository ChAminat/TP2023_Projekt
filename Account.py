from datetime import date
from ex_info import ex_code_dct


class Account:
    balance = 0.0

    def __init__(self, new_acc_id, owner_id, balance=0.0):
        self.owner_id = owner_id
        self.account_id = new_acc_id
        self.balance = balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return 301 # insufficient funds to withdraw

    def transfer(self, amount, recip_acc):
        a = self.withdraw(amount)
        if a:
            recip_acc.balance += amount
            return True
        return 301 # insufficient funds for the transfer

    def top_up(self, amount):
        self.balance += amount

    def close(self):
        self.balance = 0.0
        self.account_id = None

    def check_balance(self):
        return self.balance


class Deposit(Account):
    ac_type = "deposit"
    def __init__(self, new_acc_id, owner_id, start_sum, sdate, validity_period):
        super().__init__(new_acc_id, owner_id, start_sum)
        self.sdate = sdate
        self.validity_period = validity_period

    def withdraw(self, amount):
        now_date = date.today()
        if now_date < self.sdate + self.validity_period:
            return 311  # validity_period is not finished
        return super().withdraw(amount)

    def transfer(self, amount, recip_acc):
        now_date = date.today()
        if now_date < self.sdate + self.validity_period:
            return 311  # validity_period is not finished
        return super().transfer(amount, recip_acc)


class Credit(Account):
    ac_type = "credit"
    def __init__(self, account_id, owner_id, balance, limit, commission):
        super().__init__(account_id, owner_id, balance)
        self.limit = limit
        self.commission = commission

    def withdraw(self, amount):
        com = self.commission if self.balance < 0 else 0
        if abs(self.balance - amount - com) <= self.limit:
            self.balance -= amount + com
            return True
        return 312 #withdrawal limit exceeded

    def transfer(self, amount, to_account):
        operation = self.withdraw(amount)
        if not operation in ex_code_dct.keys(): #проверить на код ошибки
            to_account.balance += amount
            return True
        return operation


class Debit(Account):
    ac_type = "debit"
    def __init__(self, account_id, owner_id):
        super().__init__(account_id, owner_id)
