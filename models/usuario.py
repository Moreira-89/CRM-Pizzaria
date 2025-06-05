class Usuario:
    def __init__(self, id, nome, documento, telefone):
        self.id = id
        self.nome = nome
        self.documento = documento  
        self.telefone = telefone

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "documento": self.documento,
            "telefone": self.telefone
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id=data.get("id"),
            nome=data.get("nome"),
            documento=data.get("documento"),
            telefone=data.get("telefone")
        )
