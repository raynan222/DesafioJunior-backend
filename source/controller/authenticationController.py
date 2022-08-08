import re
from sqlalchemy import or_
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash

from source.controller import Globals, field_validator
from application.app import app, db
from source.model.loginTable import Login, LoginModel
from source.model.usuarioTable import Usuario, UsuarioModel


@app.route("/login", methods=["POST"])
@field_validator(LoginModel)
@field_validator(UsuarioModel)
def login():
    """Realiza o login
    ---
    post:
        tags: [Rotas]
        summary: Realiza o login retorna JWT
        requestBody:
            description: Dados necessários para o login
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    email/cpf/pis:
                      type: string
                    senha:
                      type: string
                  required:
                    - emailCpfPis
                    - senha
        responses:
            200:
                description: "Sucesso"
                content:
                    application/json:
                        schema:
                          type: object
                          properties:
                            message:
                              type: string
            400:
                description: "Ocorreu um erro"
                content:
                  application/json:
                    schema:
                      type: object
                      properties:
                        error:
                          type: string
    """
    dado = request.get_json()

    email = dado.get("email/cpf/pis").lower()
    cpf_ou_pis = re.sub("[^\\d+$]", "", email)

    login = (
        db.session.query(Login)
        .join(Usuario, Usuario.id == Login.usuario_id)
        .filter(
            or_(
                Login.email == email,
                Usuario.cpf == cpf_ou_pis,
                Usuario.pis == cpf_ou_pis,
            )
        )
        .first()
    )

    if not login:
        return jsonify({"message": Globals.AUTH_USER_NOT_FOUND, "error": True})
    elif not check_password_hash(login.senha, str(dado.get("senha"))):
        return jsonify({"message": Globals.AUTH_USER_PASS_ERROR, "error": True})

    usuario = Usuario.query.get(login.usuario_id)
    return (
        jsonify(
            {
                "access_token": create_access_token(identity=login.id),
                "refresh_token": create_refresh_token(identity=login.id),
                "acesso_id": login.acesso_id,
                "email": login.email,
                "id": login.id,
                "usuario_id": login.usuario_id,
                "usuario": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "cpf": usuario.cpf,
                    "pis": usuario.pis,
                },
                "acesso": {"id": login.acesso.id, "name": login.acesso.nome},
                "error": False,
            }
        ),
        200,
    )


@app.route("/refresh", methods=["GET"])
@jwt_refresh_token_required
def refresh():
    return (
        jsonify({"access_token": create_access_token(identity=get_jwt_identity())}),
        200,
    )


@app.route("/loginview", methods=["GET"])
@jwt_required
def view():
    login = Login.query.get(get_jwt_identity())
    if login is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )

    return (
        jsonify(login.to_dict_complete()),
        200,
    )
