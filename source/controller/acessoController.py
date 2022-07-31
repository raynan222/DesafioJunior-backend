from flask import request, jsonify
from flask_jwt_extended import jwt_required
from application.app import app
from source.controller import paginate, Messages
from source.model.acessoTable import Acesso


@app.route("/acesso/view/<int:query_id>", methods=["GET"])
@jwt_required
def acessoView(query_id: int):
    acesso = Acesso.query.get(query_id)

    if not acesso:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(query_id), "error": True}
        )

    dado = {"error": False}
    dado["id"] = acesso.id
    dado["nome"] = acesso.nome

    dado["acesso_id"] = acesso.acesso_id

    return jsonify(dado)

@app.route("/acesso/all", methods=["GET"])
@jwt_required
def acessoList():
    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)

    query = Acesso.query


    acessos, dados = paginate(query, page, rows_per_page)

    for acesso in acessos:
        dado = {}
        dado["id"] = acesso.id
        dado["nome"] = acesso.nome

        dados["itens"].append(dado)

    return jsonify(dados)