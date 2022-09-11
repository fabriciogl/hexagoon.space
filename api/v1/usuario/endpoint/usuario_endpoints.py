#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.usuario.acoes.usuario_acoes import UsuarioAcoes
from api.v1.usuario.model.usuario_model import Usuario, UsuarioHandlerToken, UsuarioIn, UsuarioOut, UsuarioRoleIn, \
    UsuarioSoftDeletedOut
from api.v1.usuario.regras.usuario_regras import UsuarioRegras
from banco_dados.mongodb.configuracao.MongoConection import Sessao
from recursos.basic_exceptions.excecao_model import Message
from recursos.response_handler import ResponseHandler
from recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/usuario",
    responses={404: {"model": Message}, 405: {"model": Message}, 401: {"model": Message}},
    tags=['Usuário']
)


class UsuarioEndpoints:

    @staticmethod
    @router.get("/{id}",
                response_model=UsuarioOut
                )
    async def find(
            id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # realiza as rules necessárias no model
        UsuarioRegras(_id=id, handler=handler, regra='find')
        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=id, handler=handler, acao='find')

        return handler.sucesso
    # O response_model_exclude funciona somente para a resposta do request, mas não para a documentação

    @staticmethod
    @router.post("",
                 response_model=UsuarioHandlerToken,
                 status_code=201)
    async def create(
            usuario: Usuario,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        UsuarioRegras(model=usuario, handler=handler, regra='create')
        # realiza as acoes necessárias no model
        UsuarioAcoes(model=usuario, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put("/{_id}",
                response_model=UsuarioHandlerToken,
                status_code=200
                )
    async def update(
            usuario: UsuarioIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, model=usuario, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, model=usuario, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200,
        response_model=UsuarioSoftDeletedOut
    )
    async def delete(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):

        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, handler=handler, regra='soft_delete')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, handler=handler, acao='soft_delete')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}/inactivate",
        status_code=200
    )
    async def inactivate(
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):

        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, handler=handler, regra='inactivate')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, handler=handler, acao='inactivate')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}/adiciona_role",
        response_model=UsuarioOut,
        status_code=200
    )
    async def adiciona_role(
            usuario: UsuarioRoleIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # inicia uma instancia de sessao do mongodb
        handler.sessao = Sessao()

        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, model=usuario, handler=handler, regra='adiciona_role')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, model=usuario, handler=handler, acao='adiciona_role')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}/remove_role",
        response_model=UsuarioOut,
        status_code=200
    )
    async def adiciona_role(
            usuario: UsuarioRoleIn,
            _id: str,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # inicia uma instancia de sessao do mongodb
        handler.sessao = Sessao()

        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, model=usuario, handler=handler, regra='remove_role')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, model=usuario, handler=handler, acao='remove_role')

        return handler.sucesso


