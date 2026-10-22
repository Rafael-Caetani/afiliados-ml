import pandas as pd
import os
from datetime import datetime

# URL da sua planilha publicada
CSV_URL = "COLE_AQUI_O_LINK_CSV"

# Arquivos locais
HISTORICO = "historico_precos.csv"
RELATORIO = "relatorio_integridade.md"

# Carrega dados atuais
df = pd.read_csv(CSV_URL)

# Padroniza nomes das colunas
df.columns = [c.strip() for c in df.columns]

# Estrutura esperada da planilha
# Nome | Imagem | Preco | Link | Categoria

agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

novos_registros = []
alteracoes = []

# Carrega histórico existente
if os.path.exists(HISTORICO):
    historico = pd.read_csv(HISTORICO)
else:
    historico = pd.DataFrame(
        columns=[
            "data",
            "nome",
            "categoria",
            "preco"
        ]
    )

for _, row in df.iterrows():

    nome = str(row["Nome"]).strip()
    categoria = str(row["Categoria"]).strip()

    preco_atual = str(row["Preço"]).strip()

    ultimos = historico[historico["nome"] == nome]

    if len(ultimos) == 0:

        novos_registros.append({
            "data": agora,
            "nome": nome,
            "categoria": categoria,
            "preco": preco_atual
        })

        alteracoes.append(
            f"🆕 Produto novo: {nome} ({preco_atual})"
        )

        continue

    ultimo_preco = (
        ultimos.iloc[-1]["preco"]
    )

    if str(ultimo_preco) != preco_atual:

        novos_registros.append({
            "data": agora,
            "nome": nome,
            "categoria": categoria,
            "preco": preco_atual
        })

        alteracoes.append(
            f"💰 Alteração de preço: {nome} | {ultimo_preco} → {preco_atual}"
        )

# Atualiza histórico
if novos_registros:

    historico = pd.concat(
        [
            historico,
            pd.DataFrame(novos_registros)
        ],
        ignore_index=True
    )

    historico.to_csv(
        HISTORICO,
        index=False,
        encoding="utf-8-sig"
    )

# Gera relatório
with open(
    RELATORIO,
    "w",
    encoding="utf-8"
) as f:

    f.write("# Relatório de Integridade\n\n")
    f.write(f"Gerado em: {agora}\n\n")

    if alteracoes:

        f.write("## Alterações Encontradas\n\n")

        for item in alteracoes:
            f.write(f"- {item}\n")

    else:

        f.write(
            "✅ Nenhuma alteração de preço encontrada.\n"
        )

print("Verificação concluída.")
