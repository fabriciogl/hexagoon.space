from pydantic import Field, BaseModel

from Repositorio.Mongo.MongoBasico import MongoBasico


class Usuario(BaseModel, MongoBasico):
    nome: str
    email: str
    senha: str
    id: str = Field(..., alias='_id')



