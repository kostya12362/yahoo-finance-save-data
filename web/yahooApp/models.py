from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


def create_table(engine):
    Base.metadata.create_all(engine)


class Symbol(Base):
    __tablename__ = "symbol"
    id = Column(Integer,  primary_key=True, unique=True, nullable=False)
    symbol = Column(String, unique=True, nullable=False)
    history = relationship('HistoryInfo', backref='symbol', lazy='dynamic', order_by="HistoryInfo.date")

    def __repr__(self):
        return f'Symbol {self.symbol}'

    @hybrid_property
    def history_count(self):
        return self.history.count()


class HistoryInfo(Base):
    __tablename__ = "history"
    __table_args__ = (UniqueConstraint('symbol_id', 'date', name='_symbol_date_uc'),
                      )
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    symbol_id = Column(Integer, ForeignKey('symbol.id'))
    date = Column('date', Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)


class HistoryInfoCase(Base):
    __tablename__ = "history_tmp"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    symbol_id = Column(Integer)
    date = Column('date', Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)
