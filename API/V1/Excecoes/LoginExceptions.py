#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.exceptions import HTTPException
from Model.Usuario import Usuario


class LoginException(HTTPException):

    def __init__(self):
        super().__init__(405, f'Falha de autenticação.')
