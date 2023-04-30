from pydantic import BaseModel
from typing import List

from model import Receita
from datetime import date
from calendar import monthrange

hoje = date.today()
data_p = date(hoje.year, hoje.month, 1) # dia 1 do mês atual
data_u = hoje.replace(day=monthrange(hoje.year, hoje.month)[1]) # ultimo dia do mês atual

class Receitaschema(BaseModel):
    """ Define como uma nova receita a ser inserido, deve ser representada
    """
    descricao: str = ""
    data: date = hoje
    valor: float = 0
    status: int = 0
    id_proc: int = 0

class ReceitaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no descrição da receita.
    """
    descricao: str = ""

class ReceitaBuscaPeriodoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no periodo da data.
    """
    id_proc: int = 0
    datainicio: date = data_p
    datafim: date = data_u

class ReceitaBuscaSchemaInt(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da receita.
    """
    id: int = 0

class ReceitaUpdateViewSchema(BaseModel):
    """ Define como a receita será retornada
    """
    id: int = 0
    status: int = 0
    descricao: str = ""
    
class ReceitasUpdatechema(BaseModel):
    """ Define como a receita sera alterada, deve ser representada
    """
    id: int = 0
    status: int = 0

class ReceitasUpdateIdProdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no periodo da data.
    """
    id_proc: int = 0
    datainicio: date = data_p
    datafim: date = data_u

class ListagemReceitasSchema(BaseModel):
    """ Define como uma listagem de receitas, que será retornada.
    """
    receitas:List[Receitaschema]

def apresenta_receitas(receitas: List[Receita]):
    """ Retorna uma representação da receita, seguindo o schema definido em
        ReceitasViewSchema.
    """
    result = []
    for receita in receitas:
        result.append({
            "id": receita.id,
            "descricao": receita.descricao,
            "data": receita.data,
            "valor": receita.valor,
            "status": receita.status,
            "id_proc":receita.id_proc,
        })

    return {"receitas": result}


class ReceitaViewSchema(BaseModel):
    """ Define como a receita será retornada
    """
    descricao: str = ""
    data: date = hoje
    valor: float = 0
    status: int = 0
    id_proc: int = 0
   
class ReceitaDelSchema(BaseModel):
    """ Define como deve ser a estrutura de dados, retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

def apresenta_receita(receita: Receita):
    """ Retorna uma representação da receita seguindo o schema definido em
        ReceitasViewSchema.
    """
    return {
        "id": receita.id,
        "descricao": receita.descricao,
        "data": receita.data,
        "valor": receita.valor,
        "status":receita.status,
        "id_proc":receita.id_proc,
    }
