from typing import Optional

from pydantic import Field, BaseModel

from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


class Usuario(BaseModel, MongoBasico):
    nome: str
    email: str
    senha: str
    id: Optional[str] = Field(..., alias='_id')



