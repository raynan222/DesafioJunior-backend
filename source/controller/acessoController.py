from flask import request, jsonify
from flask_jwt_extended import jwt_required
from application.app import app
from source.controller import paginate, Messages
from source.model.acessoTable import Acesso


@app.route("/acesso/view/<int:query_id>", methods=["GET"])
@jwt_required
def acessoView(query_id: int):
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
                        $ref: "#/components/schemas/AcessoModel"
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
    acesso = Acesso.query.get(query_id)

    if not acesso:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dict = {"error": False}
    dict["id"] = acesso.id
    dict["nome"] = acesso.nome

    return jsonify(dict)


@app.route("/acesso/all", methods=["GET"])
@jwt_required
def acessoList():
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
                                        $ref: "#/components/schemas/AcessoModel"
                            required:
                                - count
                                - items
    """
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get(
        "rows_per_page", app.config["ROWS_PER_PAGE"], type=int
    )

    query = Acesso.query

    acessos, dados = paginate(query, page, rows_per_page)

    for acesso in acessos:
        dict = {}
        dict["id"] = acesso.id
        dict["nome"] = acesso.nome

        dados["itens"].append(dict)
    return jsonify(dados)
