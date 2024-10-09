from prisma import Prisma
from prisma.engine.errors import AlreadyConnectedError

prisma = Prisma()

async def clear_database():
    try:
        await prisma.connect()
    except AlreadyConnectedError:
        await prisma.disconnect()
        await prisma.connect()
    await prisma.estabelecimento.delete_many()
    await prisma.disconnect()
