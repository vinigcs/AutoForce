from flask import Flask, jsonify, request
from database.db import conectar, criar_tabelas
import sqlite3

api = Flask(__name__)

criar_tabelas()


# PERMITIR COMUNICACAO ENTRE A INTERFACE E A API
@api.after_request
def adicionar_cors(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5000"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resposta


# LISTAR TODOS OS VEICULOS
@api.route("/api/veiculos", methods=["GET"])
def listar_veiculos():
    conexao = conectar()

    veiculos = conexao.execute("""
        SELECT
            veiculos.*,
            clientes.nome AS cliente_nome
        FROM veiculos
        JOIN clientes ON veiculos.cliente_id = clientes.id
        ORDER BY veiculos.id DESC
    """).fetchall()

    conexao.close()

    return jsonify([dict(v) for v in veiculos]), 200


# CONSULTAR UM VEICULO
@api.route("/api/veiculos/<int:id>", methods=["GET"])
def consultar_veiculo(id):
    conexao = conectar()

    veiculo = conexao.execute("""
        SELECT
            veiculos.*,
            clientes.nome AS cliente_nome
        FROM veiculos
        JOIN clientes ON veiculos.cliente_id = clientes.id
        WHERE veiculos.id = ?
    """, (id,)).fetchone()

    conexao.close()

    if veiculo is None:
        return jsonify({"erro": "Veiculo nao encontrado"}), 404

    return jsonify(dict(veiculo)), 200


# CADASTRAR VEICULO
@api.route("/api/veiculos", methods=["POST"])
def cadastrar_veiculo():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Envie os dados em formato JSON"}), 400

    campos = ["cliente_id", "placa", "marca", "modelo", "tipo"]

    if any(not dados.get(campo) for campo in campos):
        return jsonify({"erro": "Preencha todos os campos obrigatorios"}), 400

    try:
        conexao = conectar()

        cursor = conexao.execute("""
            INSERT INTO veiculos
            (cliente_id, placa, marca, modelo, ano, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            dados["cliente_id"],
            str(dados["placa"]).strip().upper(),
            dados["marca"],
            dados["modelo"],
            dados.get("ano") or None,
            dados["tipo"]
        ))

        conexao.commit()
        novo_id = cursor.lastrowid
        conexao.close()

        return jsonify({
            "mensagem": "Veiculo cadastrado com sucesso",
            "id": novo_id
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "erro": "Placa ja cadastrada ou dados invalidos"
        }), 400


# EDITAR VEICULO
@api.route("/api/veiculos/<int:id>", methods=["PUT"])
def editar_veiculo(id):
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Envie os dados em formato JSON"}), 400

    campos = ["cliente_id", "placa", "marca", "modelo", "tipo"]

    if any(not dados.get(campo) for campo in campos):
        return jsonify({"erro": "Preencha todos os campos obrigatorios"}), 400

    try:
        conexao = conectar()

        cursor = conexao.execute("""
            UPDATE veiculos
            SET cliente_id = ?,
                placa = ?,
                marca = ?,
                modelo = ?,
                ano = ?,
                tipo = ?
            WHERE id = ?
        """, (
            dados["cliente_id"],
            str(dados["placa"]).strip().upper(),
            dados["marca"],
            dados["modelo"],
            dados.get("ano") or None,
            dados["tipo"],
            id
        ))

        conexao.commit()

        if cursor.rowcount == 0:
            conexao.close()
            return jsonify({"erro": "Veiculo nao encontrado"}), 404

        conexao.close()

        return jsonify({
            "mensagem": "Veiculo atualizado com sucesso"
        }), 200

    except sqlite3.IntegrityError:
        return jsonify({
            "erro": "Placa ja cadastrada ou dados invalidos"
        }), 400


# EXCLUIR VEICULO
@api.route("/api/veiculos/<int:id>", methods=["DELETE"])
def excluir_veiculo(id):
    conexao = conectar()

    try:
        cursor = conexao.execute("""
            DELETE FROM veiculos WHERE id = ?
        """, (id,))

        conexao.commit()

        if cursor.rowcount == 0:
            conexao.close()
            return jsonify({"erro": "Veiculo nao encontrado"}), 404

        conexao.close()

        return jsonify({
            "mensagem": "Veiculo excluido com sucesso"
        }), 200

    except sqlite3.IntegrityError:
        conexao.close()
        return jsonify({
            "erro": "Veiculo possui Ordens de Servico vinculadas"
        }), 409


if __name__ == "__main__":
    api.run(port=5001, debug=True)