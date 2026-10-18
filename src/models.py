from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LeituraCSV(Base):
    __tablename__ = "leituras_iot"

    id = Column(String(100), primary_key=True)
    room_id = Column(String(100), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    temperatura = Column(Integer, nullable=False)
    ambiente = Column(String(10), nullable=False)