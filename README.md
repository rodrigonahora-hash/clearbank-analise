# ClearBank — Análise Financeira com Python

Notebook Python que lê e valida o histórico de transações bancárias da fintech fictícia **ClearBank** (`transacoes.csv`), descarta registros inválidos, calcula métricas financeiras mensais, sinaliza transações suspeitas (acima de R$ 10.000,00), exibe um relatório formatado e salva o resultado em `relatorio.json`.

A solução principal usa apenas módulos nativos do Python (`csv`, `json`, `datetime`, `math`), sem pandas.

Desafio prático da disciplina *Análise de Dados e Inteligência de Negócios com IA*.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `desafio-final.ipynb` | Notebook principal, executado e salvo com as saídas |
| `transacoes.csv` | Dados de entrada para teste (18 válidos, 14 inválidos, 3 suspeitos) |
| `relatorio.json` | Relatório gerado pelo notebook |
| `grafico.png` | Gráfico de crédito e débito por mês (opcional RO2) |
| `analise_pandas.py` | Versão alternativa com pandas que confere os resultados (opcional RO1) |

## Como executar

### Google Colab

1. Abra o `desafio-final.ipynb` no [Google Colab](https://colab.research.google.com) (*Arquivo → Fazer upload de notebook*).
2. No painel **Arquivos** (ícone de pasta à esquerda), envie o `transacoes.csv` e, se quiser rodar a comparação com pandas, o `analise_pandas.py`.
3. Execute todas as células em ordem: *Ambiente de execução → Executar tudo*.

### Jupyter local

Requer Python 3.10 ou superior. Com os arquivos na mesma pasta:

```bash
pip install notebook pandas matplotlib   # pandas e matplotlib só para os opcionais
jupyter notebook desafio-final.ipynb
```

Depois, rode todas as células em ordem (*Run → Run All Cells*).

A versão pandas também pode ser executada direto no terminal, depois do notebook: `python analise_pandas.py`.

## O que o notebook gera

1. **Resumo da limpeza**: total de linhas lidas, válidas e inválidas.
2. **Relatório no terminal**, com separadores `=====` e valores em reais (`R$ 3.500,00`):
   - período analisado (data mais antiga → mais recente e dias entre elas);
   - por mês: quantidade de transações, total de crédito, total de débito, saldo, média, maior e menor valor;
   - transações suspeitas (ID, cliente, data e valor).
3. **`relatorio.json`**: data de geração, totais de válidas e inválidas, resumo mensal e lista de suspeitas.
4. **`grafico.png`** (opcional): barras empilhadas de crédito e débito por mês.
5. **Comparação com pandas** (opcional): confirma que a versão pandas chega aos mesmos valores.

## Regras de validação

Uma linha é descartada (sem interromper o processamento) quando tem:

- `id` vazio ou não numérico;
- `cliente_id` vazio;
- `data` fora do formato `AAAA-MM-DD`;
- `tipo` diferente de `credito` ou `debito`;
- `valor` não numérico ou menor ou igual a zero.

Uma transação é **suspeita** quando o valor é maior que `LIMITE_SUSPEITO = 10000.00`.

## Uso de IA

Este projeto foi desenvolvido com apoio do assistente de IA **Claude Code** (Anthropic), utilizado no planejamento, na implementação e nos testes, sob orientação do autor. Cada etapa foi proposta, revisada e aprovada pelo autor antes de seguir para a próxima, e todo o código foi revisado e compreendido por ele. A execução final do notebook foi feita pelo autor no Google Colab.
