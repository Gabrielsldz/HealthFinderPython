from fastapi import APIRouter, Request, HTTPException
from prisma import Prisma
from prisma.errors import PrismaError
from typing import Dict, Any, List
from models.ceprequest import CepRequest
from utils.local import find_ceps_within_distance
from models.cityrequest import CityRequest
import json
from jwt import decode, InvalidTokenError
from utils.access_token import validate_token
from unidecode import unidecode
from models.staterequest import stateRequest
from models.namerequest import nameRequest
from utils.fuzzymatch import fuzzy_match

router = APIRouter(prefix='/establishments')

prisma = Prisma()
## Por isso daqui numa DB futuramente
with open('models/municipios.json', 'r', encoding='utf-8') as f:
    municipios_data = json.load(f)
with open('models/estados.json', 'r', encoding='utf-8') as f:
    estados_data = json.load(f)
@router.post('/get_establishments')
async def get_establishments(request: Request):
    search_params: Dict[str, Any] = await request.json()

    if 'codigo_tipo_unidade' not in search_params or 'codigo_uf' not in search_params:
        raise HTTPException(status_code=400, detail="Parametros 'codigo_tipo_unidade' e 'codigo_uf' são obrigatórios")

    try:
        codigo_tipo_unidade = int(search_params['codigo_tipo_unidade'])
        codigo_uf = int(search_params['codigo_uf'])

    except ValueError:
        raise HTTPException(status_code=400, detail="Parametros 'codigo_tipo_unidade' e 'codigo_uf' devem ser números inteiros")

    try:
        await prisma.connect()

        estabelecimentos = await prisma.estabelecimento.find_many(
            where={
                'codigo_tipo_unidade': codigo_tipo_unidade,
                'codigo_uf': codigo_uf
            }
        )

        if not estabelecimentos:
            raise HTTPException(status_code=404, detail="Nenhum estabelecimento encontrado")

        resultado: List[Dict[str, Any]] = []
        for estabelecimento in estabelecimentos:
            resultado.append({
                'nome_razao_social': estabelecimento.nome_razao_social,
                'nome_fantasia': estabelecimento.nome_fantasia,
                'codigo_cep_estabelecimento': estabelecimento.codigo_cep_estabelecimento,
                'endereco_estabelecimento': estabelecimento.endereco_estabelecimento,
                'numero_estabelecimento': estabelecimento.numero_estabelecimento,
                'bairro_estabelecimento': estabelecimento.bairro_estabelecimento,
                'numero_telefone_estabelecimento': estabelecimento.numero_telefone_estabelecimento,
                'descricao_turno_atendimento': estabelecimento.descricao_turno_atendimento,
                'estabelecimento_faz_atendimento_ambulatorial_sus': estabelecimento.estabelecimento_faz_atendimento_ambulatorial_sus,
            })

        return resultado

    except PrismaError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

    finally:
        await prisma.disconnect()

@router.post("/new_get_establishments")
async def new_get_establishments(request:Request):
    search_params: Dict[str, Any] = await request.json();
    pass

# @router.post('/search_by_cep')
# async def search_by_cep(cep_request: CepRequest):
#     try:
#         api_key = "f3853bcd03d04d3cbd13ef68ef5f14ee"
#         max_distance_km = cep_request.distance
#         reference_cep = cep_request.cep
#
#
#         ceps_proximos = find_ceps_within_distance(reference_cep, api_key, max_distance_km)
#
#         if not ceps_proximos:
#             raise HTTPException(status_code=404, detail="Nenhum CEP encontrado dentro da distância especificada.")
#
#         await prisma.connect()
#
#         estabelecimentos = await prisma.estabelecimento.find_many(
#             where={
#                 'codigo_cep_estabelecimento': {
#                     'in': ceps_proximos
#                 }
#             }
#         )
#
#         if not estabelecimentos:
#             raise HTTPException(status_code=404, detail="Nenhum estabelecimento encontrado para os CEPs próximos.")
#
#         resultado: List[Dict[str, Any]] = []
#         for estabelecimento in estabelecimentos:
#             resultado.append({
#                 'nome_razao_social': estabelecimento.nome_razao_social,
#                 'nome_fantasia': estabelecimento.nome_fantasia,
#                 'codigo_cep_estabelecimento': estabelecimento.codigo_cep_estabelecimento,
#                 'endereco_estabelecimento': estabelecimento.endereco_estabelecimento,
#                 'numero_estabelecimento': estabelecimento.numero_estabelecimento,
#                 'bairro_estabelecimento': estabelecimento.bairro_estabelecimento,
#                 'numero_telefone_estabelecimento': estabelecimento.numero_telefone_estabelecimento,
#                 'descricao_turno_atendimento': estabelecimento.descricao_turno_atendimento,
#                 'estabelecimento_faz_atendimento_ambulatorial_sus': estabelecimento.estabelecimento_faz_atendimento_ambulatorial_sus,
#             })
#
#         return resultado
#
#     except PrismaError as e:
#         raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
#
#     finally:
#         await prisma.disconnect()




# Busca por cep finalizada, apenas acrescentar tratamentos de erros futuramente.
@router.post('/search_by_cep')
async def search_by_cep(cep_request: CepRequest, request: Request):
    try:
        # Validar o token
        token = validate_token(request.headers)
        if not token:
            raise HTTPException(status_code=401, detail="Token inválido ou ausente")

        user_id = decode(token, "secret_key", algorithms=['HS256'])['sub']  # Decodificar o token para obter o user_id

        api_key = "f3853bcd03d04d3cbd13ef68ef5f14ee"
        max_distance_km = cep_request.distance
        reference_cep = cep_request.cep
        tipo_estabelecimento = cep_request.tipo_estabelecimento
        ceps_proximos = find_ceps_within_distance(reference_cep, api_key, max_distance_km)

        if not ceps_proximos:
            raise HTTPException(status_code=404, detail="Nenhum CEP encontrado dentro da distância especificada.")

        await prisma.connect()

        # Condição para aplicar ou não o filtro de tipo_estabelecimento
        if tipo_estabelecimento is not None:
            estabelecimentos = await prisma.estabelecimento.find_many(
                where={
                    'codigo_cep_estabelecimento': {
                        'in': ceps_proximos
                    },
                    'codigo_tipo_unidade': tipo_estabelecimento
                }
            )
        else:
            estabelecimentos = await prisma.estabelecimento.find_many(
                where={
                    'codigo_cep_estabelecimento': {
                        'in': ceps_proximos
                    }
                }
            )

        if not estabelecimentos:
            raise HTTPException(status_code=404, detail="Nenhum estabelecimento encontrado para os CEPs próximos.")

        resultado: List[Dict[str, Any]] = []
        for estabelecimento in estabelecimentos:
            resultado.append({
                'nome_razao_social': estabelecimento.nome_razao_social,
                'nome_fantasia': estabelecimento.nome_fantasia,
                'codigo_cep_estabelecimento': estabelecimento.codigo_cep_estabelecimento,
                'endereco_estabelecimento': estabelecimento.endereco_estabelecimento,
                'numero_estabelecimento': estabelecimento.numero_estabelecimento,
                'bairro_estabelecimento': estabelecimento.bairro_estabelecimento,
                'numero_telefone_estabelecimento': estabelecimento.numero_telefone_estabelecimento,
                'descricao_turno_atendimento': estabelecimento.descricao_turno_atendimento,
                'estabelecimento_faz_atendimento_ambulatorial_sus': estabelecimento.estabelecimento_faz_atendimento_ambulatorial_sus,
            })

        return resultado

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except PrismaError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
    finally:
        await prisma.disconnect()




## Implementar tambem a distancia na busca por cidade
@router.post("/search_by_city")
async def search_by_city(city_request: CityRequest, request: Request):
    city_name = unidecode(city_request.city.lower())

    normalized_municipios = {unidecode(city.lower()): code for city, code in municipios_data.items()}

    if city_name in normalized_municipios:
        codigo_municipio = normalized_municipios[city_name]

        try:
            await prisma.connect()

            if city_request.tipo_estabelecimento is not None:
                estabelecimentos = await prisma.estabelecimento.find_many(
                    where={
                        "codigo_municipio": int(codigo_municipio),
                        "codigo_tipo_unidade": city_request.tipo_estabelecimento
                    }
                )
            else:
                estabelecimentos = await prisma.estabelecimento.find_many(
                    where={
                        "codigo_municipio": int(codigo_municipio)
                    }
                )

            if estabelecimentos:
                resultado: List[Dict[str, Any]] = []
                for estabelecimento in estabelecimentos:
                    resultado.append({
                        'nome_razao_social': estabelecimento.nome_razao_social,
                        'nome_fantasia': estabelecimento.nome_fantasia,
                        'codigo_cep_estabelecimento': estabelecimento.codigo_cep_estabelecimento,
                        'endereco_estabelecimento': estabelecimento.endereco_estabelecimento,
                        'numero_estabelecimento': estabelecimento.numero_estabelecimento,
                        'bairro_estabelecimento': estabelecimento.bairro_estabelecimento,
                        'numero_telefone_estabelecimento': estabelecimento.numero_telefone_estabelecimento,
                        'descricao_turno_atendimento': estabelecimento.descricao_turno_atendimento,
                        'estabelecimento_faz_atendimento_ambulatorial_sus': estabelecimento.estabelecimento_faz_atendimento_ambulatorial_sus,
                    })
                return resultado
            else:
                raise HTTPException(status_code=404, detail="Nenhum estabelecimento encontrado para essa cidade")

        except PrismaError as e:
            raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

        finally:
            await prisma.disconnect()

    else:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")



@router.post("/search_by_state")
async def search_by_state(StateRequest: stateRequest, request: Request):
    token = validate_token(request.headers)
    if not token:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    state_name = unidecode(StateRequest.state.lower())

    normalized_state = {unidecode(state_name.lower()): code for state_name, code in estados_data.items()}

    if state_name in normalized_state:
        codigo_state = normalized_state[state_name]
        print(codigo_state)
        print(type(codigo_state))

        try:
            await prisma.connect()

            # estabelecimentos = await prisma.estabelecimento.find_many(
            #     where={
            #         "codigo_uf": {
            #             "gt": 0
            #
            #         }
            #     }
            # )
            # print(estabelecimentos)
            codigo_estabelecimento = StateRequest.tipo_estabelecimento
            estabelecimentos = await prisma.estabelecimento.find_many(
                where={
                    "codigo_uf": int(codigo_state),
                    "codigo_tipo_unidade": codigo_estabelecimento
                }
            )

            if estabelecimentos:
                resultado: List[Dict[str, Any]] = []
                for estabelecimento in estabelecimentos:
                    resultado.append({
                    'nome_razao_social': estabelecimento.nome_razao_social,
                    'nome_fantasia': estabelecimento.nome_fantasia,
                    'codigo_cep_estabelecimento': estabelecimento.codigo_cep_estabelecimento,
                    'endereco_estabelecimento': estabelecimento.endereco_estabelecimento,
                    'numero_estabelecimento': estabelecimento.numero_estabelecimento,
                    'bairro_estabelecimento': estabelecimento.bairro_estabelecimento,
                    'numero_telefone_estabelecimento': estabelecimento.numero_telefone_estabelecimento,
                    'descricao_turno_atendimento': estabelecimento.descricao_turno_atendimento,
                    'estabelecimento_faz_atendimento_ambulatorial_sus': estabelecimento.estabelecimento_faz_atendimento_ambulatorial_sus,
                })
                return resultado
            else:
                raise HTTPException(status_code=404, detail="No establishments found for this state")

        except PrismaError as e:
            raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

        finally:
            await prisma.disconnect()


@router.get("/search_by_name")
async def search_by_name(name_request: nameRequest, request: Request):
    # token = validate_token(request.headers)
    # if not token:
    #     raise HTTPException(status_code=401, detail="Token inválido ou ausente")

    search_name = name_request.name.lower()
    await prisma.connect()
    # Busque os registros do banco de dados (supondo que você use Prisma ORM)
    establishments = await prisma.estabelecimento.find_many()

    # Defina um limiar de similaridade (ajustável conforme necessidade)
    similarity_threshold = 100  # O valor vai de 0 a 100, quanto maior, mais estrita a correspondência

    # Filtro por similaridade fuzzy
    results = []
    for establishment in establishments:
        nome_razao_social = establishment.nome_razao_social.lower() if establishment.nome_razao_social else ""
        nome_fantasia = establishment.nome_fantasia.lower() if establishment.nome_fantasia else ""

        # Verifica a similaridade fuzzy com `nome_razao_social` ou `nome_fantasia`
        razao_similarity = fuzzy_match(search_name, nome_razao_social)
        fantasia_similarity = fuzzy_match(search_name, nome_fantasia)

        if razao_similarity >= similarity_threshold or fantasia_similarity >= similarity_threshold:
            results.append({
                "nome_razao_social": establishment.nome_razao_social,
                "nome_fantasia": establishment.nome_fantasia,
                "similarity_razao": razao_similarity,
                "similarity_fantasia": fantasia_similarity
            })
    await prisma.disconnect()
    if not results:
        raise HTTPException(status_code=404, detail="Nenhum estabelecimento encontrado")

    return {"results": results}