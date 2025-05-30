from datetime import datetime


class Avaliacao:
    def __init__(self, id, avaliador, avaliado, nota, comentario, data_hora=None):
        self.id = id
        self.avaliador = avaliador  # cliente, motoboy ou pizzaria
        self.avaliado = avaliado  # quem ou o que está sendo avaliado (ex.: 'motoboy:123', 'produto:calabresa')
        self.nota = nota  # de 1 a 5
        self.comentario = comentario
        self.data_hora = data_hora or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "avaliador": self.avaliador,
            "avaliado": self.avaliado,
            "nota": self.nota,
            "comentario": self.comentario,
            "data_hora": self.data_hora
        }

    @staticmethod
    def from_dict(data):
        return Avaliacao(
            id=data.get("id"),
            avaliador=data.get("avaliador"),
            avaliado=data.get("avaliado"),
            nota=data.get("nota"),
            comentario=data.get("comentario"),
            data_hora=data.get("data_hora")
        )
