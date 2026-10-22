import pandas as pd
import os
from datetime import datetime

# URL da planilha publicada como CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_87wFOqu4gttxm7EfHlcwCrmWYss5QJ-9FxHbyIg-vBOM4QAKHJ1YYZ2EB3GA9AZbDiZokCO86OcP/pub?output=csv"

# Arquivos locais
HISTORICO = "historico_precos.csv"
RELATORIO = "relatorio_integridade.md"

print("Baixando planilha...")

# Carrega dados atuais
df = pd.read_csv(CSV_URL)

print("Colunas encontradas:")
print(df.columns.tolist())

# Remove espaços extras dos nomes das colunas
df.columns = [c.strip() for c in df.columns]

print(f"Produtos encontrados: {len(df)}")

# Data da execução
agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

novos_registros = []
alteracoes = []

# Carrega histórico existente
if os.path.exists(HISTORICO):
    historico = pd.read_csv(HISTORICO)
    print(f"Histórico carregado: {len(historico)} registros")
else:
    historico = pd.DataFrame(
        columns=[
            "data",
            "nome",
            "categoria",
            "preco"
        ]
    )
    print("Histórico não encontrado. Criando novo arquivo.")

# Processa produtos
for _, row in df.iterrows():

    try:
        nome = str(row["Nome"]).strip()
        categoria = str(row["Categoria"]).strip()
        preco_atual = str(row["Preço"]).strip()

        ultimos = historico[historico["nome"] == nome]

        # Produto novo
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

        # Último preço registrado
        ultimo_preco = ultimos.iloc[-1]["preco"]

        # Compara preços
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

    except Exception as e:
        print(f"Erro ao processar produto: {e}")

# Adiciona novos registros ao histórico
if novos_registros:

    historico = pd.concat(
        [
            historico,
            pd.DataFrame(novos_registros)
        ],
        ignore_index=True
    )

    print(f"Novos registros adicionados: {len(novos_registros)}")

else:

    print("Nenhuma alteração de preço encontrada.")

# Salva histórico SEMPRE
historico.to_csv(
    HISTORICO,
    index=False,
    encoding="utf-8-sig"
)

print(f"Histórico salvo em: {HISTORICO}")

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

        f.write("✅ Nenhuma alteração de preço encontrada.\n")

print(f"Relatório gerado: {RELATORIO}")
print("Verificação concluída com sucesso.")
