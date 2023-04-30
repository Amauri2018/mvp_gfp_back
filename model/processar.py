from sqlalchemy import Column, String, Integer, Date, Float
from datetime import date
from calendar import monthrange
from typing import Union

from model import Base

hoje = date.today()
data_p = date(hoje.year, hoje.month, 1) # dia 1 do mês atual
data_u = hoje.replace(day=monthrange(hoje.year, hoje.month)[1]) # ultimo dia do mês atual


class Processar(Base):
    __tablename__ = 'processado'

    id = Column("pk_proc", Integer, primary_key=True)
    data_i = Column(Date, default=data_p)
    data_f = Column(Date, default=data_u)
    total_rece = Column(Float)
    total_desp = Column(Float)
    total_caixa = Column(Float)
    
    def __init__(self, total_rece:float, total_desp:float, total_caixa:float, data_i:Union[Date, None] = None , data_f:Union[Date, None] = None):
        """
        Cria o Processamento

        Arguments:
            total_rece: total da receitas mensal.
            total_desp: total da despesas mensal
            total_caixa: total do caixa processado
            data_i: primeiro dia do mês
            data_f: ultimo dia do mês
        """

        self.total_rece = total_rece
        self.total_desp = total_desp
        self.total_caixa = total_caixa
        if data_i:
            self.data_i = data_i
        if data_f:
            self.data_f = data_f


