"""ClearBank — versão alternativa com pandas (requisito opcional RO1).

Lê o transacoes.csv com pd.read_csv(), aplica as mesmas regras de validação do
notebook, agrupa por mês com groupby e compara o resultado com o relatorio.json
gerado pela solução nativa (desafio-final.ipynb). Execute o notebook antes.

Uso: python analise_pandas.py   (ou, no notebook: %run analise_pandas.py)
"""
import json
import math

import pandas as pd

LIMITE_SUSPEITO = 10000.00
ARQUIVO_CSV = "transacoes.csv"
ARQUIVO_JSON = "relatorio.json"


def ler_e_validar(caminho=ARQUIVO_CSV):
    """Lê o CSV e devolve (DataFrame só com as linhas válidas, total de linhas lidas)."""
    # dtype=str + keep_default_na=False: tudo chega como texto, igual ao csv.DictReader
    bruto = pd.read_csv(caminho, dtype=str, keep_default_na=False).fillna("")
    texto = bruto.apply(lambda coluna: coluna.str.strip())
    data = pd.to_datetime(texto["data"], format="%Y-%m-%d", errors="coerce")
    valor = pd.to_numeric(texto["valor"], errors="coerce")  # "abc" e "1500,00" viram NaN
    valida = (
        texto["id"].str.fullmatch(r"[+-]?\d+")  # id não vazio e inteiro
        & (texto["cliente_id"] != "")
        & data.notna() & (texto["data"].str.len() == 10)  # mesmo critério AAAA-MM-DD
        & texto["tipo"].isin(["credito", "debito"])
        & valor.notna() & (valor.abs() != math.inf) & (valor > 0)
    )
    validas = texto[valida].assign(id=lambda df: df["id"].astype(int),
                                   data=data[valida], valor=valor[valida])
    return validas, len(bruto)


def resumir_por_mes(validas):
    """Agrupa por mês (AAAA-MM) com groupby e calcula as mesmas métricas do notebook."""
    tabela = validas.assign(
        mes=validas["data"].dt.strftime("%Y-%m"),
        credito=validas["valor"].where(validas["tipo"] == "credito", 0.0),
        debito=validas["valor"].where(validas["tipo"] == "debito", 0.0),
    )
    resumo = tabela.groupby("mes").agg(
        quantidade=("valor", "size"),
        total_credito=("credito", "sum"),
        total_debito=("debito", "sum"),
        media=("valor", "mean"),
        maior_valor=("valor", "max"),
        menor_valor=("valor", "min"),
    )
    resumo.insert(3, "saldo", resumo["total_credito"] - resumo["total_debito"])
    return resumo.round(2)


def comparar_com_nativo(resumo, total_validas, total_invalidas, suspeitas_ids):
    """Compara os resultados do pandas com o relatorio.json da solução nativa."""
    try:
        with open(ARQUIVO_JSON, encoding="utf-8") as arquivo:
            nativo = json.load(arquivo)
    except FileNotFoundError:
        print(f"Aviso: '{ARQUIVO_JSON}' não encontrado. Execute o notebook antes.")
        return
    comparacoes = {
        "transações válidas": total_validas == nativo["total_transacoes_validas"],
        "transações inválidas": total_invalidas == nativo["total_transacoes_invalidas"],
        "meses": list(resumo.index) == list(nativo["resumo_mensal"]),
        "IDs suspeitos": suspeitas_ids == [t["id"] for t in nativo["transacoes_suspeitas"]],
    }
    for mes, metricas in nativo["resumo_mensal"].items():
        comparacoes[f"métricas de {mes}"] = mes in resumo.index and all(
            math.isclose(resumo.loc[mes, chave], valor, abs_tol=1e-9)
            for chave, valor in metricas.items())
    for item, igual in comparacoes.items():
        print(f"{'IGUAL' if igual else 'DIFERENTE':9} | {item}")
    print("\nResultado:", "valores idênticos à solução nativa." if all(comparacoes.values())
          else "há diferenças em relação à solução nativa.")


def main():
    try:
        validas, total_lidas = ler_e_validar()
    except FileNotFoundError:
        print(f"Aviso: arquivo '{ARQUIVO_CSV}' não encontrado.")
        return
    resumo = resumir_por_mes(validas)
    suspeitas_ids = validas.loc[validas["valor"] > LIMITE_SUSPEITO, "id"].tolist()
    print("===== ANÁLISE COM PANDAS =====")
    print(f"Linhas lidas: {total_lidas} | Válidas: {len(validas)} | "
          f"Inválidas: {total_lidas - len(validas)}")
    print(f"Suspeitas (IDs): {suspeitas_ids}\n")
    print(resumo.to_string())
    print("\n===== COMPARAÇÃO COM A SOLUÇÃO NATIVA =====")
    comparar_com_nativo(resumo, len(validas), total_lidas - len(validas), suspeitas_ids)


if __name__ == "__main__":
    main()
