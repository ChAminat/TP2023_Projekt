from Banks import *
from Account import *
from datetime import date
import random

class Transaction:
    def __init__(self, tr_id, sdate, t_type, details):
        self.transaction_ID = tr_id
        self.details = details
        self.type = t_type
        self.sdate = sdate


class BankLimitations:
    def __init__(self, commission=0, trans_limit=0, withdraw_limit=0, credit_limit=0, period=1):
        self.commission = commission
        self.trans_limit = trans_limit
        self.withdraw_limit = withdraw_limit
        self.credit_limit = credit_limit
        self.deposit_period = period


class Bank:
    __account = {}
    __users = {}
    __transactions = {}

    def __init__(self, name, address, **limits):
        self.name = name
        self.address = address
        self.limitations = BankLimitations(**limits)

    def make_transfer(self, amount, owner_acc_id, recip_acc_id, acc_status):
        if not acc_status and amount > self.limitations.trans_limit:
            print("to high amount of money, change sum")
            return False

        a = self.__account[owner_acc_id].transfer(amount, self.__account[recip_acc_id])
        if not a:
            return False

        t_id = random.randrange(10000000, 99999999)
        details = [amount, owner_acc_id, recip_acc_id]
        sdate = date.today()
        self.__transactions[t_id] = Transaction(t_id, sdate, "transfer", details)
        return

    def make_top_up(self, amount, owner_acc_id):
        self.__account[owner_acc_id].top_up(amount)
        t_id = random.randrange(10000000, 99999999)
        details = [amount, owner_acc_id]
        sdate = date.today()
        self.__transactions[t_id] = Transaction(t_id, sdate, "top_up", details)
        return

    def make_withdraw(self, amount, owner_acc_id, acc_status):
        if not acc_status and amount > self.limitations.withdraw_limit:
            print("to high amount of money, change sum")
            return False
        a = self.__account[owner_acc_id].withdraw(amount)
        if not a:
            return False
        t_id = random.randrange(10000000, 99999999)
        details = [amount, owner_acc_id]
        sdate = date.today()
        self.__transactions[t_id] = Transaction(t_id, sdate, "withdraw", details)
        return

    def cancel_transaction(self, trans_id):
        ###########################
        pass

    def create_account(self, owner_class, t_type, start_sum=0):
        new_acc_id = random.randrange(10000000, 99999999)
        if t_type == "credit":
            limit = self.limitations.credit_limit
            commission = self.limitations.commission
            new_account = Credit(new_acc_id, owner_class.UserID, start_sum, limit, commission)
        elif t_type == "deposit":
            sdate = date.today()
            new_account = Deposit(new_acc_id, owner_class.UserID, start_sum, sdate, self.limitations.deposit_period)
        else:
            new_account = Debit(new_acc_id, owner_class.UserID)
        self.__account[new_acc_id] = new_account
        return new_account

    def close_account(self, account_id):
        self.__account[account_id].close()
        del self.__account[account_id]


Sber = Bank("Sber", "Moscow", commission=100, trans_limit=100, withdraw_limit=1000, credit_limit=1000, period=1)