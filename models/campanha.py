from datetime import datetime


class Campanha:
    def __init__(self, id, nome, objetivo, data_inicio, data_fim,
                 canais, publicos_segmentados, clientes_atingidos=0,
                 taxa_resposta=0.0, conversao=0.0, roi=0.0, data_criacao=None):
        self.id = id
        self.nome = nome
        self.objetivo = objetivo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.canais = canais  # lista de canais: ["email", "whatsapp", "sms"]
        self.publicos_segmentados = publicos_segmentados  # ex.: ["frequentes", "Suzano"]
        self.clientes_atingidos = clientes_atingidos
        self.taxa_resposta = taxa_resposta
        self.conversao = conversao
        self.roi = roi
        self.data_criacao = data_criacao or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "objetivo": self.objetivo,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "canais": self.canais,
            "publicos_segmentados": self.publicos_segmentados,
            "clientes_atingidos": self.clientes_atingidos,
            "taxa_resposta": self.taxa_resposta,
            "conversao": self.conversao,
            "roi": self.roi,
            "data_criacao": self.data_criacao
        }

    @staticmethod
    def from_dict(data):
        return Campanha(
            id=data.get("id"),
            nome=data.get("nome"),
            objetivo=data.get("objetivo"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            canais=data.get("canais"),
            publicos_segmentados=data.get("publicos_segmentados"),
            clientes_atingidos=data.get("clientes_atingidos", 0),
            taxa_resposta=data.get("taxa_resposta", 0.0),
            conversao=data.get("conversao", 0.0),
            roi=data.get("roi", 0.0),
            data_criacao=data.get("data_criacao")
        )
