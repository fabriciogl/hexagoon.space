#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from recursos.response_handler import ResponseHandler
from recursos.validations.token_role_validation import valida_role
from api.v1.role.acoes.role_acoes import RoleAcoes
from api.v1.role.model.role_model import RoleOut, RoleIn, SubRoleIn
from api.v1.role.regras.role_regras import RoleRegras
from banco_dados.mongodb.configuracao.MongoConection import Sessao

router = APIRouter(
    prefix="/role",
    tags=['Role']
)


class RoleEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=RoleOut
    )
    async def find(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        RoleRegras(_id=_id, handler=handler, regra='find')
        # realiza as acoes necessárias no model
        RoleAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    # O response_model_exclude funciona somente para a sucesso do request, mas não para a documentação
    @staticmethod
    @router.post(
        "",
        response_model=RoleOut,
        status_code=201
    )
    async def create(
            model: RoleIn,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model

        # realiza as acoes necessárias no model
        RoleAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=RoleOut
    )
    async def update(
            model: RoleIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # regras aplicáveis ao model
        RoleRegras(_id=_id, model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        RoleAcoes(_id=_id, model=model, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200
    )
    async def delete(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # regras aplicáveis ao model
        RoleRegras(_id=_id, handler=handler, regra='soft_delete')

        # realiza as acoes necessárias no model
        RoleAcoes(_id=_id, handler=handler, acao='soft_delete')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}/adiciona_sub_role",
        status_code=201,
        response_model=RoleOut
    )
    async def add_sub_role(
            model: SubRoleIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # inicia uma instancia de sessao do mongodb
        handler.sessao = Sessao()

        # regras aplicáveis ao model
        RoleRegras(_id=_id, model=model, handler=handler, regra='adiciona_sub_role')

        # realiza as acoes necessárias no model
        RoleAcoes(_id=_id, model=model, handler=handler, acao='adiciona_sub_role')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}/remove_sub_role",
        status_code=200,
        response_model=RoleOut
    )
    async def remove_sub_role(
            model: SubRoleIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # inicia uma instancia de sessao do mongodb
        handler.sessao = Sessao()
        # regras aplicáveis ao model
        RoleRegras(_id=_id, model=model, handler=handler, regra='remove_sub_role')

        # realiza as acoes necessárias no model
        RoleAcoes(_id=_id, model=model, handler=handler, acao='remove_sub_role')

        return handler.sucesso