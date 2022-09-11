#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.modalidade_artigo.acoes.modalidade_artigo_acoes import ModalidadeArtigoAcoes
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigoOut, ModalidadeArtigoIn, \
    ModalidadeArtigoOutCreate, ModalidadeArtigoOutDelete, ModalidadeArtigoUpdate
from api.v1.modalidade_artigo.regras.modalidade_artigo_regras import ModalidadeArtigoRegras
from recursos.response_handler import ResponseHandler
from recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/modalidade_artigo",
    tags=['ModalidadeArtigo']
)


class ModalidadeArtigoEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=ModalidadeArtigoOut
    )
    def find(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(_id=_id, handler=handler, regra='find')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    @staticmethod
    @router.post(
        "",
        response_model=ModalidadeArtigoOutCreate,
        status_code=201
    )
    async def create(
            model: ModalidadeArtigoIn,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(model=model, handler=handler, regra='create')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=ModalidadeArtigoUpdate
    )
    async def update(
            model: ModalidadeArtigoIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(_id=_id, model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(_id=_id, model=model, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200,
        response_model=ModalidadeArtigoOutDelete
    )
    async def delete(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(_id=_id, handler=handler, regra='soft_delete')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(_id=_id, handler=handler, acao='soft_delete')

        return handler.sucesso
