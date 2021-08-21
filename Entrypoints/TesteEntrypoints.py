from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from Acoes.QuestaoAcoes import QuestaoAcoes
from Acoes.TesteAcoes import TesteAcoes
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Model.Questao import Questao
from Model.Teste import Teste
from Regras.QuestaoRegras import QuestaoRegras
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository
from Validations.CustomValidations import constr

router = APIRouter(
    prefix="/teste",
    responses={404: {"description": "Not found"}},
)

class TesteEntrypoints:

    @staticmethod
    @router.get("/{teste_id}")
    async def find(teste_id: constr(regex=r'^[\w\D]{3,4}$')):

        handler = ResponseHandler()
        # realiza as acoes necessárias no model
        QuestaoAcoes(_id=teste_id, handler=handler, acao='find')

        return handler.resultado_json

    @staticmethod
    @router.post("", response_class=HTMLResponse)
    async def create(teste: Teste, request: Request):

        handler = ResponseHandler(request)
        # realiza as acoes necessárias no model
        TesteAcoes(model=teste, handler=handler, acao='create')

        return handler.resultado_html

    @staticmethod
    @router.put("/{teste_id}")
    async def update(teste: Teste, teste_id: constr(regex=r'^[\w\D]{3,4}$')):

        handler = ResponseHandler()

        # regras aplicáveis ao model
        QuestaoRegras(_id=teste_id, model=teste, handler=handler, acao='update')

        # realiza as acoes necessárias no model
        QuestaoAcoes(_id=teste_id, model=teste, handler=handler, acao='update')

        return handler.resultado_json