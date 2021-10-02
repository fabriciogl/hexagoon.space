from fastapi import APIRouter, HTTPException

from Acoes.QuestaoAcoes import QuestaoAcoes
from Endpoints.Handler.ResponseHandler import ResponseHandler
from Model.Questao import Questao
from Regras.QuestaoRegras import QuestaoRegras
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository
from Validations.CustomValidations import constr

router = APIRouter(
    prefix="/questoes",
    responses={404: {"description": "Not found"}},
)

class QuestaoEndpoints:

    @staticmethod
    @router.get("/a/{questao_id}")
    async def find_questao_assinc(questao_id: str):
        resultado = await QuestaoRepository.aprocura_um(_id=questao_id)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Questão não encontrada")
        return {"usuario_id": resultado.__dict__}

    @staticmethod
    @router.get("/{questao_id}")
    async def find(questao_id: constr(regex=r'^[\w\D]{3,4}$')):

        handler = ResponseHandler()
        # realiza as acoes necessárias no model
        QuestaoAcoes(_id=questao_id, handler=handler, acao='find')

        return handler.resultado_json

    @staticmethod
    @router.post("")
    async def create(questao: Questao):

        handler = ResponseHandler()
        # realiza as acoes necessárias no model
        QuestaoAcoes(model=questao, handler=handler, acao='create')

        return handler.resultado_json

    @staticmethod
    @router.put("/{questao_id}")
    async def update(questao: Questao, questao_id: constr(regex=r'^[\w\D]{3,4}$')):

        handler = ResponseHandler()

        # regras aplicáveis ao model
        QuestaoRegras(_id=questao_id, model=questao, handler=handler, acao='update')

        # realiza as acoes necessárias no model
        QuestaoAcoes(_id=questao_id, model=questao, handler=handler, acao='update')

        return handler.resultado_json