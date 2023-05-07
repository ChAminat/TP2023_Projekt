from Banks import Bank


Sber = Bank("sber", "Moscow", commission=100, trans_limit=100, withdraw_limit=1000, credit_limit=1000, period=1)

available_banks = {"sber": Sber}  # changes
