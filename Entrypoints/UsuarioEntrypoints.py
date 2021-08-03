import gc

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

    @staticmethod
    @router.get("/{usuario_id}")
    async def find(usuario_id: str):
        handler = ResponseHandler()
        # realiza as acoes necessárias no objeto
        UsuarioAcoes(usuario_id, handler, 'find')

        return handler.resultado

    @staticmethod
    @router.post("/")
    async def create():

        handler = ResponseHandler()
        # valida as regras necessárias no objeto

        usuario = Usuario(_id=str(1),
                          nome=f'Fabricio',
                          email=f'fa_gatto7@gmail.com',
                          senha="fdasdfasdf")

        # realiza as acoes necessárias no objeto
        UsuarioAcoes(usuario, handler, 'create')

        return handler.resultado
