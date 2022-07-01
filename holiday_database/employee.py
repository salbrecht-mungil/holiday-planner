from sqlalchemy import Column, String, Integer, ForeignKey
from base import Base
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager_id = Column(Integer, ForeignKey('managers.id'))
    manager = relationship('Manager')
    

    def __init__(self, name, manager):
        self.name = name
        self.manager = manager