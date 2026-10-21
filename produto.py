"""
Mordisco — Classe Produto
=========================
Representa um item do estoque da cantina.

Toda linha salva no banco SQLite vira um objeto da classe `Produto`.
É daqui que sai o cálculo do valor de cada produto:
    valor total do produto = quantidade x preço unitário
"""


class Produto:
    """Um produto (lanche) guardado no estoque da cantina."""

    def __init__(self, nome, quantidade, preco_unitario, id=None):
        self.id = id
        self.nome = nome
        self.quantidade = int(quantidade)
        self.preco_unitario = float(preco_unitario)

    def valor_total(self):
        """Quanto vale esse produto dentro do estoque."""
        return self.quantidade * self.preco_unitario

    def to_dict(self):
        """Transforma o objeto em dicionário (o mesmo formato usado no JSON da API)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "preco_unitario": round(self.preco_unitario, 2),
            "valor_total": round(self.valor_total(), 2),
        }

    def __str__(self):
        return f"{self.nome} - {self.quantidade} un. x R$ {self.preco_unitario:.2f}"

    def __repr__(self):
        return (
            f"Produto(id={self.id}, nome='{self.nome}', "
            f"quantidade={self.quantidade}, preco_unitario={self.preco_unitario})"
        )
