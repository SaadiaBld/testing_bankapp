from models import Transaction, Account
from init_db import setup_db


session = setup_db()

#ajout de nouveaux comptes
account1 = Account('Batman', session=session)
account2 = Account('Robin', session=session)
account3 = Account('Hulk', session=session)


session.add_all([account1, account2, account3])

session.commit()
account1.deposit(500)
account2.deposit(1500)
account2.withdraw(1000)
account2.transfer(500, account3)
session.close()
