import re

from flask import request, jsonify
from werkzeug.security import generate_password_hash
from application.app import app, db
from source.controller import paginate, Globals, field_validator
from source.model.enderecoTable import Endereco, EnderecoModel
from source.model.loginTable import Login, LoginModel
from sqlalchemy import exc, or_
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from source.model.usuarioTable import Usuario, UsuarioModel


# C
@app.route("/login/cadastro", methods=["POST"])
@field_validator(LoginModel)
@field_validator(UsuarioModel)
@field_validator(EnderecoModel)
def cadastroLogin():
    """Adiciona registro
    ---
    post:
        summary: Adiciona um registro
        requestBody:
            description: Dados necessários para a criação do registro
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    email:
                      type: string
                    senha:
                      type: string
                    nome:
                      type: string
                    pis:
                      type: string
                    cpf:
                      type: string
                    cep:
                      type: string
                    rua:
                      type: string
                    numero:
                      type: string
                    bairro:
                      type: string
                    complemento:
                      type: string
                    municipio_id:
                      type: integer
                  required:
                    - email
                    - senha
                    - nome
                    - pis
                    - cpf
                    - cep
                    - rua
                    - numero
                    - bairro
                    - municipio_id
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

    # checa a existencia de um login ja cadastrado com os dados informados
    if Login.query.filter_by(email=dado.get("email").lower()).first():
        return jsonify(
            {"message": Globals.ALREADY_EXISTS.format("email"), "error": True}
        )

    # Checa existencia de um usuario ja cadastrado com os dados informados
    cpf = re.sub("[^\\d+$]", "", dado.get("cpf"))
    pis = re.sub("[^\\d+$]", "", dado.get("pis"))
    usuario = Usuario.query.filter(or_(Usuario.cpf == cpf, Usuario.pis == pis)).first()
    if usuario is not None:
        return jsonify(
            {"message": Globals.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )

    senha_hashed = generate_password_hash(dado.get("senha"), method="sha256")
    email = dado.get("email").lower()

    # Cadastra o endereço
    endereco = Endereco()
    for campo in ["cep", "rua", "numero", "bairro", "complemento", "municipio_id"]:
        if dado.get(campo):
            setattr(endereco, campo, dado.get(campo))
    db.session.add(endereco)
    db.session.flush()
    # Cadastra o usuario
    usuario = Usuario()
    for campo in ["nome", "pis", "cpf"]:
        if dado.get(campo):
            setattr(usuario, campo, dado.get(campo))
    # Adiciona o id do endereço
    usuario.endereco_id = endereco.id
    db.session.add(usuario)

    try:
        db.session.flush()

        login = Login(
            email=email,
            senha=senha_hashed,
            usuario_id=usuario.id,
            acesso_id=2,
        )

        db.session.add(login)

        db.session.commit()
        return jsonify(
            {
                "message": Globals.REGISTER_SUCCESS_CREATED.format("Login"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Globals.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


@app.route("/login/add", methods=["PUT"])
@jwt_required
@field_validator(LoginModel)
def loginCreation():
    """Adiciona registro
    ---
    put:
        security:
            - jwt: []
        summary: Adiciona um registro
        requestBody:
            description: Dados necessários para a criação do registro
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/LoginModel'
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

    login = Login.query.get(get_jwt_identity())
    # Caso o login nao seja adminitrador ele nao deve conseguir criar um login
    if login.acesso.nome != "administracao":
        return jsonify({"message": Globals.AUTH_USER_DENIED, "error": True})

    # Checa a existencia de email ja cadastrado
    if Login.query.filter_by(email=dado.get("email").lower()).first():
        return jsonify(
            {"message": Globals.ALREADY_EXISTS.format("email"), "error": True}
        )

    senha_hashed = generate_password_hash(dado.get("senha"), method="sha256")
    email = dado.get("email").lower()
    login = Login(
        email=email,
        senha=senha_hashed,
        usuario_id=dado.get("usuario_id"),
        acesso_id=dado.get("acesso_id"),
    )

    db.session.add(login)
    try:
        db.session.commit()
        return jsonify(
            {
                "message": Globals.REGISTER_SUCCESS_CREATED.format("Login"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Globals.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


# R(VIEW,LIST)
@app.route("/login/view/<int:query_id>", methods=["GET"])
@jwt_required
def loginView(query_id: int):
    """Busca registro por ID
    ---
    get:
      security:
        - jwt: []
      summary: Busca o registro do banco se ele existir
      parameters:
        - in: path
          name: query_id
          schema:
            type: integer
          required: true
          description: Identificação única do registro
      responses:
        200:
            description: "Sucesso"
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/LoginModel"
        204:
            description: "Ocorreu um erro"
            content:
                application/json:
                  schema:
                      type: object
                      properties:
                        error:
                          type: string
    """
    login = Login.query.get(get_jwt_identity())

    # Caso o login nao seja adminitrado ele ve a si mesmo
    if login is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )
    if login.acesso.nome != "administracao":
        query_id = login.id

    # Busca o login a ser visto no banco
    login = Login.query.get(query_id)

    if not login:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dict = login.to_dict()
    dict["error"] = False

    return jsonify(dict)


@app.route("/login/view/complete/<int:query_id>", methods=["GET"])
@jwt_required
def loginCompleteView(query_id: int):
    """Busca registro por ID
    ---
    get:
      security:
        - jwt: []
      summary: Busca o registros do banco se ele existir
      parameters:
        - in: path
          name: query_id
          schema:
            type: integer
          required: true
          description: Identificação única do registro
      responses:
        200:
            description: "Sucesso"
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/LoginModel"
        204:
            description: "Ocorreu um erro"
            content:
                application/json:
                  schema:
                      type: object
                      properties:
                        error:
                          type: string
    """
    login_atual = Login.query.get(get_jwt_identity())
    if login_atual is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )

    query = Login.query.get(query_id)
    if login_atual.acesso.nome != "administracao" or login_atual.id != query.id:
        return jsonify({"message": Globals.AUTH_USER_DENIED, "error": True})

    return (
        jsonify(
            query.to_dict_complete()
        ),
        200,
    )


@app.route("/login/list", methods=["GET"])
@jwt_required
def loginList():
    """Busca lista de registros
    ---
    get:
        security:
            - jwt: []
        summary: Busca lista de registro existentes no banco
        parameters:
            - name: email
              in: query
              description: email para filtro
              required: false
              schema:
                type: string
        responses:
            200:
                description: "Sucesso"
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                count:
                                    type: integer
                                items:
                                    type: array
                                    items:
                                        $ref: "#/components/schemas/LoginModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    email_filter = request.args.get("email", None)

    query = Login.query

    if email_filter is not None:
        query = query.filter(Login.email.ilike("%%{}%%".format(email_filter.lower())))

    logins, dados = paginate(query, page, rows_per_page)

    for login in logins:
        dados["itens"].append(login.to_dict())

    return jsonify(dados)

@app.route("/login/list/complete", methods=["GET"])
@jwt_required
def loginCompleteList():
    """Busca registro por ID
    ---
    get:
      security:
        - jwt: []
      summary: Busca o registros do banco se ele existir
      parameters:
        - in: path
          name: Filter
          schema:
            type: integer
          required: true
          description: Identificação única do registro
      responses:
        200:
            description: "Sucesso"
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/LoginModel"
        204:
            description: "Ocorreu um erro"
            content:
                application/json:
                  schema:
                      type: object
                      properties:
                        error:
                          type: string
    """
    login_atual = Login.query.get(get_jwt_identity())
    if login_atual is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )
    if login_atual.acesso.nome != "administracao":
        return jsonify({"message": Globals.AUTH_USER_DENIED, "error": True})

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    email_filter = request.args.get("email", None)
    nome_filter = request.args.get("nome", None)

    query = Login.query

    if email_filter is not None:
        query = query.filter(Login.email.ilike("%%{}%%".format(email_filter.lower())))
    elif email_filter is not None:
        query = query.filter(Login.usuario.nome.ilike("%%{}%%".format(nome_filter)))

    logins, dados = paginate(query, page, rows_per_page)

    for login in logins:
        dados["itens"].append(login.to_dict_complete())

    return jsonify(dados)

# U
@app.route("/login/update/<int:query_id>", methods=["PUT"])
@jwt_required
@field_validator(LoginModel)
def loginUpdate(query_id: int):
    """Adiciona registro
    ---
    put:
        security:
            - jwt: []
        summary: Edita um registro
        parameters:
            - in: path
              name: query_id
              schema:
                type: integer
              required: true
              description: Identificação única do registro
        requestBody:
            description: Dados necessários para a edição do registro
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/LoginModel'
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

    login = Login.query.get(get_jwt_identity())

    # Login edita a si mesmo
    if login is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )
    if login.acesso.nome != "administracao":
        query_id = login.id

    # recebe os dados do login a ser editado
    edit = Login.query.get(query_id)
    if not edit:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format("login_id"), "error": True}
        )

    # mudança de senha, somente realizado pelo proprio
    if login.id == edit.id:
        # checa a mudança na senha
        if dado.get("senha") is not None:
            senha_hashed = generate_password_hash(dado.get("senha"), method="sha256")
            login.senha = senha_hashed

    for campo in ["email", "usuario_id", "acesso_id"]:
        if dado.get(campo):
            setattr(edit, campo, dado.get(campo))

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Globals.REGISTER_SUCCESS_UPDATED.format("login"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Globals.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )


# D(DELETION)
@app.route("/login/delete/<int:query_id>", methods=["DELETE"])
@jwt_required
def loginDelete(query_id: int):
    """Remove registro por ID
    ---
    delete:
      security:
        - jwt: []
      summary: Remove o registro do banco se ele existir
      parameters:
        - in: path
          name: query_id
          schema:
            type: integer
          required: true
          description: Identificação única do registro
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
    login = Login.query.get(query_id)

    if not login:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    login_atual = Login.query.get(get_jwt_identity())

    if login_atual.acesso.nome != "administracao" and login_atual.id != login.id:
        return jsonify({"message": Globals.USER_INVALID_DELETE, "error": True})

    db.session.delete(login)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Globals.REGISTER_SUCCESS_DELETED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        return jsonify(
            {"message": Globals.REGISTER_DELETE_INTEGRITY_ERROR, "error": True}
        )
