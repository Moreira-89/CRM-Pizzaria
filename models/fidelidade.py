from datetime import datetime


class Fidelidade:
    def __init__(self, id, cliente_id, cliente_nome, pontos, nivel, validade, historico=None):
        self.id = id
        self.cliente_id = cliente_id
        self.cliente_nome = cliente_nome  # Nome armazenado para exibir na listagem
        self.pontos = pontos
        self.nivel = nivel
        self.validade = validade  # formato YYYY-MM-DD
        self.historico = historico or []

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "cliente_nome": self.cliente_nome,
            "pontos": self.pontos,
            "nivel": self.nivel,
            "validade": self.validade,
            "historico": self.historico
        }

    @staticmethod
    def from_dict(data):
        return Fidelidade(
            id=data.get("id"),
            cliente_id=data.get("cliente_id"),
            cliente_nome=data.get("cliente_nome"),
            pontos=data.get("pontos"),
            nivel=data.get("nivel"),
            validade=data.get("validade"),
            historico=data.get("historico")
        )
