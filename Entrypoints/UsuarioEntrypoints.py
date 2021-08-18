from fastapi import APIRouter

from Acoes.UsuarioAcoes import UsuarioAcoes
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Model.Usuario import Usuario
from Regras.UsuarioRegras import UsuarioRegras
from Validations.CustomValidations import constr

router = APIRouter(
    prefix="/usuarios",
    responses={404: {"Descrição": "Não Encontrado"}},
)


class UsuarioEntrypoints:

    @staticmethod
    @router.get("/{usuario_id}")
    async def find(usuario_id: constr(regex=r'^[a-f\d]{16}U$')):
        handler = ResponseHandler()
        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=usuario_id, handler=handler, acao='find')

        return handler.resultado

    @staticmethod
    @router.post("")
    async def create(usuario: Usuario):

        handler = ResponseHandler()
        # valida as regras necessárias no model

        # realiza as acoes necessárias no model
        UsuarioAcoes(model=usuario, handler=handler, acao='create')

        return handler.resultado

    @staticmethod
    @router.put("/{usuario_id}")
    async def update(usuario: Usuario, usuario_id: constr(regex=r'^[a-f\d]{16}U$')):

        handler = ResponseHandler()

        # regras aplicáveis ao model
        UsuarioRegras(_id=usuario_id, model=usuario, handler=handler, acao='update')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=usuario_id, model=usuario, handler=handler, acao='update')

        return handler.resultado
