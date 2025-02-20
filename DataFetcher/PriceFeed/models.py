from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True)
    currency_code = Column(String(10), nullable=False, index=True)
    rate = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    currency_type = Column(String(10), nullable=False)  # 'fiat' or 'crypto'
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    def __repr__(self):
        return f"<CurrencyRate(currency_code='{self.currency_code}', rate={self.rate}, type={self.currency_type})>"


class CurrencyLatestRate(Base):
    __tablename__ = 'currency_latest_rates'

    id = Column(Integer, primary_key=True)
    currency_code = Column(String(10), nullable=False, index=True)
    rate = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    currency_type = Column(String(10), nullable=False)  # 'fiat' or 'crypto'
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    def __repr__(self):
        return f"<CurrencyLatestRate(currency_code='{self.currency_code}', rate={self.rate}, type={self.currency_type})>"