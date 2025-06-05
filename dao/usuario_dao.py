import uuid
from dao.firebase_dao import FirebaseDAO
from models.usuario import Usuario


class UsuarioDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="usuarios")

    def criar(self, usuario: Usuario):
        if not usuario.id:
            usuario.id = str(uuid.uuid4())
        self.db.child(usuario.id).set(usuario.to_dict())
        return usuario.id

    def buscar_por_nome(self, nome):
        data = self.db.get()
        if data and data.val():
            for item in data.val().values():
                if item.get("nome", "").lower() == nome.lower():
                    return Usuario.from_dict(item)
        return None

    def listar_todos(self):
        data = self.db.get()
        if data and data.val():
            return [Usuario.from_dict(item) for item in data.val().values()]
        return []
