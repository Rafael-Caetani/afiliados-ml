import json
import requests
import csv
from datetime import datetime

# headers pra não ser bloqueado pela Amazon
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0"}

with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)

relatorio = ["# Relatório de Integridade", f"_Gerado em {datetime.now():%d/%m/%Y %H:%M}_\n"]
historico_rows = []

for p in produtos:
    nome = p.get("nome")
    link = p.get("link")
    img = p.get("imagem")
    
    # 1. Checa link do produto
    try:
        r = requests.head(link, headers=HEADERS, timeout=10, allow_redirects=True)
        if r.status_code != 200:
            relatorio.append(f"- ❌ **{nome}** - Link quebrado ({r.status_code}) -> {link}")
    except Exception as e:
        relatorio.append(f"- ❌ **{nome}** - Erro ao acessar link: {e}")

    # 2. Checa imagem
    try:
        r_img = requests.head(img, headers=HEADERS, timeout=10)
        if r_img.status_code != 200:
            relatorio.append(f"- ⚠️ **{nome}** - Imagem quebrada -> {img}")
    except:
        relatorio.append(f"- ⚠️ **{nome}** - Imagem com erro")

    # 3. Guarda histórico (aqui você depois adiciona o scraping de preço)
    historico_rows.append({
        "data": datetime.now().isoformat(),
        "nome": nome,
        "preco_planilha": p.get("preco"),
        "link": link
    })

if len(relatorio) == 2:
    relatorio.append("✅ Nenhum link quebrado encontrado. Tudo OK!")

with open("relatorio_integridade.md", "w", encoding="utf-8") as f:
    f.write("\n".join(relatorio))

with open("historico_precos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["data","nome","preco_planilha","link"])
    w.writeheader()
    w.writerows(historico_rows)

print("Verificação finalizada")
