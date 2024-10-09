import requests
import asyncio
from prisma import Prisma
from prisma.engine.errors import AlreadyConnectedError
import os
from tenacity import retry, stop_after_attempt, wait_fixed

prisma = Prisma()

async def upsert_data(data):
    # Verifica se o registro já existe no banco de dados
    existing_record = await prisma.estabelecimento.find_first(
        where={'codigo_cnes': data['codigo_cnes']}
    )

    # Se existir, verifica se há diferenças nos campos
    if existing_record:
        update_data = {}
        for key, value in data.items():
            if key in existing_record and existing_record[key] != value:
                update_data[key] = value

        # Se houver dados a serem atualizados, realiza a atualização
        if update_data:
            await prisma.estabelecimento.update(
                where={'codigo_cnes': data['codigo_cnes']},
                data=update_data
            )
            print(f"Registro com código CNES {data['codigo_cnes']} atualizado. Dados divergentes: {update_data}")
        else:
            pass
            #print(f"Registro com código CNES {data['codigo_cnes']} já está atualizado. Nenhuma divergência encontrada.")
    else:
        # Se não existir, insere o novo registro
        await prisma.estabelecimento.create(
            data=data
        )
        print(f"Novo registro inserido com código CNES {data['codigo_cnes']}.")

def load_codes(file_path):
    codes = {}
    with open(file_path, 'r', encoding='latin-1') as file:
        for line in file:
            if ' - ' in line:
                name, code = line.strip().rsplit(' - ', 1)
                codes[name] = code
    return codes

base_dir = os.path.dirname(os.path.abspath(__file__))
state_codes = load_codes(os.path.join(base_dir, 'codigos_estados.txt'))
unit_types = load_codes(os.path.join(base_dir, 'TiposUnidades.txt'))

headers = {
    'accept': 'application/json',
}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_establishments(params, headers):
    response = requests.get('https://apidadosabertos.saude.gov.br/cnes/estabelecimentos', params=params, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

async def get_and_populate_establishments():
    try:
        await prisma.connect()
    except AlreadyConnectedError:
        await prisma.disconnect()
        await prisma.connect()

    for state, state_code in state_codes.items():
        print('Coletando e populando dados de: ', state)
        for unit, unit_code in unit_types.items():
            params = {
                'codigo_tipo_unidade': unit_code,
                'codigo_uf': state_code,
                'status': '1',
                'limit': '20',
                'offset': '50',
            }

            try:
                response_data = fetch_establishments(params, headers)
                if response_data.get('estabelecimentos'):
                    for estabelecimento in response_data['estabelecimentos']:
                        await upsert_data(estabelecimento)
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch data for state {state} and unit {unit}: {e}")

    await prisma.disconnect()

# asyncio.run(get_and_populate_establishments())