from typing import Optional, List
import uuid
from dao.firebase_dao import FirebaseDAO
from models.fidelidade import Fidelidade

class FidelidadeDAO(FirebaseDAO):
    """DAO responsável por manipular registros de fidelidade."""

    def __init__(self):
        super().__init__(collection="fidelidade")

    def criar(self, fidelidade: Fidelidade) -> Optional[str]:
        """Cria um novo registro de fidelidade."""
        if not fidelidade.id:
            fidelidade.id = str(uuid.uuid4())
        if super().criar(fidelidade.id, fidelidade.to_dict()):
            return fidelidade.id
        return None

    def buscar_por_id(self, id: str) -> Optional[Fidelidade]:
        """Busca um registro de fidelidade pelo ID."""
        data = super().buscar_por_id(id)
        if data:
            return Fidelidade.from_dict(data)
        return None

    def listar_todos(self) -> List[Fidelidade]:
        """Lista todos os registros de fidelidade."""
        dados = super().listar_todos()
        return [Fidelidade.from_dict(item) for item in dados if item]

    def atualizar(self, fidelidade: Fidelidade) -> bool:
        """Atualiza um registro de fidelidade."""
        if not fidelidade.id:
            raise ValueError("ID da fidelidade não informado para atualização.")
        return super().atualizar(fidelidade.id, fidelidade.to_dict())

    def deletar(self, id: str) -> bool:
        """Deleta um registro de fidelidade."""
        return super().deletar(id)
