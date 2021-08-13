from Acoes.QuestaoAcoes import QuestaoAcoes
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Model.Questao import Questao
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/questoes",
    responses={404: {"description": "Not found"}},
)

@router.get("/a/{questao_id}")
async def find_questao_assinc(questao_id: str):
    resultado = await QuestaoRepository.aprocura_um(_id=questao_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    return {"questao_id": resultado.__dict__}


@router.get("/")
async def find_questao(questao: Questao):

    handler = ResponseHandler()
    # realiza as acoes necessárias no objeto
    QuestaoAcoes(questao, handler, 'find')

    return handler.resultado

@router.put(
    "/",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(questao: Questao):

    handler = ResponseHandler()
    # realiza as acoes necessárias no objeto
    QuestaoAcoes(questao, handler, 'create')

    return handler.resultado