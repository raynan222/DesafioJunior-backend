import re

from flask import request, jsonify
from sqlalchemy import or_
from sqlalchemy import exc
from flask_jwt_extended import get_jwt_identity, jwt_required
from application.app import app, db
from source.controller import paginate, Globals, field_validator
from source.model import Login
from source.model.usuarioTable import Usuario, UsuarioModel


# C
@app.route("/usuario/add", methods=["PUT"])
@jwt_required
@field_validator(UsuarioModel)
def usuarioCreation():
    """Adiciona registro
    ---
    put:
        tags: [Rotas]
        security:
            - jwt: []
        summary: Adiciona um registro
        parameters:
          - name: nome
            in: query
            description: Nome para filtro
            required: false
            schema:
                type: string
        requestBody:
            description: Dados necessários para a criação do registro
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/UsuarioModel'
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
    dados = request.get_json()

    # checa se existe cadastro do pis ou cpf
    cpf = re.sub("[^\d]", "", dados["cpf"])
    pis = re.sub("[^\d]", "", dados["pis"])
    usuario = Usuario.query.filter(or_(Usuario.cpf == cpf, Usuario.pis == pis)).first()
    if usuario is not None:
        return jsonify(
            {"message": Globals.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )

    usuario = Usuario(
        nome=dados["nome"],
        pis=re.sub("[^\d]", "", dados["pis"]),
        cpf=re.sub("[^\d]", "", dados["cpf"]),
        endereco_id=dados["endereco_id"],
    )

    db.session.add(usuario)

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


# R(VIEW, LIST)
@app.route("/usuario/view/<int:query_id>", methods=["GET"])
@jwt_required
def usuarioView(query_id: int):
    """Busca registro por ID
    ---
    get:
      tags: [Rotas]
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
                        $ref: "#/components/schemas/UsuarioModel"
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

    if login is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )
    if login.acesso.id != 1:
        query_id = login.usuario_id

    usuario = Usuario.query.get(query_id)

    if not usuario:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dic = usuario.to_dict()
    dic["error"] = False

    return jsonify(dic)


@app.route("/usuario/list", methods=["GET"])
@jwt_required
def usuarioList():
    """Busca lista de registros
    ---
    get:
        tags: [Rotas]
        security:
            - jwt: []
        summary: Busca lista de registro existentes no banco
        parameters:
            - name: nome
              in: query
              description: Nome de usuario para filtro
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
                                        $ref: "#/components/schemas/UsuarioModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    nome_filter = request.args.get("nome", None)

    query = Usuario.query

    if nome_filter is not None:
        query = query.filter(Usuario.nome.ilike("%%{}%%".format(nome_filter.lower())))

    usuarios, dados = paginate(query, page, rows_per_page)

    for usuario in usuarios:
        dados["itens"].append(usuario.to_dict())

    return jsonify(dados)


# U
@app.route("/usuario/update/<int:query_id>", methods=["PUT"])
@jwt_required
@field_validator(UsuarioModel)
def usuarioUpdate(query_id: int):
    """Adiciona registro
    ---
    put:
        tags: [Rotas]
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
                  $ref: '#/components/schemas/UsuarioModel'
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
    # Usuario edita a si mesmo caso nao seja adminitador
    if login is None:
        return jsonify(
            {
                "message": Globals.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )
    if login.acesso.id != 1:
        query_id = login.usuario_id

    # recebe os dados do usuario a ser editado
    edit = Usuario.query.get(query_id)
    if not edit:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    # checa validade dos dados
    cpf = str()
    if dado.get("cpf") is not None:
        dado["cpf"] = re.sub("[^\d]", "", dado.get("cpf"))
        cpf = dado["cpf"]

    pis = str()
    if dado.get("pis") is not None:
        dado["pis"] = re.sub("[^\d]", "", dado.get("pis"))
        pis = dado["pis"]

    existente = Usuario.query.filter(
        or_(Usuario.cpf == cpf, Usuario.pis == pis)
    ).first()
    if existente is not None:
        return jsonify(
            {"message": Globals.ALREADY_EXISTS.format("CPF/PIS"), "error": True}
        )

    for campo in ["nome", "cpf", "pis"]:
        if dado.get(campo):
            setattr(edit, campo, dado.get(campo))
    try:
        db.session.commit()
        return jsonify(
            {
                "message": Globals.REGISTER_SUCCESS_UPDATED.format("usuario"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Globals.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )


# D(DELETION)
@app.route("/usuario/delete/<int:query_id>", methods=["DELETE"])
@jwt_required
def usuarioDelete(query_id: int):
    """Remove registro por ID
    ---
    delete:
      tags: [Rotas]
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
    usuario = Usuario.query.get(query_id)

    if not usuario:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    login = Login.query.get(get_jwt_identity())

    if login.acesso.id != 1 or login.usuario_id == usuario.id:
        return jsonify({"message": Globals.USER_INVALID_DELETE, "error": True})

    db.session.delete(usuario)

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
