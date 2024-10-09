import requests
import math
import os

def get_coordinates_from_cep(cep, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={cep},Brazil&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
        else:
            print(f"Coordenadas não encontradas para o CEP: {cep}")
            return None
    else:
        print(f"Erro na requisição para o CEP: {cep}")
        return None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

def loadCeps(file_path):
    codes = {}
    with open(file_path, 'r', encoding='latin-1') as file:
        for line in file:
            if ' - ' in line:
                parts = line.strip().split(' - ')
                if len(parts) == 3:
                    cep = parts[0].strip()
                    latitude = parts[1].strip()
                    longitude = parts[2].strip()
                    codes[cep] = (latitude, longitude)
    return codes

def find_ceps_within_distance(reference_cep, api_key, max_distance_km):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ceps = loadCeps(os.path.join(base_dir, 'ceps_bd.txt'))

    reference_coords = get_coordinates_from_cep(reference_cep, api_key)
    if not reference_coords:
        print(f"Coordenadas não encontradas para o CEP de referência: {reference_cep}")
        return []
    print(reference_cep)
    print(reference_coords)
    ref_lat, ref_lon = reference_coords
    filtered_ceps = []

    for cep, (lat, lon) in ceps.items():
        if lat != 'NULL' and lon != 'NULL':
            distance = haversine(ref_lat, ref_lon, float(lat), float(lon))
            if distance <= max_distance_km:
                filtered_ceps.append(cep)

    return filtered_ceps


## Aparentemente funciona apenas com ceps de referencia de cidades grandes.
## Buscar uma API futura que forneca as coords de todos os ceps
## ou salvar em um banco essas coordenadas
## testar a funcao
# api_key = "f3853bcd03d04d3cbd13ef68ef5f14ee"
# max_distance_km = 100
# reference_cep = "29010"
# ceps_proximos = find_ceps_within_distance(reference_cep, api_key, max_distance_km)
# print(ceps_proximos)
