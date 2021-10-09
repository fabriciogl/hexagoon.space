#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from Model.Vertice import Vertice


class VerticeCreateException(HTTPException):
    """Exceção a ser utilizada quando ocorre erro na criacao de model"""

    def __init__(self, model: Vertice):
        super().__init__(404, f'O {model.Config.title} não foi criado.')
