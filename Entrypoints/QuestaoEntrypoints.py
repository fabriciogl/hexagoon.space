from fastapi import APIRouter, HTTPException

from Acoes.QuestaoAcoes import QuestaoAcoes
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Model.Questao import Questao
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository
from Validations.CustomValidations import constr

router = APIRouter(
    prefix="/questoes",
    responses={404: {"description": "Not found"}},
)

class QuestaoEntrypoints:

    @staticmethod
    @router.get("/a/{questao_id}")
    async def find_questao_assinc(questao_id: str):
        resultado = await QuestaoRepository.aprocura_um(_id=questao_id)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Questão não encontrada")
        return {"questao_id": resultado.__dict__}

    @staticmethod
    @router.get("/{questao_id}")
    async def find_questao(questao_id: constr(regex=r'^[\w\D]{3,4}$')):

        handler = ResponseHandler()
        # realiza as acoes necessárias no objeto
        QuestaoAcoes(questao_id, handler, 'find')

        return handler.resultado

    @staticmethod
    @router.put(
        "",
        tags=["custom"],
        responses={403: {"description": "Operation forbidden"}},
    )
    async def update_item(questao: Questao):

        handler = ResponseHandler()
        # realiza as acoes necessárias no objeto
        QuestaoAcoes(questao, handler, 'create')

        return handler.resultado