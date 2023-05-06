from Accounts import Debit, Credit, Deposit
from Storages import AccountStorage, UserStorage, TransactionStorage
from datetime import date
import uuid
from ex_info import EX_CODE_MESSAGES, INCORRECT_ACCOUNT_ID_ERROR, LIMITED_ACCOUNT_WITHDRAW_ERROR

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
    def __init__(self, name, address, **limits):
        self.name = name
        self.address = address
        self.limitations = BankLimitations(**limits)
        self.__accounts = AccountStorage(self.name)
        self.__transactions = TransactionStorage(self.name)
        self.__users = UserStorage(self.name)

    def find_user(self, login, password):
        user_account = self.__users.find(login, password)
        if user_account not in EX_CODE_MESSAGES.keys():  # changes
            user_account.bank = self
            user_account.MyAccountList = self.__accounts.find_all(user_account.UserID)
        return user_account

    def add_new_user(self, login, password, sys_account):
        return self.__users.add_new_user(login, password, sys_account)

    def make_transfer(self, amount, owner_acc_id, recip_acc_id, sys_acc_status):
        if not sys_acc_status and amount > self.limitations.trans_limit:
            return LIMITED_ACCOUNT_WITHDRAW_ERROR  # limited account. transfer limit exceeded
        acc_from = self.__accounts.find(owner_acc_id)
        acc_to = self.__accounts.find(recip_acc_id)
        if acc_from == None or acc_to == None:
            return INCORRECT_ACCOUNT_ID_ERROR  # non-existent account id
        operation = acc_from.transfer(amount, acc_to)
        if operation in EX_CODE_MESSAGES.keys():
            return operation

        self.__accounts.update_account_info(acc_from)
        self.__accounts.update_account_info(acc_to)
        t_id = uuid.uuid4().int
        details = {"amount": amount, "owner_acc_id": owner_acc_id, "recip_acc_id": recip_acc_id}
        sdate = date.today()
        self.__transactions.add_transaction(t_id, Transaction(t_id, sdate, "transfer", details))
        return True

    def make_top_up(self, amount, owner_acc_id):
        acc_to = self.__accounts.find(owner_acc_id)
        if acc_to == None:
            return INCORRECT_ACCOUNT_ID_ERROR  # non-existent account id
        acc_to.top_up(amount)
        self.__accounts.update_account_info(acc_to)
        t_id = uuid.uuid4().int
        details = {"amount": amount, "owner_acc_id": owner_acc_id}
        sdate = date.today()
        self.__transactions.add_transaction(t_id, Transaction(t_id, sdate, "top_up", details))
        return True

    def make_withdraw(self, amount, owner_acc_id, acc_status):
        if not acc_status and amount > self.limitations.withdraw_limit:
            return LIMITED_ACCOUNT_WITHDRAW_ERROR  # limited account. withdraw limit exceeded
        acc_to = self.__accounts.find(owner_acc_id)
        if acc_to == None:
            return INCORRECT_ACCOUNT_ID_ERROR  # non-existent account id
        operation = acc_to.withdraw(amount)
        if operation in EX_CODE_MESSAGES.keys():
            return operation

        self.__accounts.update_account_info(acc_to)
        t_id = uuid.uuid4().int
        details = {"amount": amount, "owner_acc_id": owner_acc_id}
        sdate = date.today()
        self.__transactions.add_transaction(t_id, Transaction(t_id, sdate, "withdraw", details))
        return True

    def cancel_transaction(self, trans_id):
        operation = self.__transactions.cancel(trans_id)
        return operation

    def create_account(self, owner_class, t_type, start_sum=0):
        new_acc_id = uuid.uuid4().int
        if t_type == "credit":
            limit = self.limitations.credit_limit
            commission = self.limitations.commission
            new_account = Credit(new_acc_id, owner_class.UserID, start_sum, limit, commission)
        elif t_type == "deposit":
            sdate = date.today()
            new_account = Deposit(new_acc_id, owner_class.UserID, start_sum, sdate, self.limitations.deposit_period)
        else:
            new_account = Debit(new_acc_id, owner_class.UserID)
        self.__accounts.add_new_account(new_acc_id, new_account)
        return new_account

    def close_account(self, account_id):
        operation = self.__accounts.close(account_id)
        return operation

    def show_accounts(self, UserID):
        return self.__accounts.find_all(UserID)

    def check_balance(self, acc_id):
        acc = self.__accounts.find(acc_id)
        if not acc in EX_CODE_MESSAGES.keys():
            return acc.balance
        return acc

    def update_user_info(self, user_sys_acc):
        self.__users.update_user_info(user_sys_acc)