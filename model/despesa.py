from sqlalchemy import Column, String, Integer, Date, Float
from datetime import date
from typing import Union

from model import Base

class Despesa(Base):
    __tablename__ = 'despesa'

    id = Column("pk_despesa", Integer, primary_key=True)
    descricao = Column(String(300))
    data = Column(Date, default=date.today())
    valor = Column(Float)
    status = Column(Integer, default=0)
    id_proc = Column(Integer, default=None)

    def __init__(self, descricao:str, status:Integer, id_proc:Integer, valor:float, data:Union[Date, None] = None):
        """
        Cria a despesa

        Arguments:
            descrição: descrição da despesa.
            data: data de quando o despesa foi inserido à base
            valor: valor da entrada de despesa
        """
        self.descricao = descricao
        if status:
            self.status = status
        if id_proc:
            self.id_proc = id_proc
        self.valor = valor
        if data:
            self.data = data


