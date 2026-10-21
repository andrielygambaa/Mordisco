"""
Mordisco — Classe Estoque
=========================
Cuida de tudo o que o estoque faz:

* guarda os produtos numa lista de objetos `Produto`;
* cadastra e remove produtos no banco SQLite;
* calcula os totais (quantos itens, quantas unidades e quanto vale tudo).

A classe `Produto` cuida de cada item; a classe `Estoque` cuida do conjunto.
"""

import sqlite3
from pathlib import Path

from produto import Produto

# O banco fica sempre na pasta do projeto, mesmo se o app for aberto de outro lugar.
CAMINHO_DB = Path(__file__).resolve().parent / "estoque.db"


class Estoque:
    """Gerencia a lista de produtos e o banco de dados da cantina."""

    def __init__(self, caminho_db=CAMINHO_DB):
        self.caminho_db = str(caminho_db)
        self.produtos = []  # lista de objetos Produto
        self.criar_tabela()
        self.carregar()

    # ------------------------------------------------------------------
    # Banco de dados
    # ------------------------------------------------------------------
    def conectar(self):
        """Abre a conexão com o arquivo SQLite."""
        conexao = sqlite3.connect(self.caminho_db)
        conexao.row_factory = sqlite3.Row
        return conexao

    def criar_tabela(self):
        """Cria a tabela `produtos` (só na primeira vez que o app roda)."""
        conexao = self.conectar()
        try:
            with conexao:
                conexao.execute(
                    """
                    CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        preco_unitario REAL NOT NULL
                    )
                    """
                )
        finally:
            conexao.close()

    # ------------------------------------------------------------------
    # Cadastro, listagem e exclusão
    # ------------------------------------------------------------------
    def cadastrar(self, nome, quantidade, preco_unitario):
        """Salva um produto novo no banco e devolve o objeto `Produto` criado."""
        conexao = self.conectar()
        try:
            with conexao:
                cursor = conexao.execute(
                    "INSERT INTO produtos (nome, quantidade, preco_unitario) VALUES (?, ?, ?)",
                    (nome, int(quantidade), float(preco_unitario)),
                )
                novo_id = cursor.lastrowid
        finally:
            conexao.close()

        produto = Produto(nome, quantidade, preco_unitario, novo_id)
        self.produtos.append(produto)  # a lista da classe fica atualizada
        return produto

    def carregar(self):
        """Lê todos os produtos do banco e guarda na lista da classe."""
        conexao = self.conectar()
        try:
            linhas = conexao.execute("SELECT * FROM produtos ORDER BY id").fetchall()
        finally:
            conexao.close()

        self.produtos = [
            Produto(linha["nome"], linha["quantidade"], linha["preco_unitario"], linha["id"])
            for linha in linhas
        ]
        return self.produtos

    def listar(self):
        """Lista de produtos do banco (sempre atualizada)."""
        return self.carregar()

    def buscar(self, produto_id):
        """Acha um produto pelo id (ou devolve None se não existir)."""
        for produto in self.listar():
            if produto.id == produto_id:
                return produto
        return None

    def remover(self, produto_id):
        """Apaga um produto do banco. Devolve True se conseguiu apagar."""
        conexao = self.conectar()
        try:
            with conexao:
                cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
                removido = cursor.rowcount > 0
        finally:
            conexao.close()

        if removido:
            self.produtos = [produto for produto in self.produtos if produto.id != produto_id]
        return removido

    # ------------------------------------------------------------------
    # Totais (resumo do estoque)
    # ------------------------------------------------------------------
    def total_produtos(self):
        """Quantos produtos estão cadastrados."""
        return len(self.listar())

    def quantidade_total(self):
        """Soma das unidades de todos os produtos."""
        return sum(produto.quantidade for produto in self.listar())

    def valor_total(self):
        """Valor financeiro de todo o estoque (soma do valor de cada produto)."""
        return sum(produto.valor_total() for produto in self.listar())
