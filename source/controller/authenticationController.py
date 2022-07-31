import re
from sqlalchemy import or_

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, \
    jwt_required
from werkzeug.security import check_password_hash

from source.controller import Messages
from application.app import app
from application.database import db
from source.model.loginTable import Login
from source.model.usuarioTable import Usuario


@app.route("/login", methods=["POST"])
def login():
    dado = request.get_json()

    email = dado.get("email").lower()
    cpf_ou_pis = re.sub('[^\\d+$]', '', email)

    login = db.session.query(Login).join(Usuario, Usuario.id == Login.usuario_id).filter(
        or_(
            Login.email == email,
            Usuario.cpf == cpf_ou_pis,
            Usuario.pis == cpf_ou_pis
        )
    ).first()

    retorno = {
        "form": [],
        "error": False
    }

    if not login:
        retorno["form"].append({"message": Messages.AUTH_USER_NOT_FOUND})
        retorno["error"] = True
    elif not check_password_hash(login.senha, str(dado.get("senha"))):
        retorno["form"].append({"message": Messages.AUTH_USER_PASS_ERROR})
        retorno["error"] = True

    if retorno["error"]:
        return jsonify(retorno)

    return (
        jsonify(
            {
                "access_token": create_access_token(identity=login.id),
                "refresh_token": create_refresh_token(identity=login.id),
                "acesso_id": login.acesso_id,
                "email": login.email,
                "usuario_id": login.usuario_id,
                "usuario": {
                    "id": login.usuario_id,
                    "nome": login.usuario.nome,
                    "cpf": login.usuario.cpf,
                    "pis": login.usuario.pis
                } if login.usuario_id is not None else None,
                "acesso": {
                    "id": login.acesso.id,
                    "name": login.acesso.nome
                },
            }
        ),
        200,
    )

@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    return jsonify({"access_token": create_access_token(identity=get_jwt_identity())}), 200

@app.route("/loginview", methods=["GET"])
@jwt_required
def view():
    login = Login.query.get(get_jwt_identity())
    if login is None:
        return jsonify({"message": Messages.REGISTER_NOT_FOUND.format(get_jwt_identity()), "error": True})

    return (
        jsonify(
            {
                "error": False,
                "id": login.id,
                "email": login.email,
                "usuario_id": login.usuario_id,
                "usuario":{
                    "id": login.usuario_id,
                    "nome": login.usuario.nome,
                    "cpf": login.usuario.cpf,
                    "pis": login.usuario.pis,
                    "cep": login.usuario.endereco.cep,
                    "rua": login.usuario.endereco.rua,
                    "numero": login.usuario.endereco.numero,
                    "bairro": login.usuario.endereco.bairro,
                    "complemento": login.usuario.endereco.complemento,
                    "municipio_id": login.usuario.endereco.municipio_id,
                }if login.usuario_id is not None else None,
                "acesso_id": login.acesso_id,
                "acesso": {
                    "id": login.acesso.id,
                    "name": login.acesso.nome
                },
            }
        ),
        200,
    )

