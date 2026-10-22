import pandas as pd

url = "CSV_PUBLICO"

df = pd.read_csv(url)

produtos = []

for _, row in df.iterrows():
    produtos.append({
        "nome": row["Nome"],
        "categoria": row["Categoria"],
        "preco": row["Preço"],
        "imagem": row["Imagem"],
        "link": row["Link"]
    })

import json

with open("produtos.json", "w", encoding="utf-8") as f:
    json.dump(produtos, f, ensure_ascii=False, indent=2)
