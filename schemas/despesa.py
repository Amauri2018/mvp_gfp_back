from pydantic import BaseModel
from typing import List

from model import Despesa
from datetime import date
from calendar import monthrange

hoje = date.today()
data_p = date(hoje.year, hoje.month, 1) # dia 1 do mês atual
data_u = hoje.replace(day=monthrange(hoje.year, hoje.month)[1]) # ultimo dia do mês atual

class Despesaschema(BaseModel):
    """ Define como uma nova despesa a ser inserido, deve ser representada
    """
    descricao: str = ""
    data: date = hoje
    valor: float = 0
    status: int = 0
    id_proc: int = 0

class DespesaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no descrição da despesa.
    """
    descricao: str = ""

class DespesaBuscaPeriodoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no periodo da data.
    """
    id_proc: int = 0
    datainicio: date = data_p
    datafim: date = data_u

class DespesaBuscaSchemaInt(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da despesa.
    """
    id: int = 0

class DespesaUpdateViewSchema(BaseModel):
    """ Define como a receita será retornada
    """
    id: int = 0
    status: int = 0
    descricao: str = ""
    
class DespesasUpdatechema(BaseModel):
    """ Define como a receita sera alterada, deve ser representada
    """
    id: int = 0
    status: int = 0

class DespesasUpdateIdProdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no periodo da data.
    """
    id_proc: int = 0
    datainicio: date = data_p
    datafim: date = data_u

class ListagemDespesasSchema(BaseModel):
    """ Define como uma listagem de despesas, que será retornada.
    """
    despesa:List[Despesaschema]

def apresenta_despesas(despesas: List[Despesa]):
    """ Retorna uma representação da despesa, seguindo o schema definido em
        DespesasViewSchema.
    """
    result = []
    for despesa in despesas:
        result.append({
            "id": despesa.id,
            "descricao": despesa.descricao,
            "data": despesa.data,
            "valor": despesa.valor,
            "status": despesa.status,
            "id_proc":despesa.id_proc,
        })

    return {"despesas": result}


class DespesaViewSchema(BaseModel):
    """ Define como a despesa será retornada
    """
    descricao: str = ""
    data: date = hoje
    valor: float = 0
    status: int = 0
    id_proc: int = 0
    
class DespesaDelSchema(BaseModel):
    """ Define como deve ser a estrutura de dados, retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str
  
def apresenta_despesa(despesa: Despesa):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesasViewSchema.
    """
    return {
        "id": despesa.id,
        "descricao": despesa.descricao,
        "data": despesa.data,
        "valor": despesa.valor,
        "status":despesa.status,
        "id_proc":despesa.id_proc,
    }
