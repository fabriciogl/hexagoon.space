from fastapi import APIRouter

from Acoes.UsuarioAcoes import UsuarioAcoes
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Model.Usuario import Usuario
from Validations.CustomValidations import constr

router = APIRouter(
    prefix="/usuarios",
    responses={404: {"Descrição": "Não Encontrado"}},
)


class UsuarioEntrypoints:

    @staticmethod
    @router.get("/{usuario_id}")
    async def find(usuario_id: constr(regex=r'^[\w\D]{3,400}$')):
        handler = ResponseHandler()
        # realiza as acoes necessárias no model
        UsuarioAcoes(usuario_id, handler, 'find')

        return handler.resultado

    @staticmethod
    @router.post("")
    async def create(usuario: Usuario):

        handler = ResponseHandler()
        # valida as regras necessárias no model

        # realiza as acoes necessárias no model
        UsuarioAcoes(model=usuario, handler=handler, acao='create')

        return handler.resultado
