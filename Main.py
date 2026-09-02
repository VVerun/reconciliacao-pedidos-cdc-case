import pandas as pd
import numpy as np

# 1. Leitura dos dados brutos com deduplicação (Garante Idempotência)
df_origem = pd.read_csv("pedidos_origem.csv").drop_duplicates(
    subset=[
        "id_pedido",
        "id_cliente",
        "status",
        "valor_total",
        "atualizado_em",
        "operacao"
    ]
)

df_destino = pd.read_csv("pedidos_destino.csv").drop_duplicates()

# 2. Padronização de texto e tratamento seguro das datas
df_origem["status"] = df_origem["status"].str.strip().str.upper()
df_destino["status"] = df_destino["status"].str.strip().str.upper()

df_origem["atualizado_em"] = (
    pd.to_datetime(df_origem["atualizado_em"], format="mixed")
    .dt.tz_localize(None)
)

df_destino["atualizado_em"] = (
    pd.to_datetime(df_destino["atualizado_em"], format="mixed")
    .dt.tz_localize(None)
)

# 3. Prioridade das operações para desempatar eventos no mesmo timestamp
prioridade = {"I": 1, "U": 2, "D": 3}
df_origem["prioridade_operacao"] = df_origem["operacao"].map(prioridade)

# 4. Ordenação cronológica e reconstrução dos eventos parciais (Forward Fill)
df_origem = df_origem.sort_values(
    by=["id_pedido", "atualizado_em", "prioridade_operacao"]
)

colunas_ffill = ["id_cliente", "status", "valor_total"]

df_origem[colunas_ffill] = (
    df_origem.groupby("id_pedido")[colunas_ffill].ffill()
)

# 5. Extração do estado final real usando .tail(1)
df_real = (
    df_origem.groupby("id_pedido", as_index=False)
    .tail(1)
    .reset_index(drop=True)
)

# Validações de integridade estrutural
assert df_real["id_pedido"].is_unique, (
    "Erro: Existem IDs de pedido duplicados no estado real!"
)

assert not df_real["atualizado_em"].isna().any(), (
    "Erro: Existem datas nulas no estado real!"
)

# 6. Cruzamento total (Full Outer Join) entre origem reconstruída e destino
df_cruzamento = pd.merge(
    df_real,
    df_destino,
    on="id_pedido",
    how="outer",
    suffixes=("_origem", "_destino"),
    indicator=True
)

# 7. Matriz de regras (Lógica CASE WHEN vetorizada)
condicoes = [
    (df_cruzamento["_merge"] == "left_only")
    & (df_cruzamento["operacao"] == "D"),

    (df_cruzamento["_merge"] == "left_only")
    & (df_cruzamento["operacao"] != "D"),

    (df_cruzamento["_merge"] == "right_only"),

    (df_cruzamento["_merge"] == "both")
    & (
        df_cruzamento["valor_total_origem"].round(2)
        != df_cruzamento["valor_total_destino"].round(2)
    )
    & (
        df_cruzamento["status_origem"]
        != df_cruzamento["status_destino"]
    ),

    (df_cruzamento["_merge"] == "both")
    & (
        df_cruzamento["valor_total_origem"].round(2)
        != df_cruzamento["valor_total_destino"].round(2)
    ),

    (df_cruzamento["_merge"] == "both")
    & (
        df_cruzamento["status_origem"]
        != df_cruzamento["status_destino"]
    )
]

resultados = [
    "Correto - Deletado",
    "Pedido Faltante no Destino",
    "Pedido Fantasma",
    "Divergencia de Valor e Status",
    "Divergencia de Valor",
    "Divergencia de Status"
]

df_cruzamento["tipo_divergencia"] = np.select(
    condicoes,
    resultados,
    default="Sem Divergencia"
)

# 8. Filtro exclusivo para erros reais
df_erros = df_cruzamento[
    ~df_cruzamento["tipo_divergencia"].isin(
        ["Sem Divergencia", "Correto - Deletado"]
    )
].copy()

# 9. Estruturação do relatório final
df_relatorio = df_erros[
    [
        "id_pedido",
        "tipo_divergencia",
        "status_origem",
        "status_destino",
        "valor_total_origem",
        "valor_total_destino"
    ]
].copy()

df_relatorio.columns = [
    "id_pedido",
    "tipo_divergencia",
    "status_origem",
    "status_destino",
    "valor_origem",
    "valor_destino"
]

# 10. Prints de validação para o terminal
print("\n=== VALIDAÇÃO DE ENGENHARIA ===")
print(f"Linhas na Origem após deduplicação: {len(df_origem)}")
print(f"Linhas no Destino: {len(df_destino)}")
print(f"Pedidos Únicos Reconstruídos: {len(df_real)}")

print("\n=== CLASSIFICAÇÃO GERAL DE TODOS OS PEDIDOS ===")
print(df_cruzamento["tipo_divergencia"].value_counts())

print("\n=== TOTAL DE ERROS REAIS SEPARADOS PARA O RELATÓRIO ===")
print(df_erros["tipo_divergencia"].value_counts())
print(f"Total de pedidos divergentes: {len(df_erros)}")

# 11. Exportação do resultado em CSV
df_relatorio.to_csv("relatorio_divergencias.csv", index=False)