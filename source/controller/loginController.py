from application import Login



#C
def loginCreation():
    dados = request.get_json()

    #Checa a existencia de email ja cadastrado
    if Login.query.filter_by(email=dados.get("email").lower()).first():
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("email"), "error": True}
        )

    senha_hashed = generate_password_hash(dados.get('senha'), method="sha256")
    email = dados.get("email").lower()
    login = Login(email = email,
                  senha = senha_hashed,
                  acesso_id = 1)

    db.session.add(login)

    try:
        db.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True})

#R(VIEW,LIST)
def loginView(query_id: int):
    login = Login.query.get(get_jwt_identity())

    #Caso o login nao seja adminitrado ele ve a si mesmo
    if login is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(get_jwt_identity()), "error": True})
    if login.acesso.nome != "administracao":
        query_id = login.id

    dados = Login.query.get(query_id)

    if not dados:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True})

    dado = dados.to_dict()
    dado["error"] = False

    return jsonify(dado)

def loginList():
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    email_filter = request.args.get("email", None)

    query = Login.query

    if email_filter is not None:
        query = query.filter(Login.email.ilike("%%{}%%".format(email_filter.lower())))

    logins, dados = paginate(query, page, rows_per_page)

    for login in logins:
        dado = login.to_dict()
        dados["itens"].append(dado)

    return jsonify(dados)

#U
def loginUpdate(query_id: int):
    dado = request.get_json()

    login = Login.query.get(get_jwt_identity())

    #Login edita a si mesmo
    if login is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(get_jwt_identity()), "error": True})
    if login.acesso.nome != "administracao":
        query_id = login.id

    #recebe os dados do login a ser editado
    edit = Login.query.get(query_id)
    if not edit:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(login_id), "error": True})

    # mudança de senha, somente realizado pelo proprio
    if login.id == edit.id:
        # checa a mudança na senha
        if dado.get('senha') is not None:
            senha_hashed = generate_password_hash(dado.get('senha'), method="sha256")
            login.senha = senha_hashed

    login.email = data.get("email").lower()

    try:
        db.session.commit()
        return jsonify({"message": Messages.REGISTER_SUCCESS_UPDATED.format("login"),"error": False,})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True})

#D(DELETION)
def loginDelete(query_id: int):
    login = Login.query.get(query_id)

    if not login:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    login_atual = Login.query.get(get_jwt_identity())

    if login_atual.acesso.nome != "administracao" and login_atual.id != login.id:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})

    db.session.delete(login)

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