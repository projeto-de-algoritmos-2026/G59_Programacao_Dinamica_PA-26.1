# 🍕 Montador de Pizza Inteligente

**Disciplina:** Projeto e Análise de Algoritmos  
**Aluna:** Leticia de Carvalho dos Santos  
**Matrícula:** 222022135  
**Gravação:** [[clique aqui para assistir](https://youtu.be/x2MV74PstDo)](#) 

---

## 📌 Sobre o projeto

O Montador de Pizza Inteligente é uma aplicação web que usa o algoritmo de **Programação Dinâmica — Knapsack 0-1** para encontrar a combinação de ingredientes com o **maior sabor possível** dentro de um limite calórico definido pelo usuário.

A ideia é simples: cada ingrediente tem um custo em kcal (o "peso") e uma nota de sabor (o "valor"). O algoritmo decide quais ingredientes incluir ou não, sem repetição, para maximizar o sabor total sem ultrapassar o limite de kcal.

---

## 🎒 O problema do Knapsack

O problema da mochila (Knapsack 0-1) é um problema clássico de otimização:

> Dado um conjunto de itens, cada um com um **peso** e um **valor**, e uma mochila com **capacidade máxima**, escolha quais itens levar para **maximizar o valor total** sem ultrapassar a capacidade.

Na nossa pizza:

| Conceito geral | Na pizza |
|---|---|
| Mochila | Limite de kcal do cliente |
| Peso do item | kcal do ingrediente |
| Valor do item | Nota de sabor (1–15) |
| Solução ótima | Combinação de ingredientes mais gostosa |

---

## 🧠 Por que Programação Dinâmica?

### A abordagem ingênua (força bruta)

Sem DP, a solução seria testar **todas as combinações possíveis** de ingredientes. Com 10 ingredientes, isso significa 2¹⁰ = **1024 combinações**. Com 30 ingredientes, seriam mais de **1 bilhão**. Inviável.

### A abordagem gulosa (greedy)

Outra tentativa seria ordenar os ingredientes pela razão sabor/kcal e ir adicionando enquanto couber. Mas como mostrado nas aulas, o algoritmo guloso **não garante a solução ótima** quando os pesos são arbitrários.

### A solução com DP

A Programação Dinâmica resolve o problema quebrando-o em **subproblemas menores que se sobrepõem** e guardando os resultados para não recalcular.

A ideia central é definir:

> **M[i][w]** = maior sabor possível usando os primeiros **i** ingredientes com no máximo **w** kcal disponíveis.

A recorrência é:

```
M[i][w] = 0                                          se i = 0 ou w = 0

M[i][w] = M[i-1][w]                                 se kcal_i > w
           (ingrediente não cabe, ignora)

M[i][w] = max( M[i-1][w],                           caso contrário
               sabor_i + M[i-1][w - kcal_i] )
           (escolhe o melhor entre incluir ou não incluir)
```

Cada célula da tabela é resolvida **uma única vez** e reutilizada por outras células. Isso transforma a complexidade de O(2ⁿ) para **O(n × W)**, onde n é o número de ingredientes e W é o limite de kcal.

---

## 📊 Exemplo passo a passo

Considere 3 ingredientes e limite de 100 kcal:

| # | Ingrediente | kcal | Sabor |
|---|---|---|---|
| 1 | 🥬 Rúcula | 10 | 2 |
| 2 | 🍄 Cogumelos | 20 | 6 |
| 3 | 🧀 Mozzarella | 80 | 9 |

A tabela DP preenchida (simplificada em blocos de 10 kcal):

```
          0    10    20    30    40    50    60    70    80    90   100
∅         0     0     0     0     0     0     0     0     0     0     0
Rúcula    0     2     2     2     2     2     2     2     2     2     2
Cogumelos 0     2     6     8     8     8     8     8     8     8     8
Mozzarella 0    2     6     8     8     8     9    11    15    17    17  ← solução
```

A célula M[3][100] = **17** indica que o maior sabor com 100 kcal é 17.

Fazendo o **backtracking** (de baixo pra cima na tabela):
- M[3][100] ≠ M[2][100] → Mozzarella foi incluída, w = 100 - 80 = 20
- M[2][20] ≠ M[1][20] → Cogumelos foi incluída, w = 20 - 20 = 0
- Resultado: 🧀 Mozzarella + 🍄 Cogumelos = **17 de sabor com 100 kcal**

---

## ⚙️ Como funciona o código

### Backend — `app.py`

Implementado em Python com Flask. A função principal `knapsack()` recebe a lista de ingredientes selecionados e o limite de kcal, e retorna:

- `sabor_maximo` — o maior sabor encontrado
- `escolhidos` — lista de ingredientes da solução ótima
- `tabela_dp` — a tabela M completa (para visualização no frontend)

```python
def knapsack(ingredientes, limite_kcal):
    itens = [{"blocos": i["kcal"] // 10, ...} for i in ingredientes]
    W = limite_kcal // 10
    n = len(itens)

    M = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = itens[i - 1]
        for w in range(W + 1):
            sem = M[i - 1][w]
            if item["blocos"] <= w:
                com = item["sabor"] + M[i - 1][w - item["blocos"]]
                M[i][w] = max(sem, com)
            else:
                M[i][w] = sem

    # backtracking para descobrir quais itens foram escolhidos
    escolhidos = []
    w = W
    for i in range(n, 0, -1):
        if M[i][w] != M[i - 1][w]:
            escolhidos.append(ingredientes[i - 1])
            w -= itens[i - 1]["blocos"]

    return {"sabor_maximo": M[n][W], "escolhidos": escolhidos, "tabela_dp": M}
```

### Frontend — `index.html`

HTML + CSS + JavaScript puro. Permite ao usuário:

1. Definir o limite de kcal via slider (100–800 kcal)
2. Selecionar quais ingredientes considerar
3. Visualizar os ingredientes escolhidos com suas kcal
4. Ver a tabela DP completa com o caminho da solução ótima destacado

---

## 🚀 Como rodar

**Pré-requisitos:** Python 3.8+

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Instalar dependência
pip install flask

# 3. Rodar o servidor
python app.py

# 4. Abrir no navegador
# http://localhost:5000
```

---

## 📈 Complexidade

| | Tempo | Espaço |
|---|---|---|
| Força bruta | O(2ⁿ) | O(n) |
| Knapsack DP | O(n × W) | O(n × W) |

Onde **n** = número de ingredientes e **W** = limite de kcal (em blocos de 10).

---

