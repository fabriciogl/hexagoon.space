#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.exceptions import HTTPException
from Model.Usuario import Usuario


class TokenExpiredException(HTTPException):

    def __init__(self):
        """
        """
        super().__init__(401, f'O token jwt está expirado.')


class TokenInvalidException(HTTPException):

    def __init__(self):
        super().__init__(401, f'Token inválido.')

