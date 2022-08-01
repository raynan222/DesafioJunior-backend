from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import exc

from application.app import app
from application.database import db
from source.controller import paginate, Messages, field_validator
from source.model import Login
from source.model.enderecoTable import Endereco, EnderecoModel


@app.route("/endereco/view/<int:query_id>", methods=["GET"])
@jwt_required
def enderecoView(query_id: int):
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
            {"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dado = {"error": False}
    dado["id"] = endereco.id
    dado["cep"] = endereco.cep
    dado["rua"] = endereco.rua
    dado["numero"] = endereco.numero
    dado["bairro"] = endereco.bairro
    dado["complemento"] = endereco.complemento
    dado["municipio"] = endereco.municipio_id

    return jsonify(dado)


@app.route("/endereco/list", methods=["GET"])
@jwt_required
def enderecoList():
    """Busca lista de registros
    ---
    get:
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
        dado = {}
        dado["id"] = endereco.id
        dado["cep"] = endereco.cep
        dado["rua"] = endereco.rua
        dado["numero"] = endereco.numero
        dado["bairro"] = endereco.bairro
        dado["complemento"] = endereco.complemento
        dado["municipio"] = endereco.municipio_id

        dados["itens"].append(dado)

    return jsonify(dados)


# U
@app.route("/endereco/update/<int:query_id>", methods=["PUT"])
@jwt_required
@field_validator(EnderecoModel)
def enderecoUpdate(query_id: int):
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
                "message": Messages.REGISTER_NOT_FOUND.format(get_jwt_identity()),
                "error": True,
            }
        )
    if login.acesso.nome != "administração":
        query_id = login.usuario.endereco_id

    # recebe os dados do login a ser editado
    edit = Endereco.query.get(query_id)
    if not edit:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    for campo in ["cep", "rua", "numero", "bairro", "complemento", "municipio_id"]:
        if dado.get(campo):
            print(campo)
            setattr(edit, campo, dado.get(campo))

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_UPDATED.format("login"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )
