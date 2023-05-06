from ex_info import USER_NOT_FOUND_ERROR, INCORRECT_PASSWORD_ERROR, ACCOUNT_NUMBER_ERROR, EXISTED_LOGIN_ERROR
import sqlite3 as sq
from SystemAccount import SystemAccount, Client
from Accounts import Debit, Deposit, Credit
from datetime import datetime


class AccountStorage:
    # __accounts = {}

    def __init__(self, bank_name):
        self.bank = bank_name

    def find(self, id):
        '''
        if id in self.__accounts.keys():
            return self.__accounts[id]
        else:
            return None
        '''
        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            query = f'SELECT * FROM Accounts WHERE AccountId == "{str(id)}"'
            cur.execute(query)
            result = cur.fetchall()
            if not result:
                return None

            result = result[0]
            ownerID, accountID, balance = result[0], int(result[1]), float(result[2])
            if result[3] == "deposit":
                date_time_obj = datetime.strptime(result[4], '%Y-%m-%d').date()
                account = Deposit(accountID, ownerID, balance, date_time_obj, int(result[5]))
            elif result[3] == "debit":
                account = Debit(accountID, ownerID)
                account.balance = balance
            else:
                account = Credit(accountID, ownerID, balance, float(result[6]), float(result[7]))
        return account

    def find_all(self, owner_id):
        accout_class_dct = {}
        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            query = f'SELECT * FROM Accounts WHERE OwnerId == "{owner_id}"'
            cur.execute(query)
            result = cur.fetchall()
            for account_line in result:
                next_acc = self.find(account_line[1])
                accout_class_dct[int(account_line[1])] = next_acc
        return accout_class_dct

    def add_new_account(self, id, new_account):
        # self.__accounts[id] = new_account

        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            ownerID, accountID = new_account.owner_id, new_account.account_id
            balance, acType = new_account.balance, new_account.ac_type

            startDate, valPeriod, Limit, Commission = "", "", "", ""
            if acType == "credit":
                Limit, Commission = new_account.limit, new_account.commission
            elif acType == "deposit":
                startDate, valPeriod = new_account.sdate, new_account.validity_period

            query = """INSERT INTO Accounts VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
            cur.execute(query, (str(ownerID), str(accountID), str(balance), \
                                str(acType), str(startDate), str(valPeriod), \
                                str(Limit), str(Commission)))

    def update_account_info(self, account_class):
        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            balance, accountID = account_class.balance, account_class.account_id

            query = f"""UPDATE Accounts SET Balance = '{balance}' WHERE AccountId = '{accountID}'"""
            cur.execute(query)

    def close(self, id):
        '''
        cl_acc = self.__accounts.find(id)
        if cl_acc == None:
            return ACCOUNT_NUMBER_ERROR  # unavailable account number
        del self.__accounts[id]  # изменить удаление
        return True
        '''

        cl_acc = self.find(id)
        if cl_acc == None:
            return ACCOUNT_NUMBER_ERROR

        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            query = f"""DELETE FROM Accounts WHERE AccountId = '{id}'"""
            cur.execute(query)

        return True


class TransactionStorage:
    __transactions = {}

    def __init__(self, bank_name):
        self.bank = bank_name

    def add_transaction(self, t_id, transaction):
        self.__transactions[t_id] = transaction

    def cancel(self, trans_id):
        pass


class UserStorage:
    # __users = {}

    def __init__(self, bank_name):
        self.bank = bank_name

    def find(self, login, password):
        '''
        if login in self.__users.keys():
            if password == self.__users[login][0]:
                return self.__users[login][1]
            return INCORRECT_PASSWORD_ERROR
        # return USER_NOT_FOUND_ERROR
        '''

        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            query = f'SELECT * FROM Users WHERE login == "{login}"'
            cur.execute(query)
            result = cur.fetchall()
            if not result:
                return USER_NOT_FOUND_ERROR

            result = result[0]
            if result[1] != password:
                return INCORRECT_PASSWORD_ERROR

            name, surname, address, passport = result[2:6]
            client = Client(name, surname, address, passport)
            my_account = SystemAccount(client, result[6], login, password)
            my_account.UserID = result[7]
            return my_account

    def add_new_user(self, login, password, sys_account):
        '''
        if login in self.__users.keys():
            return EXISTED_LOGIN_ERROR
        self.__users[login] = [password, sys_account]
        '''

        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            cur.execute("SELECT login FROM Users")
            flag = True
            for log in cur:
                if log[0] == login:
                    flag = False
                    break
            if not flag:
                return EXISTED_LOGIN_ERROR

            name, surname = sys_account.user.userName(), sys_account.user.userSurname()
            address, passport = sys_account.user.userAddress(), sys_account.user.userPassport()
            bank, userId = self.bank, sys_account.UserID
            query = """INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
            cur.execute(query, (login, password, name, surname, address, passport, bank, userId))
        return True

    def update_user_info(self, user_sys_acc):
        ID, address, passport = user_sys_acc.UserID, user_sys_acc.user.client.address, user_sys_acc.user.client.passport
        with sq.connect(f"{self.bank}.db") as data:
            cur = data.cursor()
            query = f"""UPDATE Users SET address = '{address}', passport = '{passport}' WHERE UserID = '{ID}'"""
            cur.execute(query)
