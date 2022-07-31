import re

from flask import request, jsonify
from sqlalchemy import or_
from sqlalchemy import exc
from flask_jwt_extended import get_jwt_identity, jwt_required
from application.app import app
from application.database import db
from source.controller import paginate, Messages
from source.model.usuarioTable import Usuario

#C
@app.route("/usuario/add", methods=["POST"])
@jwt_required
def usuarioCreation():
    dados = request.get_json()

    #checa se existe cadastro do pis ou cpf
    cpf = re.sub('[^\\d+$]', '', dados["cpf"])
    pis = re.sub('[^\\d+$]', '', dados["pis"])
    usuario = Usuario.query.filter(or_(Usuario.cpf == cpf, Usuario.pis == pis)).first()
    if usuario is not None:
        return jsonify({"message": Messages.ALREADY_EXISTS.format("CPF/PIS"), "error": True})

    usuario = Usuario(
        nome = dados["nome"],
        pis = re.sub('[^\\d+$]', '', dados["pis"]),
        cpf = re.sub('[^\\d+$]', '', dados["cpf"]),
    )

    db.session.add(usuario)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True})

#R(VIEW,LIST)
@app.route("/usuario/view/<int:query_id>", methods=["GET"])
@jwt_required
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

@app.route("/perfil/list", methods=["GET"])
@jwt_required
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
@app.route("/usuario/edit/<int:query_id>", methods=["PUT"])
@jwt_required
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


    usuario.nome = dado.get("nome")
    usuario.cpf = dado.get("cpf")
    usuario.pis = dado.get("pis")
    try:
        db.session.commit()
        return jsonify({"message": Messages.REGISTER_SUCCESS_UPDATED.format("usuario"),"error": False,})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True})

#D(DELETION)
@app.route("/usuario/delete/<int:query_id>", methods=["DELETE"])
@jwt_required
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