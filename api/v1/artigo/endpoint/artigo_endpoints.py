#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.artigo.acoes.artigo_acoes import ArtigoAcoes
from api.v1.artigo.model.artigo_model import ArtigoOutCreate, ArtigoInUpdate, ArtigoOutDelete, ArtigoOutUpdate, Artigo, \
    ArtigoFind, ArtigoInCreate
from api.v1.artigo.regras.artigo_regras import ArtigoRegras
from recursos.response_handler import ResponseHandler
from recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/artigo",
    tags=['Artigo']
)


class ArtigoEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=ArtigoFind
    )
    def find(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(_id=_id, handler=handler, regra='find')

        # realiza as acoes necessárias no model
        ArtigoAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    # O response_model_exclude funciona somente para a sucesso do request, mas não para a documentação
    @staticmethod
    @router.post(
        "",
        response_model=ArtigoOutCreate,
        status_code=201,
    )
    async def create(
            model: ArtigoInCreate,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ArtigoAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=ArtigoOutUpdate
    )
    async def update(
            model: ArtigoInUpdate,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(_id=_id, model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ArtigoAcoes(_id=_id, model=model, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200,
        response_model=ArtigoOutDelete
    )
    async def delete(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(_id=_id, handler=handler, regra='soft_delete')

        # realiza as acoes necessárias no model
        ArtigoAcoes(_id=_id, handler=handler, acao='soft_delete')

        return handler.sucesso