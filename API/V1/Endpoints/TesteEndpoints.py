from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from API.V1.Acoes.QuestaoAcoes import QuestaoAcoes
from API.V1.Acoes.TesteAcoes import TesteAcoes
from API.V1.Endpoints.Handler.ResponseHandler import ResponseHandler
from Model.Teste import Teste
from API.V1.Regras.QuestaoRegras import QuestaoRegras
from API.V1.Regras.TesteRegras import TesteRegras
from Validations.PydanticCustomValidations import constr

router = APIRouter(
    prefix="/teste",
    responses={404: {"description": "Not found"}},
)

class TesteEndpoints:

    @staticmethod
    @router.get("/{teste_id}")
    async def find(teste_id: str, request: Request):

        handler = ResponseHandler(request)
        # realiza as acoes necessárias no model
        TesteAcoes(_id=teste_id, handler=handler, acao='find')

        return handler.resultado_html

    @staticmethod
    @router.post("", response_class=HTMLResponse)
    async def create(teste: Teste, request: Request):

        handler = ResponseHandler(request)
        # regras de validação do teste
        TesteRegras(model=teste, handler=handler, acao='create')
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