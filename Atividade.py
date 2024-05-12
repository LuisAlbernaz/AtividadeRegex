import requests
import re
import csv

base_url = 'https://ulbra-to.br/ensino/professores/pagina={}'

professores = []

for pagina in range(1, 6):
    url = base_url.format(pagina)
    response = requests.get(url)

    if response.status_code == 200:
        regex_nome = r'[A-Za-zÀ-ÿ\s]+'
        nome = r'<div class="card-title fw-bold lh-1">({})</div>'
        titularidade = r'<div class="small">({})</div>'

        matches_nome = re.findall(nome.format(regex_nome), response.text)
        matches_titularidade = re.findall(titularidade.format(regex_nome), response.text)

        for nome, titularidade in zip(matches_nome, matches_titularidade):
            if nome not in [professor['Nome'] for professor in professores]:
                professores.append({'Nome': nome, 'Titularidade': titularidade})

nome_arquivo = 'professores.csv'
with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=['Nome', 'Titularidade'])
    escritor_csv.writeheader()
    escritor_csv.writerows(professores)

print(f'Os dados foram salvos no arquivo "{nome_arquivo}"')