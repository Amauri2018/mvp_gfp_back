from pydantic import BaseModel
from typing import List

from model import Processar
from datetime import date
from calendar import monthrange

hoje = date.today()
data_p = date(hoje.year, hoje.month, 1) # dia 1 do mês atual
data_u = hoje.replace(day=monthrange(hoje.year, hoje.month)[1]) # ultimo dia do mês atual

class Processaschema(BaseModel):
    """ Define como um novo processamento a ser inserido, deve ser representada
    """
    data_i: date = data_p
    data_f: date = data_u
    total_rece: float = 0
    total_desp: float = 0
    total_caixa: float = 0

class ProcessarViewSchema(BaseModel):
    """ Define como o processamento será retornada
    """
    data_i: date = data_p
    data_f: date = data_u
    total_rece: float = 0
    total_desp: float = 0
    total_caixa: float = 0

class ProcessarUpdateViewSchema(BaseModel):
    """ Define como a receita será retornada
    """
    total_rece: float = 0
    total_desp: float = 0
    total_caixa: float = 0

class ProcessarUpdatechema(BaseModel):
    """ Define como a receita sera alterada, deve ser representada
    """
    id_proc: int = 0
    total_rece: float = 0
    total_desp: float = 0
    total_caixa: float = 0

class ListagemProcessarSchema(BaseModel):
    """ Define como uma listagem de processamento, que será retornada.
    """
    Processar:List[Processaschema]

class ProcessarBuscaPeriodoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no periodo da data.
    """
    datainicio: date = data_p
    datafim: date = data_u

class ProcessarDelSchema(BaseModel):
    """ Define como deve ser a estrutura de dados, retornado após uma requisição
        de remoção.
    """
    mesage: str

class ProcessarBuscaSchemaInt(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da receita.
    """
    id_proc: int = 0

def apresenta_processar(processar: Processar):
    """ Retorna uma representação da processamento seguindo o schema definido em
        ProcessasViewSchema.
    """
    return {
        "id": processar.id,
        "data_i": processar.data_i,
        "data_f": processar.data_f,
        "total_rece": processar.total_rece,
        "total_desp":processar.total_desp,
        "total_caixa":processar.total_caixa,
    }

def apresenta_Processas(processas: List[Processar]):
    """ Retorna uma representação da receita, seguindo o schema definido em
        ProcessarViewSchema.
    """
    result = []
    for processar in processas:
        result.append({
            "id": processar.id,
            "data_i": processar.data_i,
            "data_f": processar.data_f,
            "total_rece": processar.total_rece,
            "total_desp":processar.total_desp,
            "total_caixa":processar.total_caixa,
            })

    return {"processar": result}