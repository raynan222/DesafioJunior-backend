from application import Usuario



#C
def usuarioCreation():
    dados = request.get_json()


    #checa se existe cadastro do pis ou cpf
    cpf = fieldsFormatter.CpfFormatter().clean(dados["cpf"])
    pis = fieldsFormatter.PisFormatter().clean(dados["pis"])
    usuario = Usuario.query.filter(or_(Usuario.cpf == cpf, Usuario.pis == pis)).first()
    if usuario is not None:
        return jsonify({"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True})

    usuario = Usuario(
        nome = dados.get("nome"),
        pis = fieldsFormatter.PisFormatter().clean(dados.get("pis")),
        cpf = fieldsFormatter.CpfFormatter().clean(dados.get("cpf")),
    )

    db.session.add(usuario)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True})

#R(VIEW,LIST)
def usuarioView(query_id: int):
    usuario = Usuario.query.get(get_jwt_identity())

    if usuario is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(get_jwt_identity()), "error": True})
    if usuario.login.acesso.nome != "administracao":
        query_id = usuario.id

    dados = Usuario.query.get(query_id)

    if not dados:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True})

    user = dados.to_dict()
    user["error"] = False

    return jsonify(user)

def usuarioList():
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    email_filter = request.args.get("email", None)

    query = Usuario.query

    if email_filter is not None:
        #vai quebrar
        query = query.filter(Usuario.login.email.ilike("%%{}%%".format(email_filter.lower())))

    usuarios, dados = paginate(query, page, rows_per_page)

    for usuario in usuarios:
        dado = usuario.to_dict()
        dados["itens"].append(dado)

    return jsonify(dados)

#U
def usuarioUpdate(query_id: int):
    dado = request.get_json()

    usuario = Usuario.query.get(get_jwt_identity())

    #Usuario edita a si mesmo
    if usuario is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(get_jwt_identity()), "error": True})
    if usuario.login.acesso.nome != "administracao":
        query_id = usuario.id

    #recebe os dados do usuario a ser editado
    edit = Usuario.query.get(query_id)
    if not edit:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True})

    # checa validade dos dados
    cpf = dado.get("cpf")
    pis = dado.get("pis")
    existente = Usuario.query.filter(or_(Usuario.cpf == cpf, Usuario.pis == pis)).first()
    if existente is not None:
        return jsonify({"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True})


    usuario.nome = data.get("nome")
    usuario.cpf = data.get("cpf")
    usuario.pis = data.get("pis")
    try:
        db.session.commit()
        return jsonify({"message": Messages.REGISTER_SUCCESS_UPDATED.format("usuario"),"error": False,})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True})

#D(DELETION)
def usuarioDelete(query_id: int):
    usuario = Usuario.query.get(query_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    usuario_atual = Usuario.query.get(get_jwt_identity())

    if usuario_atual.login.acesso.nome != "administracao" and usuario_atual.id != usuario.id:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})

    db.session.delete(usuario)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_DELETED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        return jsonify(
            {"message": Messages.REGISTER_DELETE_INTEGRITY_ERROR, "error": True}
        )