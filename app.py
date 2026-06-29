from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Cada ingrediente tem kcal reais e uma nota de sabor de 1-15
INGREDIENTES = [
    {"id": 1,  "nome": "Mozzarella",  "kcal": 80,  "sabor": 9,  "emoji": "🧀"},
    {"id": 2,  "nome": "Pepperoni",   "kcal": 130, "sabor": 10, "emoji": "🍖"},
    {"id": 3,  "nome": "Cogumelos",   "kcal": 20,  "sabor": 6,  "emoji": "🍄"},
    {"id": 4,  "nome": "Pimentão",    "kcal": 20,  "sabor": 5,  "emoji": "🫑"},
    {"id": 5,  "nome": "Azeitona",    "kcal": 40,  "sabor": 4,  "emoji": "🫒"},
    {"id": 6,  "nome": "Frango",      "kcal": 90,  "sabor": 8,  "emoji": "🍗"},
    {"id": 7,  "nome": "Bacon",       "kcal": 150, "sabor": 12, "emoji": "🥓"},
    {"id": 8,  "nome": "Tomate seco", "kcal": 30,  "sabor": 3,  "emoji": "🍅"},
    {"id": 9,  "nome": "Rúcula",      "kcal": 10,  "sabor": 2,  "emoji": "🥬"},
    {"id": 10, "nome": "Catupiry",    "kcal": 110, "sabor": 11, "emoji": "🫙"},
]


def knapsack(ingredientes, limite_kcal):
    """
    Knapsack 0-1 bottom-up.
    Trabalha internamente em blocos de 10 kcal para manter a tabela pequena.
    Retorna sabor máximo, ingredientes escolhidos e tabela DP (em blocos).
    """
    # converte kcal reais para blocos de 10
    itens = [{"nome": i["nome"], "emoji": i["emoji"], "kcal": i["kcal"],
               "blocos": i["kcal"] // 10, "sabor": i["sabor"]} for i in ingredientes]

    W = limite_kcal // 10          # limite em blocos
    n = len(itens)

    # tabela M[i][w]: melhor sabor usando primeiros i itens com até w blocos
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

    # backtracking: quais itens foram escolhidos
    escolhidos = []
    w = W
    for i in range(n, 0, -1):
        if M[i][w] != M[i - 1][w]:
            escolhidos.append(ingredientes[i - 1])   # devolve obj original com kcal reais
            w -= itens[i - 1]["blocos"]
    escolhidos.reverse()

    return {
        "sabor_maximo": M[n][W],
        "escolhidos": escolhidos,
        "tabela_dp": M,          # índices internos (blocos)
        "limite_blocos": W,      # para o frontend saber até onde vai a tabela
    }


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/ingredientes")
def get_ingredientes():
    return jsonify(INGREDIENTES)


@app.route("/montar", methods=["POST"])
def montar():
    data = request.get_json()
    limite = int(data.get("limite_kcal", 300))
    ids    = set(data.get("ids_ingredientes", []))

    disponiveis = [i for i in INGREDIENTES if i["id"] in ids]
    if not disponiveis:
        return jsonify({"erro": "Selecione ao menos um ingrediente."}), 400
    if limite < 10:
        return jsonify({"erro": "Limite mínimo é 10 kcal."}), 400

    return jsonify(knapsack(disponiveis, limite))


if __name__ == "__main__":
    print("🍕 http://localhost:5000")
    app.run(debug=True, port=5000)