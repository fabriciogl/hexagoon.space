#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.exceptions import HTTPException


class ModalidadeArtigoRegrasException(HTTPException):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)


class ModalidadeArtigoCreateException(HTTPException):

    def __init__(self, msg: str):

        super().__init__(422, msg)



class ModalidadeArtigoUpdateException(HTTPException):

    def __init__(self, msg: str):
        super().__init__(422, msg)
