from typing import Optional, List
import uuid
from dao.firebase_dao import FirebaseDAO
from models.campanha import Campanha

class CampanhaDAO(FirebaseDAO):
    """DAO responsável por manipular registros de campanhas."""

    def __init__(self):
        super().__init__(collection="campanhas")

    def criar(self, campanha: Campanha) -> Optional[str]:
        """Cria uma nova campanha e retorna seu ID."""
        if not campanha.id:
            campanha.id = str(uuid.uuid4())
        if super().criar(campanha.id, campanha.to_dict()):
            return campanha.id
        return None

    def buscar_por_id(self, id: str) -> Optional[Campanha]:
        """Busca uma campanha pelo ID."""
        data = super().buscar_por_id(id)
        if data:
            return Campanha.from_dict(data)
        return None

    def listar_todos(self) -> List[Campanha]:
        """Retorna todas as campanhas cadastradas."""
        dados = super().listar_todos()
        return [Campanha.from_dict(item) for item in dados if item]

    def atualizar(self, campanha: Campanha) -> bool:
        """Atualiza os dados de uma campanha."""
        if not campanha.id:
            raise ValueError("ID da campanha não informado para atualização.")
        return super().atualizar(campanha.id, campanha.to_dict())

    def deletar(self, id: str) -> bool:
        """Remove uma campanha pelo ID."""
        return super().deletar(id)
