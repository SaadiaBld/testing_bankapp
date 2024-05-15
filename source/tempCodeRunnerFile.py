from models import *
from init_db import *


Session = setup_db()
session =Session()

#ajout de nouveaux comptes
account1 = Account('Batman', session=session)
account2 = Account('Robin', session=session)
account3 = Account('Hulk', session=session)


session.add_all([account1, account2, account3])

session.commit()
account1.deposit(500)
session.commit()
account2.deposit(1500)
session.commit()
account2.withdraw(1000)
session.close()

# if __name__ == "**main**":
# 	main()
	