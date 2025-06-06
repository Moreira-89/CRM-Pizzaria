def buscar_por_campo_unico(dao, cpf=None, telefone=None, nome=None):
    """
    Busca um registro por CPF (prioritário), telefone ou nome.
    Retorna (objeto, mensagem_erro)
    """
    if cpf:
        registros = [r for r in dao.listar_todos() if hasattr(r, "cpf") and r.cpf == cpf]
        if registros:
            return registros[0], None
        return None, "Nenhum registro encontrado com este CPF."
    elif telefone:
        registros = [r for r in dao.listar_todos() if hasattr(r, "telefone") and r.telefone == telefone]
        if len(registros) == 1:
            return registros[0], None
        elif len(registros) > 1:
            return None, "Mais de um registro encontrado com este telefone. Por favor, use o CPF."
        else:
            return None, "Nenhum registro encontrado com este telefone."
    elif nome:
        registros = [r for r in dao.listar_todos() if hasattr(r, "nome") and r.nome.lower() == nome.lower()]
        if len(registros) == 1:
            return registros[0], None
        elif len(registros) > 1:
            return None, "Mais de um registro encontrado com este nome. Por favor, use o CPF ou telefone."
        else:
            return None, "Nenhum registro encontrado com este nome."
    else:
        return None, "Informe pelo menos um campo para busca."