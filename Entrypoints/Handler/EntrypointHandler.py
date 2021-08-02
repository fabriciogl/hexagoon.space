# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Any, Optional

from pydantic import BaseModel
from Entrypoints.Handler.ResponseHandler import ResponseHandler


class EntrypointHandler():

    model: Optional[str] = None
    id: Optional[str] = None
    response: ResponseHandler = ResponseHandler()


