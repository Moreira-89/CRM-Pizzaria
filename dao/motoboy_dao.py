import uuid
from dao.firebase_dao import FirebaseDAO
from models.motoboy import Motoboy


class MotoboyDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="motoboys")

    def criar(self, motoboy: Motoboy):
        if not motoboy.id:
            motoboy.id = str(uuid.uuid4())
        self.db.child(motoboy.id).set(motoboy.to_dict())
        return motoboy.id

    def buscar_por_id(self, id):
        data = self.db.child(id).get()
        if data and data.val():
            return Motoboy.from_dict(data.val())
        return None

    def listar_todos(self):
        data = self.db.get()
        if data and data.val():
            return [Motoboy.from_dict(item) for item in data.val().values()]
        return []

    def atualizar(self, motoboy: Motoboy):
        if not motoboy.id:
            raise ValueError("ID do motoboy não informado para atualização.")
        self.db.child(motoboy.id).update(motoboy.to_dict())

    def deletar(self, id):
        self.db.child(id).delete()
