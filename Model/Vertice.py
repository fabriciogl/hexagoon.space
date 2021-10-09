# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Vertice(BaseModel):
    texto: Optional[str]
    titulo: str
    pais: Optional[List[str]]
    filhos: Optional[List[str]]
    irmaos: Optional[List[str]]
    data: Optional[datetime] = datetime.now()
    autores: Optional[List[str]] = []
    id: str = Field(None, alias='_id')  # alias, pois o Pydantic esconde campos privados

    class Config:
        title = 'Vertice'
