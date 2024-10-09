import json

def extrair_codigos_estados(arquivo):
    resultados = {}

    # Lendo o arquivo com codificação ISO-8859-1
    with open(arquivo, 'r', encoding='UTF-8') as file:
        linhas = file.readlines()

        for linha in linhas:
            if '-' in linha:
                partes = linha.split('-')
                estado = partes[0].strip()
                codigo_estado = partes[1].strip()

                resultados[estado] = codigo_estado

    # Salvando os resultados em um arquivo JSON
    with open('../../models/unidades.json', 'w', encoding='utf-8') as json_file:
        json.dump(resultados, json_file, ensure_ascii=False, indent=4)

    print("Arquivo JSON de estados gerado com sucesso!")

# Especifica o caminho do arquivo de entrada
arquivo = 'TiposUnidades.txt'
extrair_codigos_estados(arquivo)
