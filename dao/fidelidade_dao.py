import uuid
from dao.firebase_dao import FirebaseDAO
from models.fidelidade import Fidelidade


class FidelidadeDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="fidelidade")

    def criar(self, fidelidade: Fidelidade):
        if not fidelidade.id:
            fidelidade.id = str(uuid.uuid4())
        self.db.child(fidelidade.id).set(fidelidade.to_dict())
        return fidelidade.id

    def buscar_por_id(self, id):
        data = self.db.child(id).get()
        if data and data.val():
            return Fidelidade.from_dict(data.val())
        return None

    def listar_todos(self):
        data = self.db.get()
        if data and data.val():
            return [Fidelidade.from_dict(item) for item in data.val().values()]
        return []

    def atualizar(self, fidelidade: Fidelidade):
        if not fidelidade.id:
            raise ValueError("ID da fidelidade não informado para atualização.")
        self.db.child(fidelidade.id).update(fidelidade.to_dict())

    def deletar(self, id):
        self.db.child(id).delete()
