from flask import request, jsonify
from flask_jwt_extended import jwt_required

from application.app import app
from source.controller import paginate, Messages
from source.model.enderecoTable import Endereco


@app.route("/endereco/view/<int:query_id>", methods=["GET"])
@jwt_required
def enderecoView(query_id: int):

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
    dado["estado_id"] = endereco.estado_id

    return jsonify(dado)

@app.route("/endereco/list", methods=["GET"])
@jwt_required
def enderecoList():

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
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
        dado["estado_id"] = endereco.estado_id

        dados["itens"].append(dado)

    return jsonify(dados)