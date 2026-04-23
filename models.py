from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    dun14 = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    unidade = Column(String, default="CX")

class Recebimento(Base):
    __tablename__ = "recebimentos"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.now)
    itens = relationship("ItemRecebimento", back_populates="recebimento")
    historico = relationship("Historico", back_populates="recebimento", uselist=False)

class ItemRecebimento(Base):
    __tablename__ = "itens_recebimento"

    id = Column(Integer, primary_key=True, index=True)
    recebimento_id = Column(Integer, ForeignKey("recebimentos.id"), nullable=False)
    dun14 = Column(String, nullable=False)
    nome_produto = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    recebimento = relationship("Recebimento", back_populates="itens")

class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True, index=True)
    recebimento_id = Column(Integer, ForeignKey("recebimentos.id"), nullable=False, unique=True)
    nome = Column(String, nullable=False)
    data = Column(DateTime, default=datetime.now)
    recebimento = relationship("Recebimento", back_populates="historico")