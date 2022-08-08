import re

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import exc

from application.app import app, db
from source.controller import paginate, Globals, field_validator
from source.model import Login, Municipio, Estado, Pais
from source.model.enderecoTable import Endereco, EnderecoModel


@app.route("/endereco/view/<int:query_id>", methods=["GET"])
@jwt_required
def enderecoView(query_id: int):
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
                        $ref: "#/components/schemas/EnderecoModel"
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
    endereco = Endereco.query.get(query_id)

    if not endereco:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dado = endereco.to_dict_complete()
    dado["error"] = False

    return jsonify(dado)


@app.route("/endereco/list", methods=["GET"])
@jwt_required
def enderecoList():
    """Busca lista de registros
    ---
    get:
        tags: [Rotas]
        security:
            - jwt: []
        summary: Busca lista de registro existentes no banco
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
                                        $ref: "#/components/schemas/EnderecoModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    rua = request.args.get("rua", None)
    query = Endereco.query

    if rua != None:
        query = query.filter(Endereco.rua.ilike("%%{}%%".format(rua)))

    enderecos, dados = paginate(query, page, rows_per_page)

    for endereco in enderecos:
        dados["itens"].append(endereco.to_dict_complete())

    dados["error"] = False
    return jsonify(dados)


@app.route("/municipio/list", methods=["GET"])
def municipioList():
    """Busca lista de registros
    ---
    get:
        tags: [Rotas]
        security:
            - jwt: []
        summary: Busca lista de registro existentes no banco
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
                                        $ref: "#/components/schemas/EnderecoModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    nome_filter = request.args.get("nome", None)
    query = Municipio.query

    if nome_filter is not None:
        query = query.filter(Municipio.nome.ilike("{}%%".format(nome_filter)))

    municipios, dados = paginate(query, page, rows_per_page)

    for municipio in municipios:
        dado = municipio.to_dict()
        dado["estado"] = municipio.estado.nome
        dados["itens"].append(dado)
    dados["error"] = False
    return jsonify(dados)


@app.route("/municipio/view/<int:query_id>", methods=["GET"])
def municipioView(query_id: int):
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
                        $ref: "#/components/schemas/EnderecoModel"
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
    municipio = Municipio.query.get(query_id)

    if not municipio:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dado = municipio.to_dict()
    dado["estado"] = municipio.estado.nome
    dado["error"] = False

    return jsonify(dado)


@app.route("/estado/list", methods=["GET"])
@jwt_required
def estadoList():
    """Busca lista de registros
    ---
    get:
        tags: [Rotas]
        security:
            - jwt: []
        summary: Busca lista de registro existentes no banco
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
                                        $ref: "#/components/schemas/EnderecoModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    nome = request.args.get("nome", None)
    query = Estado.query

    pais_id = request.args.get("pais_id")
    if nome is not None:
        query = query.filter(Estado.pais_id == pais_id)

    estados, dados = paginate(query, page, rows_per_page)

    for estado in estados:
        dados["itens"].append(estado.to_dict())

    return jsonify(dados)


@app.route("/pais/list", methods=["GET"])
@jwt_required
def paisList():
    """Busca lista de registros
    ---
    get:
        tags: [Rotas]
        security:
            - jwt: []
        summary: Busca lista de registro existentes no banco
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
                                        $ref: "#/components/schemas/EnderecoModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )
    nome = request.args.get("nome", None)
    query = Pais.query

    if nome is not None:
        query = query.filter(Pais.nome.ilike("%%{}%%".format(nome)))

    paises, dados = paginate(query, page, rows_per_page)

    for pais in paises:
        dados["itens"].append(pais.to_dict())

    return jsonify(dados)


# U
@app.route("/endereco/update/<int:query_id>", methods=["PUT"])
@jwt_required
@field_validator(EnderecoModel)
def enderecoUpdate(query_id: int):
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
                  $ref: '#/components/schemas/EnderecoModel'
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
    if login.acesso.id != 1:
        query_id = login.usuario.endereco_id

    # recebe os dados do login a ser editado
    edit = Endereco.query.get(query_id)
    if not edit:
        return jsonify(
            {"message": Globals.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    if dado["cep"] is not None:
        dado["cep"] = re.sub("[^\d]", "", dado.get("cep"))
    for campo in ["cep", "rua", "numero", "bairro", "complemento", "municipio_id"]:
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
