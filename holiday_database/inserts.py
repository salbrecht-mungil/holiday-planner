from datetime import date, datetime
from base import Session, engine, Base

from employee import Employee
from manager import Manager
from holiday import Holiday

# Generate database schema
Base.metadata.create_all(engine)
# Create new session
session = Session()

# Create managers
balin = Manager('Balin')
gimli = Manager('Gimli')

# Create employees
frodo_baggins = Employee('Frodo Baggins', gimli)
samwise_gamgee = Employee('Samwise Gamgee', balin)
peregrin_took = Employee('Peregrin Took', balin)
meriadoc_brandybock = Employee('Meriadoc Brandybock', gimli)

# Create holidays
frodo_hol_1 = Holiday('approved', date(2022, 1, 21), datetime(2022, 1, 23, 12, 00), datetime(2022, 1, 24, 23, 59), frodo_baggins, gimli, 1.5)
frodo_hol_2 = Holiday('approved', date(2022, 1, 25), datetime(2022, 1, 26, 00, 00), datetime(2022, 1, 27, 23, 59), frodo_baggins, gimli, 2)
samwise_hol_1 = Holiday('approved', date(2022, 2, 21), datetime(2022, 3, 3, 12, 00), datetime(2022, 3, 10, 11, 59), samwise_gamgee, balin, 7)
peregrin_hol_1 = Holiday('approved', date(2022, 2, 21), datetime(2022, 3, 12, 00, 00), datetime(2022, 3, 24, 23, 59), peregrin_took, balin, 13)
meriadoc_hol_1 = Holiday('rejected', date(2022, 2, 22), datetime(2022, 3, 12, 00, 00), datetime(2022, 3, 18, 23, 59), meriadoc_brandybock, gimli, 7)
meriadoc_hol_2 = Holiday('pending', date(2022, 6, 29), datetime(2022, 8, 1, 00, 00), datetime(2022, 8, 20, 23, 59), meriadoc_brandybock, gimli, 21)

# Persisting data
session.add(frodo_baggins)
session.add(samwise_gamgee)
session.add(peregrin_took)
session.add(meriadoc_brandybock)

session.add(balin)
session.add(gimli)

session.add(frodo_hol_1)
session.add(frodo_hol_2)
session.add(samwise_hol_1)
session.add(peregrin_hol_1)
session.add(meriadoc_hol_1)
session.add(meriadoc_hol_2)

# Commit and close session
session.commit()
session.close()