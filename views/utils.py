# views/utils.py

def buscar_por_campo_unico(dao, cpf=None, telefone=None, nome=None):
    """
    Busca um registro em dao por CPF (prioritário), telefone ou nome.
    Retorna (objeto, mensagem_erro).
    """
    try:
        registros = dao.listar_todos()
    except Exception:
        return None, "Erro ao acessar a base de dados."

    if cpf:
        encontrados = [r for r in registros if hasattr(r, "cpf") and r.cpf == cpf]
        if len(encontrados) == 1:
            return encontrados[0], None
        elif len(encontrados) > 1:
            return None, "Mais de um registro encontrado com este CPF."
        else:
            return None, "Nenhum registro encontrado com este CPF."

    if telefone:
        encontrados = [r for r in registros if hasattr(r, "telefone") and r.telefone == telefone]
        if len(encontrados) == 1:
            return encontrados[0], None
        elif len(encontrados) > 1:
            return None, "Mais de um registro encontrado com este telefone."
        else:
            return None, "Nenhum registro encontrado com este telefone."

    if nome:
        encontrados = [r for r in registros if hasattr(r, "nome") and r.nome.lower() == nome.lower()]
        if len(encontrados) == 1:
            return encontrados[0], None
        elif len(encontrados) > 1:
            return None, "Mais de um registro encontrado com este nome."
        else:
            return None, "Nenhum registro encontrado com este nome."

    return None, "Informe CPF, telefone ou nome para busca."
