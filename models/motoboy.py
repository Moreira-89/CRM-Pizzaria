from models.usuario import Usuario

class Motoboy(Usuario):
    def __init__(self, id, nome, cpf, cnh, telefone, status_operacional,
                 zonas_atuacao=None, horarios_disponiveis=None, avaliacao_media=None, tempo_medio_entrega=None):
        super().__init__(id, nome, cpf, telefone)
        self.cnh = cnh
        self.telefone = telefone
        self.status_operacional = status_operacional  
        self.zonas_atuacao = zonas_atuacao or []
        self.horarios_disponiveis = horarios_disponiveis or []
        self.avaliacao_media = avaliacao_media or 0
        self.tempo_medio_entrega = tempo_medio_entrega or 0

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "cnh": self.cnh,
            "telefone": self.telefone,
            "status_operacional": self.status_operacional,
            "zonas_atuacao": self.zonas_atuacao,
            "horarios_disponiveis": self.horarios_disponiveis,
            "avaliacao_media": self.avaliacao_media,
            "tempo_medio_entrega": self.tempo_medio_entrega
        })
        return base

    @staticmethod
    def from_dict(data):
        return Motoboy(
            id=data.get("id"),
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            cnh=data.get("cnh"),
            telefone=data.get("telefone"),
            status_operacional=data.get("status_operacional"),
            zonas_atuacao=data.get("zonas_atuacao"),
            horarios_disponiveis=data.get("horarios_disponiveis"),
            avaliacao_media=data.get("avaliacao_media"),
            tempo_medio_entrega=data.get("tempo_medio_entrega")
        )
