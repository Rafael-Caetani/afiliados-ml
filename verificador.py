name: Verificar Produtos

on:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  verificar:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Configurar Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.11"

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Executar verificador
        run: |
          python verificador.py

      - name: Commit arquivos
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          # Garante que os arquivos existem antes de adicionar
          touch relatorio_integridade.md historico_precos.csv
          git add relatorio_integridade.md historico_precos.csv

          if git diff --staged --quiet; then
            echo "Sem alteracoes"
            exit 0
          fi

          git commit -m "Atualizacao automatica"
          git pull --rebase origin main
          git push
