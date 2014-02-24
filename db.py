from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///teabot.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

def create_all():
    Base.metadata.create_all(engine)


class WeightChange(Base):
    __tablename__ = 'weight_change'

    id = Column(Integer, primary_key=True)

    tare = Column(Integer)

    start_weight = Column(Integer)
    end_weight = Column(Integer)
    delta = Column(Integer)

    dt = Column(DateTime)

    def __init__(self, start_weight, end_weight, tare, dt=None):
        self.start_weight = start_weight
        self.end_weight = end_weight
        self.delta = start_weight - end_weight

        self.tare = tare
        self.dt = dt or datetime.now()


def record_weight_change(start_weight, end_weight, tare, dt=None):
    weight_change = WeightChange(start_weight, end_weight, tare, dt)
    session.add(weight_change)
    session.commit()
