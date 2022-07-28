#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.modalidade_artigo.acoes.modalidade_artigo_acoes import ModalidadeArtigoAcoes
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigoOut, ModalidadeArtigoIn
from api.v1.modalidade_artigo.regras.modalidade_artigo_regras import ModalidadeArtigoRegras
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/modalidade_artigo",
    tags=['ModalidadeArtigo']
)


class ArtigoEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=ModalidadeArtigoOut
    )
    def find(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # valida as regras necessárias no model

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    # O response_model_exclude funciona somente para a sucesso do request, mas não para a documentação
    @staticmethod
    @router.post(
        "",
        response_model=ModalidadeArtigoOut,
        status_code=201
    )
    async def create(
            model: ModalidadeArtigoIn,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=ModalidadeArtigoOut
    )
    async def update(
            model: ModalidadeArtigoIn,
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(_id=_id, model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(_id=_id, model=model, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200
    )
    async def delete(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ModalidadeArtigoRegras(_id=_id, handler=handler, regra='softdelete')

        # realiza as acoes necessárias no model
        ModalidadeArtigoAcoes(_id=_id, handler=handler, acao='softdelete')

        return handler.sucesso
