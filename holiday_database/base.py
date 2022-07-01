from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creating PosgreSQL to communicate with an instance running locally on port 5432.
# Defining usr and pass as credentials to access sqlalchemy database
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
# Creating ORM session factory bound to engine
Session = sessionmaker(bind=engine)
# base class for classes definitions
Base = declarative_base()