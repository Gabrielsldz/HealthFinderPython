from utils.scrap.populateDatabase import get_and_populate_establishments

async def update_database(request):
    request.app.state.is_updating_database = True
    try:
        print('Atualizando banco de dados...')
        await get_and_populate_establishments()
        print('Banco de dados atualizado com sucesso!')
    finally:
        request.app.state.is_updating_database = False
        print('Atualização do banco de dados finalizada')