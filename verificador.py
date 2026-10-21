import csv
import requests
from datetime import datetime

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_87wFOqu4gttxm7EfHlcwCrmWYss5QJ-9FxHbyIg-vBOM4QAKHJ1YYZ2EB3GA9AZbDiZokCO86OcP/pub?output=csv"

dados = requests.get(CSV_URL, timeout=30).text

linhas = list(csv.DictReader(dados.splitlines()))

relatorio = []

relatorio.append("# Relatório Diário")
relatorio.append("")
relatorio.append(f"Gerado em: {datetime.now()}")
relatorio.append("")

for produto in linhas:

    nome = produto.get("nome", "")
    imagem = produto.get("imagem", "")
    link = produto.get("link", "")

    status_img = "OK"
    status_link = "OK"

    try:
        r = requests.get(imagem, timeout=15)
        if r.status_code != 200:
            status_img = f"ERRO ({r.status_code})"
    except Exception:
        status_img = "FALHA"

    try:
        r = requests.get(link, timeout=15, allow_redirects=True)

        if r.status_code != 200:
            status_link = f"ERRO ({r.status_code})"

    except Exception:
        status_link = "FALHA"

    relatorio.append(f"## {nome}")
    relatorio.append(f"- Imagem: {status_img}")
    relatorio.append(f"- Link: {status_link}")
    relatorio.append("")

with open("relatorio_integridade.md", "w", encoding="utf-8") as f:
    f.write("\n".join(relatorio))

print("Relatório gerado")
