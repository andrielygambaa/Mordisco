"""
Mordisco — API Flask (Atividade 3)
==================================
Conecta a página HTML com o banco SQLite.

Rotas:
    GET    /            -> abre a página do sistema
    GET    /produtos    -> lista os produtos do banco
    POST   /produtos    -> cadastra um produto novo
    DELETE /produtos/<id> -> apaga um produto
    GET    /resumo      -> totais do estoque (itens, unidades e valor)
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from estoque import Estoque

app = Flask(__name__)

# --- CORS: libera a API para a página buscar os dados (requisito da Atividade 3) ---
CORS(app)

# Para os acentos aparecerem certinhos no JSON ("Pão de Queijo", não "PÃ£o de Queijo").
app.json.ensure_ascii = False

# O estoque (classe Estoque) cuida de ler e gravar no banco SQLite.
estoque = Estoque()


@app.route("/")
def pagina_inicial():
    """Entrega a página principal do sistema."""
    return render_template("index.html")


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    """GET /produtos -> devolve a lista (em JSON) dos produtos salvos no banco."""
    produtos = [produto.to_dict() for produto in estoque.listar()]
    return jsonify(produtos)


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    """POST /produtos -> cadastra um produto novo e devolve o produto criado."""
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados do produto em JSON."}), 400

    nome = str(dados.get("nome", "")).strip()
    if not nome:
        return jsonify({"erro": "O nome do produto é obrigatório."}), 400

    try:
        quantidade = int(dados.get("quantidade"))
    except (TypeError, ValueError):
        return jsonify({"erro": "A quantidade precisa ser um numero inteiro."}), 400

    try:
        preco_unitario = float(dados.get("preco_unitario"))
    except (TypeError, ValueError):
        return jsonify({"erro": "O preco unitario precisa ser um numero."}), 400

    if quantidade < 0:
        return jsonify({"erro": "A quantidade nao pode ser negativa."}), 400

    if preco_unitario < 0:
        return jsonify({"erro": "O preco nao pode ser negativo."}), 400

    produto = estoque.cadastrar(nome, quantidade, preco_unitario)
    return jsonify(produto.to_dict()), 201


@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def excluir_produto(produto_id):
    """DELETE /produtos/<id> -> apaga um produto do estoque."""
    if not estoque.remover(produto_id):
        return jsonify({"erro": "Produto nao encontrado."}), 404

    return jsonify({"mensagem": "Produto removido."})


@app.route("/resumo", methods=["GET"])
def resumo_estoque():
    """GET /resumo -> totais calculados pela classe Estoque."""
    return jsonify(
        {
            "total_produtos": estoque.total_produtos(),
            "total_unidades": estoque.quantidade_total(),
            "valor_total": round(estoque.valor_total(), 2),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
