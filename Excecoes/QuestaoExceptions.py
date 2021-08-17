#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from Model.Questao import Questao


class QuestaoCreateException(HTTPException):
    """Exceção a ser utilizada quando ocorre erro na criacao de model"""

    def __init__(self, model: Questao, msg: str):
        """

        Args:
            model_name: string do nome do model
            i:  identificação do model
        """
        print(msg)
        super().__init__(404, f'A {type(model).__name__} não foi criado.')
