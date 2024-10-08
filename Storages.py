class AccountStorage:
  __accounts = {}

  def __init__(self, bank_name):
    self.bank = bank_name

  def find(self, id):
    if id in self.__accounts.keys():
      return self.__accounts[id]
    else:
      return None

  def add_new_account(self, id, new_account):
    self.__accounts[id] = new_account #изменить принцип добавления
  
  def close(self, id):
    cl_acc = self.__accounts.find(id)
    if cl_acc == None:
      return 111  # unavailable account number
    del self.__accounts[id]
    return True
  

class TransactionStorage:
  __transactions = {}

  def __init__(self, bank_name):
    self.bank = bank_name

  def add_transaction(self, t_id, transaction):
    self.__transactions[t_id] = transaction #изменить принцип добавления
  
  def cancel(self, trans_id):
    pass


class UserStorage:
  __users = {}

  def __init__(self, bank_name):
    self.bank = bank_name

  def find(self, login, password):
    if login in self.__users.keys():
      if password == self.__users[login][0]:
        return self.__users[login][1] #вернуть клсс my_account
      return 101
    return 102

  def add_new_user(self, login, password, sys_account):
    if login in self.__users.keys():
      return 103
    self.__users[login] = [password, sys_account] #изменить принцип добавления
    return True
      