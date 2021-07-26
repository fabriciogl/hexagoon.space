from Repositorio.Mongo.QuestaoRepository import QuestaoRepository
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/questoes",
    responses={404: {"description": "Not found"}},
)

@router.get("/a/{questao_id}")
async def read_item(questao_id: str):
    resultado = await QuestaoRepository.aprocura_um(_id=questao_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    return {"questao_id": resultado.__dict__}


@router.get("/s/{questao_id}")
async def read_item(questao_id: str):
    resultado = QuestaoRepository.sprocura_um(_id=questao_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    return {"questao_id": resultado}

@router.put(
    "/{questao_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(questao_id: str):
    if questao_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"questao_id": questao_id, "name": "The great Plumbus"}