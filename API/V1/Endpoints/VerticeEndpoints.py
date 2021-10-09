from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Security

from API.V1.Acoes.VerticeAcoes import VerticeAcoes
from API.V1.Endpoints.Handler.ResponseHandler import ResponseHandler
from Model.Vertice import Vertice
from API.V1.Regras.VerticeRegras import VerticeRegras
from Repositorio.Mongo.VerticeRepository import VerticeRepository
from Validations.PydanticCustomValidations import constr
from Validations.TokenValidation import valida_token, valida_role

router = APIRouter(
    prefix="/vertice",
    dependencies=[Depends(valida_token)]
)

class VerticeEndpoints:

    @staticmethod
    @router.get("/a/{_id}", response_model=Vertice)
    async def find_questao_assinc(_id: str):
        vertice = await VerticeRepository.aprocura_um(_id=_id)
        if vertice is None:
            raise HTTPException(status_code=404, detail="Vértice não encontrado.")
        return vertice

    @staticmethod
    @router.get("/{id}")
    async def find(
            id: constr(regex=r'^[\w\D]{32}$'),
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # realiza as acoes necessárias no model
        VerticeAcoes(_id=id, handler=handler, acao='find')

        return handler.resultado_json

    @staticmethod
    @router.post("", response_model=Vertice)
    async def create(
            vertice: Vertice,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # valida o model
        VerticeRegras(model=vertice, handler=handler, acao='create')

        # realiza as acoes necessárias no model
        VerticeAcoes(model=vertice, handler=handler, acao='create')

        return handler.resultado_json

    @staticmethod
    @router.put("/{id}")
    async def update(vertice: Vertice, id: constr(regex=r'^[\w\D]{32}$')):

        handler = ResponseHandler()

        # regras aplicáveis ao model
        VerticeRegras(_id=id, model=vertice, handler=handler, acao='update')

        # realiza as acoes necessárias no model
        VerticeAcoes(_id=id, model=vertice, handler=handler, acao='update')

        return handler.resultado_json