class AccountStorage:
  __accounts = {}

  def find(self, id):
    if id in self.__accounts.keys():
      return self.__accounts[id]
    else:
      return None

  def add_new_account(self, id, new_account):
    self.__accounts[id] = new_account
  
  def close(self, id):
    cl_acc = self.__accounts.find(id)
    if cl_acc == None:
      return False
    del self.__accounts[id]
    return True
  

class TransactionStorage:
  __transactions = {}

  def add_transaction(self, t_id, transaction):
    self.__transactions[t_id] = transaction
  
  def cancel(self, trans_id):
    pass