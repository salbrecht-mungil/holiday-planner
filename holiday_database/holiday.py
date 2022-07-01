from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Numeric
from base import Base
from sqlalchemy.orm import relationship
from employee import Employee
from manager import Manager

class Holiday(Base):
    __tablename__ = 'holidays'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship(Employee, backref='holidays')
    manager_id = Column(Integer, ForeignKey('managers.id'))
    manager = relationship(Manager, backref='holidays')
    status = Column(String)
    created_at_date = Column(Date)
    holiday_start_date = Column(DateTime)
    holiday_end_date = Column(DateTime)
    number_of_holidays = Column(Numeric)

    def __init__(self, status, created_at_date, holiday_start_date, holiday_end_date, employee, manager, number_of_holidays):
        self.status = status
        self.created_at_date = created_at_date
        self.holiday_start_date = holiday_start_date
        self.holiday_end_date = holiday_end_date
        self.employee = employee
        self.manager = manager
        self.number_of_holidays = number_of_holidays