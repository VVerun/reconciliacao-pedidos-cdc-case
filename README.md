# Reconciliacao de Pedidos - Case de Engenharia de Dados

## Objetivo

Reconstruir o estado atual dos pedidos a partir de um log de eventos (CDC - Change Data Capture), comparar esse estado com uma tabela analítica de destino e gerar um relatório de divergências entre os dois sistemas.

## Estrutura do projeto

* `main.py` — Script principal da reconciliação.
* `pedidos_origem.csv` — Histórico de eventos do sistema transacional.
* `pedidos_destino.csv` — Estado atual da tabela analítica.
* `relatorio_divergencias.csv` — Resultado da reconciliação.
* `RESUMO.md` — Resumo executivo da auditoria.
* `DECISOES.md` — Decisões, premissas, limitações e uso de IA.

## Como executar

```bash
pip install pandas numpy
python main.py
```

O script gera automaticamente o arquivo `relatorio_divergencias.csv`.
