from fastapi import APIRouter, HTTPException

from Acoes.UsuarioAcoes import UsuarioAcoes
from Entrypoints.Handler.EntrypointHandler import EntrypointHandler
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

        # valida as regras necessárias no objeto

        # realiza as acoes necessárias no objeto
        UsuarioAcoes(usuario, 'create')

        # conclui as operacoes no banco
        resultado = MongoBasico.comitar()

        if resultado is None:
            raise HTTPException(status_code=404, detail="Erro ao salvar o objeto.")
        return {"resultado": resultado[0].bulk_api_result}
