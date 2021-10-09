from typing import Optional, List

from pydantic import Field, BaseModel, EmailStr


class Usuario(BaseModel):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    roles: Optional[List[str]]
    # Pydantic protege os campos iniciados com '_', não permite alterá-los diretamente.
    # É possível usá-los atribuindo a função PrivateAttr(), porém não funciona no modo Debug do Pycharm.
    id: Optional[str] = Field(None, alias='_id')  # álias permite importar campo_valor com nome diferente do model

    class Config:
        title = 'Usuario'