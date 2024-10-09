import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server
from prismadb import connect_prisma
from routes.user import router as user_router
from routes.estabelecimentos import router as estabelecimentos_router
from utils.endpoints.block_endpoints import BlockEndpointsMiddleware

loop = asyncio.new_event_loop()
loop.run_until_complete(connect_prisma())
app = FastAPI()

# Inicializando o estado de atualização do banco de dados
app.state.is_updating_database = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(BlockEndpointsMiddleware)

app.include_router(user_router)
app.include_router(estabelecimentos_router)

config = Config(app=app, port=8080, loop=loop)
server = Server(config=config)
loop.run_until_complete(server.serve())
