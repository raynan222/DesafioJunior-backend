import re

from flask import request, jsonify
from werkzeug.security import generate_password_hash
from application.database import db
from application.app import app
from source.controller import paginate, Messages
from source.model.enderecoTable import Endereco
from source.model.loginTable import Login
from sqlalchemy import exc, or_
from flask_jwt_extended import get_jwt_identity, jwt_required
from source.model.usuarioTable import Usuario

#C



@app.route("/login/cadastro", methods=["POST"])
def cadastroLogin():
    dado = request.get_json()

    #checa a existencia de um login ja cadastrado com os dados informados
    if Login.query.filter_by(email=dado.get("email").lower()).first():
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("email"), "error": True}
        )

    #Checa existencia de um usuario ja cadastrado com os dados informados
    cpf = re.sub('[^\\d+$]', '', dado["cpf"])
    pis = re.sub('[^\\d+$]', '', dado["pis"])
    usuario = Usuario.query.filter(or_(Usuario.cpf == cpf, Usuario.pis == pis)).first()
    if usuario is not None:
        return jsonify(
            {"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )

    senha_hashed = generate_password_hash(dado.get('senha'), method="sha256")
    email = dado.get("email").lower()

    #Cadastra o endereço
    endereco = Endereco(
        cep=re.sub('[^\\d+$]', '', dado.get("cep")),
        rua=dado.get("rua"),
        numero=dado.get("numero"),
        bairro=dado.get("bairro"),
        complemento=dado.get("complemento"),
        municipio_id=dado.get("municipio_id"),
    )
    db.session.add(endereco)

    #Cadastra o usuario
    usuario = Usuario(
        nome=dado.get("nome"),
        pis=re.sub('[^\\d+$]', '', dado.get("pis")),
        cpf=re.sub('[^\\d+$]', '', dado.get("cpf")),
        endereco=endereco.id
    )
    db.session.add(usuario)

    try:
        db.session.flush()

        login = Login(
            email=email,
            senha=senha_hashed,
            usuario_id=usuario.id,
            cargo_id=2,
        )

        db.session.add(login)

        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_CREATED.format("Login"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )

@app.route("/login/add", methods=["POST"])
@jwt_required
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
@app.route("/login/view/<int:query_id>", methods=["GET"])
@jwt_required
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

@app.route("/login/list", methods=["GET"])
@jwt_required
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
@app.route("/login/update/<int:query_id>", methods=["PUT"])
@jwt_required
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
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format("login_id"), "error": True})

    # mudança de senha, somente realizado pelo proprio
    if login.id == edit.id:
        # checa a mudança na senha
        if dado.get('senha') is not None:
            senha_hashed = generate_password_hash(dado.get('senha'), method="sha256")
            login.senha = senha_hashed

    login.email = dado.get("email").lower()

    try:
        db.session.commit()
        return jsonify({"message": Messages.REGISTER_SUCCESS_UPDATED.format("login"),"error": False,})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True})

#D(DELETION)
@app.route("/login/delete/<int:query_id>", methods=["DELETE"])
@jwt_required
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