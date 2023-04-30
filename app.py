from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Receita, Despesa, Processar
from logger import logger

from schemas.receita import *
from schemas.despesa import *
from schemas.processar import *
from schemas.error import *

from flask_cors import CORS


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
receita_tag = Tag(name="Receita", description="Adição, visualização, alteração e remoção de receita à base")
despesa_tag = Tag(name="Despesa", description="Adição, visualização, alteração e remoção de despesa à base")
processar_tag = Tag(name="Processar", description="Faz o processamento dos dados, pelo período de data ")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

############################## rotas para tabela receita #############################################

@app.post('/receita', tags=[receita_tag],
          responses={"200": ReceitaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_receita(form: Receitaschema):
    """Adicionado uma nova receita à base de dados.

    Retorna uma representação das receita.
    """
    receita = Receita(
        descricao=form.descricao,
        data=form.data,
        valor=form.valor,
        status=form.status,
        id_proc=form.id_proc)
    logger.debug(f"Adicionado receita de descrição: '{receita.descricao}'")
    try:
        # criando conexão com a base
        session = Session()
        
        # adicionando receita
        session.add(receita)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado receita de descrição: '{receita.descricao}'")
        return apresenta_receita(receita), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar receita '{receita.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/receitas', tags=[receita_tag],
         responses={"200": ListagemReceitasSchema, "404": ErrorSchema})
def get_receitas():
    """Faz a busca por todas, as receita cadastradas.

    Retorna uma representação da listagem de receitas.
    """
    logger.debug(f"Coletando receitas ")
    # criando conexão com a base
    session = Session()
   
    # fazendo a busca
    receitas = session.query(Receita).filter(Receita.id_proc == None).all()

    if not receitas:
        # se não há receitas cadastradas
        return {"receitas": []}, 200
    else:
        logger.debug(f"%d receitas econtradas" % len(receitas))
        # retorna a representação de receitas
        print(receitas)
        return apresenta_receitas(receitas), 200


@app.get('/receita', tags=[receita_tag],
         responses={"200": ListagemReceitasSchema, "404": ErrorSchema})
def get_receita(query: ReceitaBuscaSchema):
    """Faz a busca por receita, a partir da descricão da receita.

    Retorna uma representação da receita.
    """
    receita_descricao = query.descricao
    logger.debug(f"Coletando receita ")
    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    receita = session.query(Receita).filter(Receita.descricao == receita_descricao, Receita.id_proc == None).all()
    
    if not receita:
        # se não há receitas cadastradas
        return {"receita": []}, 200
    else:
        logger.debug(f"%d receita econtrada" % len(receita))
        # retorna a representação de receita
        print(receita)
        return apresenta_receitas(receita), 200


@app.delete('/receita', tags=[receita_tag],
            responses={"200": ReceitaDelSchema, "404": ErrorSchema})
def del_receita(query: ReceitaBuscaSchemaInt):
    """Deleta uma receita, a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    receita_id = query.id
    print(receita_id)

    logger.debug(f"Deletando dados sobre a receita #{receita_id}")
    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Receita).filter(Receita.id == receita_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado receita #{receita_id}")
        return {"mesage": "Receita removida", "id": receita_id}
    else:
        # se a receita não foi encontrada
        error_msg = "Receita não encontrada na base :/"
        logger.warning(f"Erro ao deletar Receita #'{receita_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/receita_periodo', tags=[receita_tag],
         responses={"200": ListagemReceitasSchema, "404": ErrorSchema})
def get_periodo_recet(query: ReceitaBuscaPeriodoSchema):
    """Faz a busca da receita, por periodo de data.

    Retorna uma representação da receita.
    """
    receita_id_proc = query.id_proc
    receita_datainicio = query.datainicio
    receita_datafim = query.datafim

    logger.debug(f"Coletando receita ")
    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    receita = session.query(Receita).filter(Receita.data.between(receita_datainicio, receita_datafim), Receita.id_proc == receita_id_proc).all()
    
    if not receita:
        # se não há receitas cadastradas
        return {"receitas": []}, 200
    else:
        logger.debug(f"%d receita econtrada" % len(receita))
        # retorna a representação de receita
        print(receita)
        return apresenta_receitas(receita), 200


@app.post('/receita_update', tags=[receita_tag],
          responses={"200": ReceitaUpdateViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_receita(query: ReceitasUpdatechema):
    """Atualiza o campo status da receita, com valor 1 "recebido", ou 0 "não recedido".

    Retorna uma representação das receita.
    """  
    receita_status = query.status
    receita_id = query.id

    logger.debug(f"Atualizando o campo status da receita id: '{receita_id}'")
 
    # criando conexão com a base
    session = Session()

    # altera receita
    receita = session.query(Receita).filter(Receita.id == receita_id, Receita.id_proc == None).update({Receita.status:receita_status}, synchronize_session = False)
    session.commit()

    if receita:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Status #{receita_id}")
        return {"mesage": "Status da receita Alterada", "id": receita_id}
    else:
        # se a receita não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar receita #'{receita_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.post('/receita_update_idProc', tags=[receita_tag],
         responses={"200": ReceitaUpdateViewSchema, "404": ErrorSchema})
def update_receita_idproc(query: ReceitasUpdateIdProdSchema):
    """Atualiza o campo id_proc, por periodo de data, com codigo do processamento.

    Retorna uma representação da receita.
    """
    receita_id_proc = query.id_proc
    receita_datainicio = query.datainicio
    receita_datafim = query.datafim

    logger.debug(f"Atualizando campo id_proc")
 
    # criando conexão com a base
    session = Session()

    # altera receita
    receita = session.query(Receita).filter(Receita.data.between(receita_datainicio, receita_datafim), Receita.id_proc == None, Receita.status == 1).update({Receita.id_proc:receita_id_proc}, synchronize_session = False)
    session.commit()
    
    if receita:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"id_proc #{receita_id_proc}")
        return {"mesage": "Campo id_proc da receita Atualizado", "id": receita_id_proc}
    else:
        # se a receita não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar receita #'{receita_id_proc}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.post('/receita_update_idProc_vazio', tags=[receita_tag],
         responses={"200": ReceitaUpdateViewSchema, "404": ErrorSchema})
def update_receita_idproc_vazio(query: ReceitasUpdateIdProdSchema):
    """Atualiza o campo id_proc da receita, para vazio, apos deletar o processaemento

    Retorna uma representação da receita.
    """
    receita_id_proc = query.id_proc
   
    logger.debug(f"Atualizando campo id_proc")
 
    # criando conexão com a base
    session = Session()

    # altera receita
    receita = session.query(Receita).filter(Receita.id_proc == receita_id_proc, Receita.status == 1).update({Receita.id_proc: None}, synchronize_session = False)
    session.commit()
    
    if receita:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"id_proc #{receita_id_proc}")
        return {"mesage": "Campo id_proc da receita Atualizado", "id": receita_id_proc}
    else:
        # se a receita não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar receita #'{receita_id_proc}', {error_msg}")
        return {"mesage": error_msg}, 404




############################## rotas para tabela despesas ############################################
@app.post('/despesa', tags=[despesa_tag],
          responses={"200": DespesaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_despesa(form: Despesaschema):
    """Adicionado uma nova despesa à base de dados.

    Retorna uma representação das despesa.
    """
    despesa = Despesa(
        descricao=form.descricao,
        data=form.data,
        valor=form.valor,
        status=form.status,
        id_proc=form.id_proc)
    logger.debug(f"Adicionado despesa de descrição: '{despesa.descricao}'")
    try:
        # criando conexão com a base
        session = Session()
       
        # adicionando despesa
        session.add(despesa)
       
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado despesa de descrição: '{despesa.descricao}'")
        return apresenta_despesa(despesa), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/despesas', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "404": ErrorSchema})
def get_despesas():
    """Faz a busca por todas, as despesa cadastradas.

    Retorna uma representação da listagem de despesas.
    """
    logger.debug(f"Coletando despesas ")
    # criando conexão com a base
    session = Session()
   
    # fazendo a busca
    despesas = session.query(Despesa).filter(Despesa.id_proc == None).all()

    if not despesas:
        # se não há despesas cadastradas
        return {"despesas": []}, 200
    else:
        logger.debug(f"%d despesas econtradas" % len(despesas))
        # retorna a representação de despesas
        print(despesas)
        return apresenta_despesas(despesas), 200


@app.get('/despesa', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "404": ErrorSchema})
def get_despesa(query: DespesaBuscaSchema):
    """Faz a busca por despesa, a partir da descricão da despesa.

    Retorna uma representação das despesas.
    """
    despesa_descricao = query.descricao
    logger.debug(f"Coletando despesa ")
    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    despesa = session.query(Despesa).filter(Despesa.descricao == despesa_descricao, Despesa.id_proc == None).all()
    
    if not despesa:
        # se não há despesa cadastrada
        return {"despesa": []}, 200
    else:
        logger.debug(f"%d despesa econtrada" % len(despesa))
        # retorna a representação da despesa
        print(despesa)
        return apresenta_despesas(despesa), 200


@app.delete('/despesa', tags=[despesa_tag],
            responses={"200": DespesaDelSchema, "404": ErrorSchema})
def del_despesa(query: DespesaBuscaSchemaInt):
    """Deleta uma despesa, a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    despesa_id = query.id
    print(despesa_id)
    logger.debug(f"Deletando dados sobre a despesa #{despesa_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Despesa).filter(Despesa.id == despesa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado despesa #{despesa_id}")
        return {"mesage": "Despesa removida", "id": despesa_id}
    else:
        # se a despesa não foi encontrada
        error_msg = "Despesa não encontrada na base :/"
        logger.warning(f"Erro ao deletar despesa #'{despesa_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.get('/despesa_periodo', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "404": ErrorSchema})
def get_periodo_desp(query: DespesaBuscaPeriodoSchema):
    """Faz a busca da despesa, por periodo de data.

    Retorna uma representação da despesa.
    """
    despesa_id_proc = query.id_proc
    despesa_datainicio = query.datainicio
    despesa_datafim = query.datafim

    logger.debug(f"Coletando despesa ")
    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    despesa = session.query(Despesa).filter(Despesa.data.between(despesa_datainicio, despesa_datafim), Despesa.id_proc == despesa_id_proc).all()
    
    if not despesa:
        # se não há despesa cadastradas
        return {"despesas": []}, 200
    else:
        logger.debug(f"%d despesa econtrada" % len(despesa))
        # retorna a representação da despesa
        print(despesa)
        return apresenta_despesas(despesa), 200

  
@app.post('/despesa_update', tags=[despesa_tag],
          responses={"200": DespesaUpdateViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_despesa(query: DespesasUpdatechema):
    """Atualiza o campo status da despesa, com valor 1 "pago", ou 0 "não pago.

    Retorna uma representação das despesa.
    """  
    despesa_status = query.status
    despesa_id = query.id

    logger.debug(f"Alterando status da despesa id: '{despesa_id}'")
 
    # criando conexão com a base
    session = Session()

    # altera despesa
    despesa = session.query(Despesa).filter(Despesa.id == despesa_id, Despesa.id_proc == None).update({Despesa.status:despesa_status}, synchronize_session = False)
    session.commit()

    if despesa:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Status #{despesa_id}")
        return {"mesage": "Status da despesa Alterada", "id": despesa_id}
    else:
        # se a despesa não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar despesa #'{despesa_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/despesa_update_idProc', tags=[despesa_tag],
         responses={"200": DespesaUpdateViewSchema, "404": ErrorSchema})
def update_despesa_idproc(query: DespesasUpdateIdProdSchema):
    """Atualiza o campo id_proc, por periodo de data, com codigo do processamento.

    Retorna uma representação da despesa.
    """
    despesa_id_proc = query.id_proc
    despesa_datainicio = query.datainicio
    despesa_datafim = query.datafim

    logger.debug(f"Atualizando campo id_proc")
 
    # criando conexão com a base
    session = Session()

    # altera despesa
    despesa = session.query(Despesa).filter(Despesa.data.between(despesa_datainicio, despesa_datafim), Despesa.id_proc == None , Despesa.status == 1).update({Despesa.id_proc:despesa_id_proc}, synchronize_session = False)
    session.commit()
    
    if despesa:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"id_proc #{despesa_id_proc}")
        return {"mesage": "Campo id_proc da despesa Atualizado", "id": despesa_id_proc}
    else:
        # se a despesa não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar despesa #'{despesa_id_proc}', {error_msg}")
        return {"mesage": error_msg}, 404    
    

@app.post('/despesa_update_idProc_vazio', tags=[despesa_tag],
         responses={"200": DespesaUpdateViewSchema, "404": ErrorSchema})
def update_despesa_idproc_vazio(query: DespesasUpdateIdProdSchema):
    """Atualiza o campo id_proc da despesa, para vazio, apos deletar o processaemento

    Retorna uma representação da despesa.
    """
    despesa_id_proc = query.id_proc

    logger.debug(f"Atualizando campo id_proc")
 
    # criando conexão com a base
    session = Session()

    # altera despesa
    despesa = session.query(Despesa).filter(Despesa.id_proc == despesa_id_proc , Despesa.status == 1).update({Despesa.id_proc:None}, synchronize_session = False)
    session.commit()
    
    if despesa:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"id_proc #{despesa_id_proc}")
        return {"mesage": "Campo id_proc da despesa Atualizado", "id": despesa_id_proc}
    else:
        # se a despesa não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar despesa #'{despesa_id_proc}', {error_msg}")
        return {"mesage": error_msg}, 404    






############################## rotas para tabela processado #############################################
@app.post('/processar', tags=[processar_tag],
          responses={"200": ProcessarViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_processar(form: Processaschema):
    """Adicionado um novo processamento à base de dados.

    Retorna uma representação dos processamento.
    """
    processar = Processar(
        data_i=form.data_i,
        data_f=form.data_f,
        total_rece=form.total_rece,
        total_desp=form.total_desp,
        total_caixa=form.total_caixa)
    logger.debug(f"Adicionado processamento de id: '{processar.id}'")
    try:
        # criando conexão com a base
        session = Session()
        
        # adicionando processamento
        session.add(processar)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado processamento de id: '{processar.id}'")
        return apresenta_processar(processar), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo processamento :/"
        logger.warning(f"Erro ao salvar o processamento '{processar.id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/processado_periodo', tags=[processar_tag],
         responses={"200": ListagemProcessarSchema, "404": ErrorSchema})
def get_periodo_proc(query: ProcessarBuscaPeriodoSchema):
    """Faz a busca do processamento, por periodo de data.

    Retorna uma representação do processamento.
    """
    processar_datainicio = query.datainicio
    processar_datafim = query.datafim

    logger.debug(f"Coletando processamento ")
    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    processar = session.query(Processar).filter(Processar.data_i >= processar_datainicio, Processar.data_f <= processar_datafim).all()
    
    if not processar:
        # se não há processamento cadastradas
        return {"processar": []}, 200
    else:
        logger.debug(f"%d processamento econtrado" % len(processar))
        # retorna a representação do processamento
        print(processar)
        return apresenta_Processas(processar), 200
    

@app.post('/processar_update', tags=[processar_tag],
          responses={"200": ProcessarUpdateViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_totalrece(query: ProcessarUpdatechema):
    """Atualiza o campo total_rece e total_desp do processamento, apos deleta um item da lista receita ou despesa".

    Retorna uma representação das processamento.
    """  
    processar_id_proc = query.id_proc
    processar_total_rece = query.total_rece
    processar_total_desp = query.total_desp
    processar_total_caixa = query.total_caixa

    logger.debug(f"Atualizando o campo total do processamento id: '{processar_id_proc}'")
 
    # criando conexão com a base
    session = Session()

    # altera processar
    processar = session.query(Processar).filter(Processar.id == processar_id_proc).update({Processar.total_rece:processar_total_rece, Processar.total_desp:processar_total_desp ,Processar.total_caixa:processar_total_caixa}, synchronize_session = False)
    session.commit()

    if processar:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Status #{processar_id_proc}")
        return {"mesage": "Campo total Alterado", "id": processar_id_proc}
    else:
        # se a receita não foi encontrada
        error_msg = "ID não encontrada na base :/"
        logger.warning(f"Erro ao alterar processamento #'{processar_id_proc}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/processar_deletar', tags=[processar_tag],
            responses={"200": ProcessarDelSchema, "404": ErrorSchema})
def del_processar(query: ProcessarBuscaSchemaInt):
    """Deleta um processamento, a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    processar_id_proc = query.id_proc
    print(processar_id_proc)

    logger.debug(f"Deletando dados sobre a processamento #{processar_id_proc}")
    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Processar).filter(Processar.id == processar_id_proc).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado processamento #{processar_id_proc}")
        return {"mesage": "Processamento removida", "id": processar_id_proc}
    else:
        # se a receita não foi encontrada
        error_msg = "Receita não encontrada na base :/"
        logger.warning(f"Erro ao deletar processamento #'{processar_id_proc}', {error_msg}")
        return {"mesage": error_msg}, 404


    