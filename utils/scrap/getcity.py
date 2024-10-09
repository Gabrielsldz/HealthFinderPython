import json


def extrair_codigos_arquivo(arquivo):
    resultados = {}


    with open(arquivo, 'r', encoding='ISO-8859-1') as file:
        linhas = file.readlines()

        for linha in linhas:
            if '-' in linha:
                partes = linha.split('-')
                municipio = partes[0].strip()
                codigo_completo = partes[1].strip()
                codigo_truncado = codigo_completo[:-1]

                resultados[municipio] = codigo_truncado

    with open('../../models/municipios.json', 'w', encoding='utf-8') as json_file:
        json.dump(resultados, json_file, ensure_ascii=False, indent=4)

    print("Arquivo JSON gerado com sucesso!")

arquivo = 'codigos_municipios.txt'
extrair_codigos_arquivo(arquivo)
