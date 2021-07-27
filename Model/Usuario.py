from typing import Optional

from pydantic import Field, BaseModel, EmailStr, PrivateAttr

from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


class Usuario(BaseModel, MongoBasico):
    nome: str
    email: EmailStr
    senha: str
    # Pydantic protege os campos iniciados com '_', não permite alterá-los diretamente.
    # É possível usá-los atribuindo a função PrivateAttr(), porém não funciona no modo Debug do Pycharm.
    id: Optional[str] = Field(..., alias='_id') # álias permite importar campo com nome diferente do objeto



