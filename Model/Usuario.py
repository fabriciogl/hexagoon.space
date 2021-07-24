import asyncio
from dataclasses import dataclass

from Repositorio.Mongo.MongoBasico import MongoBasico


@dataclass
class Usuario(MongoBasico):
    id: str
    nome: str
    email: str
    senha: str


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    u = Usuario(id='a76ad87', nome='Fabricio', email='f@g.com', senha='123456')


    async def rota1():
       return await u.salvar()

    async def rota2():
        return await u.deletar()

    async def main():
        result = asyncio.gather(loop.create_task(rota1()), loop.create_task(rota2()))
        print(result)

    loop.run_until_complete(main())


