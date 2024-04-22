from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref

from database import Base


class Agent(Base):
    __tablename__ = "agent"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(length=50), nullable=False)
    position = Column(String(length=15), nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100), nullable=False)
    add_date = Column(TIMESTAMP, nullable=False)
    contact = Column(String(length=100), nullable=False)
    from_source = Column(String(length=40), nullable=False)


class Provider(Base):
    __tablename__ = "provider"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100), nullable=False)
    platform = Column(String(length=15), nullable=False)
    branch = Column(String(length=50), nullable=False)
    site = Column(String(length=250))
    contact = Column(String(length=100), nullable=False)


class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey(Provider.id))
    agent_id = Column(Integer, ForeignKey(Agent.id))
    title = Column(String(length=200), nullable=False)
    price_per_day = Column(Numeric(precision=10, scale=2), nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    duration_days = Column(Integer, nullable=False)
    doc_link = Column(String(length=200), nullable=False)

    seller = relationship("Provider", lazy="joined")
    agent = relationship("Agent", lazy="joined")


class Deal(Base):
    __tablename__ = "deal"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey(Client.id))
    agent_id = Column(Integer, ForeignKey(Agent.id))
    contract_id = Column(Integer, ForeignKey(Contract.id))
    full_price = Column(Numeric(precision=10, scale=2), nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    duration_days = Column(Integer, nullable=False)

    client = relationship("Client", lazy="joined")
    agent = relationship("Agent", lazy="joined")
    contract = relationship("Contract", lazy="joined", backref=backref("deals"))


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey(Deal.id))
    pay_value = Column(Numeric(precision=10, scale=2), nullable=False)
    create_date = Column(TIMESTAMP, nullable=False)

    deal = relationship("Deal", lazy="joined", backref=backref("payments"))

