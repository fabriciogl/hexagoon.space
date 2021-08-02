from fastapi import APIRouter, HTTPException

from Acoes.UsuarioAcoes import UsuarioAcoes
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico

router = APIRouter(
    prefix="/usuarios",
    responses={404: {"Descrição": "Não Encontrado"}},
)


class UsuarioEntrypoints:

    @router.get("/{usuario_id}")
    async def find(usuario_id: str):

        handler = ResponseHandler()
        # realiza as acoes necessárias no objeto
        UsuarioAcoes(usuario_id, handler, 'find')

        return handler.resultado

    @router.post("/")
    async def create(usuario: Usuario):

        handler = ResponseHandler()
        # valida as regras necessárias no objeto

        # realiza as acoes necessárias no objeto
        UsuarioAcoes(usuario, handler, 'create')

        return handler.resultado
