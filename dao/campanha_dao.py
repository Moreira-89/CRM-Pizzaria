import uuid
from dao.firebase_dao import FirebaseDAO
from models.campanha import Campanha


class CampanhaDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="campanhas")

    def criar(self, campanha: Campanha):
        if not campanha.id:
            campanha.id = str(uuid.uuid4())
        self.db.child(campanha.id).set(campanha.to_dict())
        return campanha.id

    def buscar_por_id(self, id):
        data = self.db.child(id).get()
        if data and data.val():
            return Campanha.from_dict(data.val())
        return None

    def listar_todos(self):
        data = self.db.get()
        if data and data.val():
            return [Campanha.from_dict(item) for item in data.val().values()]
        return []

    def atualizar(self, campanha: Campanha):
        if not campanha.id:
            raise ValueError("ID da campanha não informado para atualização.")
        self.db.child(campanha.id).update(campanha.to_dict())

    def deletar(self, id):
        self.db.child(id).delete()
