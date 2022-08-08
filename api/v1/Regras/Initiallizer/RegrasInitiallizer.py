import inspect
import re
from abc import ABC
from typing import Callable, Union, Optional

from pydantic import BaseModel

from api.V1.Endpoints.Handler.ResponseHandler import ResponseHandler


class RegrasInitiallizer(ABC):
    """ classe que contém o construtor das classes do tipo Regra"""

    def __init__(self, handler: ResponseHandler, acao: str, model: BaseModel = None, _id: Optional[str] = None):
        """
        contrutor a ser herdado por toda classe do tipo Regra
        Args:
            _id:
            model:
            handler:
            acao:
        """
        self._id = _id
        self.model = model
        self.handler = handler

        method: Callable[[Union[str, BaseModel], ResponseHandler], None]
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            use_cases: re.Match = re.search(r'(?P<use>uso\s{,4}[:=]{1,2}\s{,4}\[.*])', method.__doc__, flags=re.IGNORECASE)
            if handler.resultado_json:
                break
            elif use_cases and acao in use_cases.group():
                method()
            else:
                continue
