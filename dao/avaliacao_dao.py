import uuid
from dao.firebase_dao import FirebaseDAO
from models.avaliacao import Avaliacao


class AvaliacaoDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="avaliacoes")

    def criar(self, avaliacao: Avaliacao):
        if not avaliacao.id:
            avaliacao.id = str(uuid.uuid4())
        self.db.child(avaliacao.id).set(avaliacao.to_dict())
        return avaliacao.id

    def buscar_por_id(self, id):
        data = self.db.child(id).get()
        if data and data:
            return Avaliacao.from_dict(data)
        return None

    def listar_todos(self):
        data = self.db.get()
        if data and data:
            return [Avaliacao.from_dict(item) for item in data.values()]
        return []

    def atualizar(self, avaliacao: Avaliacao):
        if not avaliacao.id:
            raise ValueError("ID da avaliação não informado para atualização.")
        self.db.child(avaliacao.id).update(avaliacao.to_dict())

    def deletar(self, id):
        self.db.child(id).delete()
