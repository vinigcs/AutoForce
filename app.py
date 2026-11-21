from flask import Flask, render_template, request, redirect, url_for
from database.db import conectar, criar_tabelas
from datetime import datetime
import sqlite3

app = Flask(__name__)

criar_tabelas()

STATUS_OS = [
    "Aberta",
    "Em diagnóstico",
    "Aguardando aprovação",
    "Em execução",
    "Finalizada",
    "Entregue"
]


# PÁGINA INICIAL

@app.route("/")
def inicio():
    return render_template("index.html")


# GESTÃO DE CLIENTES

@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"] or None
        telefone = request.form["telefone"]
        email = request.form["email"] or None

        conexao = conectar()

        try:
            conexao.execute("""
                INSERT INTO clientes (nome, cpf, telefone, email)
                VALUES (?, ?, ?, ?)
            """, (nome, cpf, telefone, email))
            conexao.commit()

        except sqlite3.IntegrityError:
            conexao.close()
            return "Erro: este CPF já está cadastrado."

        conexao.close()
        return redirect(url_for("clientes"))

    conexao = conectar()
    lista_clientes = conexao.execute(
        "SELECT * FROM clientes ORDER BY id DESC"
    ).fetchall()
    conexao.close()

    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conexao = conectar()

    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"] or None
        telefone = request.form["telefone"]
        email = request.form["email"] or None

        try:
            conexao.execute("""
                UPDATE clientes
                SET nome = ?, cpf = ?, telefone = ?, email = ?
                WHERE id = ?
            """, (nome, cpf, telefone, email, id))
            conexao.commit()

        except sqlite3.IntegrityError:
            conexao.close()
            return "Erro: este CPF já pertence a outro cliente."

        conexao.close()
        return redirect(url_for("clientes"))

    cliente = conexao.execute(
        "SELECT * FROM clientes WHERE id = ?", (id,)
    ).fetchone()

    conexao.close()

    if cliente is None:
        return "Cliente não encontrado.", 404

    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/clientes/excluir/<int:id>", methods=["POST"])
def excluir_cliente(id):
    conexao = conectar()

    try:
        conexao.execute(
            "DELETE FROM clientes WHERE id = ?", (id,)
        )
        conexao.commit()

    except sqlite3.IntegrityError:
        conexao.close()
        return "Não é possível excluir um cliente que possui veículos cadastrados."

    conexao.close()
    return redirect(url_for("clientes"))


# GESTÃO DE VEÍCULOS

@app.route("/veiculos", methods=["GET", "POST"])
def veiculos():
    conexao = conectar()

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        placa = request.form["placa"].strip().upper()
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        ano = request.form["ano"] or None
        tipo = request.form["tipo"]

        try:
            conexao.execute("""
                INSERT INTO veiculos
                (cliente_id, placa, marca, modelo, ano, tipo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cliente_id, placa, marca, modelo, ano, tipo))
            conexao.commit()

        except sqlite3.IntegrityError:
            conexao.close()
            return "Erro: placa já cadastrada ou dados inválidos."

        conexao.close()
        return redirect(url_for("veiculos"))

    lista_clientes = conexao.execute(
        "SELECT * FROM clientes ORDER BY nome"
    ).fetchall()

    lista_veiculos = conexao.execute("""
        SELECT veiculos.*, clientes.nome AS cliente_nome
        FROM veiculos
        JOIN clientes ON veiculos.cliente_id = clientes.id
        ORDER BY veiculos.id DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "veiculos.html",
        clientes=lista_clientes,
        veiculos=lista_veiculos
    )


@app.route("/veiculos/editar/<int:id>", methods=["GET", "POST"])
def editar_veiculo(id):
    conexao = conectar()

    veiculo = conexao.execute("""
        SELECT * FROM veiculos WHERE id = ?
    """, (id,)).fetchone()

    if veiculo is None:
        conexao.close()
        return "Veículo não encontrado.", 404

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        placa = request.form["placa"].strip().upper()
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        ano = request.form["ano"] or None
        tipo = request.form["tipo"]

        try:
            conexao.execute("""
                UPDATE veiculos
                SET cliente_id = ?, placa = ?, marca = ?,
                    modelo = ?, ano = ?, tipo = ?
                WHERE id = ?
            """, (
                cliente_id, placa, marca, modelo,
                ano, tipo, id
            ))
            conexao.commit()

        except sqlite3.IntegrityError:
            conexao.close()
            return "Erro: placa já cadastrada ou dados inválidos."

        conexao.close()
        return redirect(url_for("veiculos"))

    lista_clientes = conexao.execute("""
        SELECT * FROM clientes ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "editar_veiculo.html",
        veiculo=veiculo,
        clientes=lista_clientes
    )


@app.route("/veiculos/excluir/<int:id>", methods=["POST"])
def excluir_veiculo(id):
    conexao = conectar()

    try:
        cursor = conexao.execute("""
            DELETE FROM veiculos WHERE id = ?
        """, (id,))
        conexao.commit()

        if cursor.rowcount == 0:
            conexao.close()
            return "Veículo não encontrado.", 404

    except sqlite3.IntegrityError:
        conexao.close()
        return (
            "Não é possível excluir este veículo, "
            "pois ele possui Ordens de Serviço vinculadas."
        )

    conexao.close()
    return redirect(url_for("veiculos"))


# GESTÃO DE FUNCIONÁRIOS

@app.route("/funcionarios", methods=["GET", "POST"])
def funcionarios():
    conexao = conectar()

    if request.method == "POST":
        nome = request.form["nome"]
        cargo = request.form["cargo"]
        telefone = request.form["telefone"] or None

        conexao.execute("""
            INSERT INTO funcionarios (nome, cargo, telefone)
            VALUES (?, ?, ?)
        """, (nome, cargo, telefone))

        conexao.commit()
        conexao.close()

        return redirect(url_for("funcionarios"))

    lista_funcionarios = conexao.execute("""
        SELECT * FROM funcionarios ORDER BY id DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "funcionarios.html",
        funcionarios=lista_funcionarios
    )


@app.route("/funcionarios/editar/<int:id>", methods=["GET", "POST"])
def editar_funcionario(id):
    conexao = conectar()

    funcionario = conexao.execute("""
        SELECT * FROM funcionarios WHERE id = ?
    """, (id,)).fetchone()

    if funcionario is None:
        conexao.close()
        return "Funcionário não encontrado.", 404

    if request.method == "POST":
        nome = request.form["nome"]
        cargo = request.form["cargo"]
        telefone = request.form["telefone"] or None

        conexao.execute("""
            UPDATE funcionarios
            SET nome = ?, cargo = ?, telefone = ?
            WHERE id = ?
        """, (nome, cargo, telefone, id))

        conexao.commit()
        conexao.close()

        return redirect(url_for("funcionarios"))

    conexao.close()

    return render_template(
        "editar_funcionario.html",
        funcionario=funcionario
    )


@app.route("/funcionarios/excluir/<int:id>", methods=["POST"])
def excluir_funcionario(id):
    conexao = conectar()

    try:
        cursor = conexao.execute("""
            DELETE FROM funcionarios WHERE id = ?
        """, (id,))

        conexao.commit()

        if cursor.rowcount == 0:
            conexao.close()
            return "Funcionário não encontrado.", 404

    except sqlite3.IntegrityError:
        conexao.close()
        return (
            "Não é possível excluir este funcionário, "
            "pois ele está vinculado a uma ou mais Ordens de Serviço."
        )

    conexao.close()
    return redirect(url_for("funcionarios"))


# GESTÃO DE PEÇAS

@app.route("/pecas", methods=["GET", "POST"])
def pecas():
    conexao = conectar()

    if request.method == "POST":
        nome = request.form["nome"]
        marca = request.form["marca"] or None

        try:
            quantidade = int(request.form["quantidade"])
            preco = float(request.form["preco"])

            if quantidade < 0 or preco < 0:
                raise ValueError

            conexao.execute("""
                INSERT INTO pecas (nome, marca, quantidade, preco)
                VALUES (?, ?, ?, ?)
            """, (nome, marca, quantidade, preco))

            conexao.commit()

        except (ValueError, sqlite3.IntegrityError):
            conexao.close()
            return "Erro: verifique a quantidade e o preço informados."

        conexao.close()
        return redirect(url_for("pecas"))

    lista_pecas = conexao.execute("""
        SELECT * FROM pecas ORDER BY id DESC
    """).fetchall()

    conexao.close()

    return render_template("pecas.html", pecas=lista_pecas)


@app.route("/pecas/editar/<int:id>", methods=["GET", "POST"])
def editar_peca(id):
    conexao = conectar()

    peca = conexao.execute("""
        SELECT * FROM pecas WHERE id = ?
    """, (id,)).fetchone()

    if peca is None:
        conexao.close()
        return "Peça não encontrada.", 404

    if request.method == "POST":
        nome = request.form["nome"]
        marca = request.form["marca"] or None

        try:
            preco = float(request.form["preco"])

            if preco < 0:
                raise ValueError

            conexao.execute("""
                UPDATE pecas
                SET nome = ?, marca = ?, preco = ?
                WHERE id = ?
            """, (nome, marca, preco, id))

            conexao.commit()

        except ValueError:
            conexao.close()
            return "Erro: informe um preço válido."

        conexao.close()
        return redirect(url_for("pecas"))

    conexao.close()

    return render_template("editar_peca.html", peca=peca)


@app.route("/pecas/excluir/<int:id>", methods=["POST"])
def excluir_peca(id):
    conexao = conectar()

    try:
        cursor = conexao.execute("""
            DELETE FROM pecas WHERE id = ?
        """, (id,))

        conexao.commit()

        if cursor.rowcount == 0:
            conexao.close()
            return "Peça não encontrada.", 404

    except sqlite3.IntegrityError:
        conexao.close()
        return (
            "Não é possível excluir esta peça, pois ela possui "
            "histórico de movimentação ou utilização em Ordens de Serviço."
        )

    conexao.close()
    return redirect(url_for("pecas"))


# MOVIMENTAÇÃO DE ESTOQUE

@app.route("/estoque", methods=["GET", "POST"])
def estoque():
    conexao = conectar()

    if request.method == "POST":
        peca_id = request.form["peca_id"]
        tipo = request.form["tipo"]
        descricao = request.form["descricao"] or None

        try:
            quantidade = int(request.form["quantidade"])

            if quantidade <= 0 or tipo not in ("Entrada", "Saida"):
                raise ValueError

            conexao.execute("BEGIN IMMEDIATE")

            peca = conexao.execute("""
                SELECT * FROM pecas WHERE id = ?
            """, (peca_id,)).fetchone()

            if peca is None:
                conexao.rollback()
                conexao.close()
                return "Erro: peça não encontrada."

            if tipo == "Entrada":
                conexao.execute("""
                    UPDATE pecas
                    SET quantidade = quantidade + ?
                    WHERE id = ?
                """, (quantidade, peca_id))

            else:
                cursor = conexao.execute("""
                    UPDATE pecas
                    SET quantidade = quantidade - ?
                    WHERE id = ? AND quantidade >= ?
                """, (quantidade, peca_id, quantidade))

                if cursor.rowcount == 0:
                    conexao.rollback()
                    conexao.close()
                    return (
                        "Estoque insuficiente! "
                        f"Quantidade disponível: {peca['quantidade']}."
                    )

            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conexao.execute("""
                INSERT INTO movimentacoes_estoque
                (peca_id, tipo, quantidade, data_movimentacao, descricao)
                VALUES (?, ?, ?, ?, ?)
            """, (peca_id, tipo, quantidade, data_atual, descricao))

            conexao.commit()

        except (ValueError, sqlite3.IntegrityError):
            conexao.rollback()
            conexao.close()
            return "Erro: confira os dados da movimentação."

        conexao.close()
        return redirect(url_for("estoque"))

    lista_pecas = conexao.execute("""
        SELECT * FROM pecas ORDER BY nome
    """).fetchall()

    lista_movimentacoes = conexao.execute("""
        SELECT
            movimentacoes_estoque.*,
            pecas.nome AS peca_nome
        FROM movimentacoes_estoque
        JOIN pecas
            ON movimentacoes_estoque.peca_id = pecas.id
        ORDER BY movimentacoes_estoque.id DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "estoque.html",
        pecas=lista_pecas,
        movimentacoes=lista_movimentacoes
    )


# PEÇAS UTILIZADAS NAS ORDENS DE SERVIÇO

@app.route("/itens-os", methods=["GET", "POST"])
def itens_os():
    conexao = conectar()

    if request.method == "POST":
        try:
            ordem_id = int(request.form["ordem_servico_id"])
            peca_id = int(request.form["peca_id"])
            quantidade = int(request.form["quantidade"])

            if quantidade <= 0:
                raise ValueError

            conexao.execute("BEGIN IMMEDIATE")

            ordem = conexao.execute("""
                SELECT id FROM ordens_servico WHERE id = ?
            """, (ordem_id,)).fetchone()

            peca = conexao.execute("""
                SELECT * FROM pecas WHERE id = ?
            """, (peca_id,)).fetchone()

            if ordem is None:
                conexao.rollback()
                conexao.close()
                return "Erro: Ordem de Serviço não encontrada."

            if peca is None:
                conexao.rollback()
                conexao.close()
                return "Erro: peça não encontrada."

            cursor = conexao.execute("""
                UPDATE pecas
                SET quantidade = quantidade - ?
                WHERE id = ? AND quantidade >= ?
            """, (quantidade, peca_id, quantidade))

            if cursor.rowcount == 0:
                conexao.rollback()
                conexao.close()
                return (
                    "Estoque insuficiente! "
                    f"Quantidade disponível: {peca['quantidade']}."
                )

            conexao.execute("""
                INSERT INTO itens_os
                (ordem_servico_id, peca_id, quantidade, valor_unitario)
                VALUES (?, ?, ?, ?)
            """, (ordem_id, peca_id, quantidade, peca["preco"]))

            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conexao.execute("""
                INSERT INTO movimentacoes_estoque
                (peca_id, tipo, quantidade, data_movimentacao, descricao)
                VALUES (?, 'Saida', ?, ?, ?)
            """, (
                peca_id,
                quantidade,
                data_atual,
                f"Utilização na Ordem de Serviço #{ordem_id}"
            ))

            conexao.commit()

        except (ValueError, sqlite3.IntegrityError):
            conexao.rollback()
            conexao.close()
            return "Erro ao adicionar a peça à Ordem de Serviço."

        conexao.close()
        return redirect(url_for("itens_os"))

    lista_ordens = conexao.execute("""
        SELECT
            os.id,
            v.marca,
            v.modelo,
            v.placa
        FROM ordens_servico AS os
        JOIN veiculos AS v ON os.veiculo_id = v.id
        ORDER BY os.id DESC
    """).fetchall()

    lista_pecas = conexao.execute("""
        SELECT * FROM pecas ORDER BY nome
    """).fetchall()

    lista_itens = conexao.execute("""
        SELECT
            itens_os.*,
            pecas.nome AS peca_nome
        FROM itens_os
        JOIN pecas ON itens_os.peca_id = pecas.id
        ORDER BY itens_os.id DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "itens_os.html",
        ordens=lista_ordens,
        pecas=lista_pecas,
        itens=lista_itens
    )


# ORDENS DE SERVIÇO

@app.route("/ordens-servico", methods=["GET", "POST"])
def ordens_servico():
    conexao = conectar()

    if request.method == "POST":
        veiculo_id = request.form["veiculo_id"]
        funcionario_id = request.form["funcionario_id"] or None
        data_entrada = request.form["data_entrada"]
        descricao_problema = request.form["descricao_problema"]

        try:
            valor_mao_obra = float(request.form["valor_mao_obra"] or 0)

            if valor_mao_obra < 0:
                raise ValueError

            conexao.execute("""
                INSERT INTO ordens_servico
                (veiculo_id, funcionario_id, data_entrada,
                 descricao_problema, valor_mao_obra)
                VALUES (?, ?, ?, ?, ?)
            """, (
                veiculo_id,
                funcionario_id,
                data_entrada,
                descricao_problema,
                valor_mao_obra
            ))

            conexao.commit()

        except (sqlite3.IntegrityError, ValueError):
            conexao.close()
            return "Erro ao cadastrar a ordem de serviço."

        conexao.close()
        return redirect(url_for("ordens_servico"))

    lista_veiculos = conexao.execute("""
        SELECT * FROM veiculos ORDER BY modelo
    """).fetchall()

    lista_funcionarios = conexao.execute("""
        SELECT * FROM funcionarios ORDER BY nome
    """).fetchall()

    lista_ordens = conexao.execute("""
        SELECT
            os.*,
            v.marca,
            v.modelo,
            v.placa,
            f.nome AS funcionario_nome,
            COALESCE(itens.total_pecas, 0) AS total_pecas,
            os.valor_mao_obra + COALESCE(itens.total_pecas, 0)
                AS valor_total
        FROM ordens_servico AS os
        JOIN veiculos AS v
            ON os.veiculo_id = v.id
        LEFT JOIN funcionarios AS f
            ON os.funcionario_id = f.id
        LEFT JOIN (
            SELECT
                ordem_servico_id,
                SUM(quantidade * valor_unitario) AS total_pecas
            FROM itens_os
            GROUP BY ordem_servico_id
        ) AS itens
            ON itens.ordem_servico_id = os.id
        ORDER BY os.id DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "ordens_servico.html",
        veiculos=lista_veiculos,
        funcionarios=lista_funcionarios,
        ordens=lista_ordens,
        status_os=STATUS_OS
    )


# EDITAR ORDEM DE SERVIÇO

@app.route("/ordens-servico/editar/<int:id>", methods=["GET", "POST"])
def editar_os(id):
    conexao = conectar()

    ordem = conexao.execute("""
        SELECT * FROM ordens_servico WHERE id = ?
    """, (id,)).fetchone()

    if ordem is None:
        conexao.close()
        return "Ordem de Serviço não encontrada.", 404

    if request.method == "POST":
        veiculo_id = request.form["veiculo_id"]
        funcionario_id = request.form["funcionario_id"] or None
        data_entrada = request.form["data_entrada"]
        descricao_problema = request.form["descricao_problema"]

        try:
            valor_mao_obra = float(request.form["valor_mao_obra"] or 0)

            if valor_mao_obra < 0:
                raise ValueError

            conexao.execute("""
                UPDATE ordens_servico
                SET veiculo_id = ?,
                    funcionario_id = ?,
                    data_entrada = ?,
                    descricao_problema = ?,
                    valor_mao_obra = ?
                WHERE id = ?
            """, (
                veiculo_id,
                funcionario_id,
                data_entrada,
                descricao_problema,
                valor_mao_obra,
                id
            ))

            conexao.commit()

        except (ValueError, sqlite3.IntegrityError):
            conexao.close()
            return "Erro: confira os dados informados na Ordem de Serviço."

        conexao.close()
        return redirect(url_for("ordens_servico"))

    lista_veiculos = conexao.execute("""
        SELECT * FROM veiculos ORDER BY modelo
    """).fetchall()

    lista_funcionarios = conexao.execute("""
        SELECT * FROM funcionarios ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "editar_os.html",
        ordem=ordem,
        veiculos=lista_veiculos,
        funcionarios=lista_funcionarios
    )


# EXCLUIR ORDEM DE SERVIÇO

@app.route("/ordens-servico/excluir/<int:id>", methods=["POST"])
def excluir_os(id):
    conexao = conectar()

    ordem = conexao.execute("""
        SELECT id FROM ordens_servico WHERE id = ?
    """, (id,)).fetchone()

    if ordem is None:
        conexao.close()
        return "Ordem de Serviço não encontrada.", 404

    itens = conexao.execute("""
        SELECT id FROM itens_os
        WHERE ordem_servico_id = ?
        LIMIT 1
    """, (id,)).fetchone()

    if itens is not None:
        conexao.close()
        return (
            "Não é possível excluir esta Ordem de Serviço, "
            "pois existem peças vinculadas a ela. "
            "O histórico e o estoque foram preservados."
        )

    conexao.execute("""
        DELETE FROM ordens_servico WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("ordens_servico"))


# ATUALIZAR STATUS DA ORDEM DE SERVIÇO

@app.route("/ordens-servico/atualizar-status/<int:id>", methods=["POST"])
def atualizar_status_os(id):
    novo_status = request.form.get("status")

    if novo_status not in STATUS_OS:
        return "Erro: status inválido.", 400

    conexao = conectar()

    ordem = conexao.execute("""
        SELECT id FROM ordens_servico WHERE id = ?
    """, (id,)).fetchone()

    if ordem is None:
        conexao.close()
        return "Ordem de Serviço não encontrada.", 404

    conexao.execute("""
        UPDATE ordens_servico
        SET status = ?
        WHERE id = ?
    """, (novo_status, id))

    conexao.commit()
    conexao.close()

    return redirect(url_for("ordens_servico"))


# RELATÓRIOS

@app.route("/relatorios")
def relatorios():
    conexao = conectar()

    # Quantidade de OS por situação
    os_abertas = conexao.execute("""
        SELECT COUNT(*) AS total
        FROM ordens_servico
        WHERE status = 'Aberta'
    """).fetchone()["total"]

    os_execucao = conexao.execute("""
        SELECT COUNT(*) AS total
        FROM ordens_servico
        WHERE status = 'Em execução'
    """).fetchone()["total"]

    os_finalizadas = conexao.execute("""
        SELECT COUNT(*) AS total
        FROM ordens_servico
        WHERE status IN ('Finalizada', 'Entregue')
    """).fetchone()["total"]

    total_os = conexao.execute("""
        SELECT COUNT(*) AS total
        FROM ordens_servico
    """).fetchone()["total"]

    # Faturamento registrado: mão de obra + peças de todas as OS
    resultado_faturamento = conexao.execute("""
        SELECT
            COALESCE(SUM(
                os.valor_mao_obra + COALESCE(itens.total_pecas, 0)
            ), 0) AS faturamento
        FROM ordens_servico AS os
        LEFT JOIN (
            SELECT
                ordem_servico_id,
                SUM(quantidade * valor_unitario) AS total_pecas
            FROM itens_os
            GROUP BY ordem_servico_id
        ) AS itens
            ON itens.ordem_servico_id = os.id
    """).fetchone()

    faturamento = resultado_faturamento["faturamento"]

    # Peças com cinco unidades ou menos
    pecas_baixo_estoque = conexao.execute("""
        SELECT nome, quantidade
        FROM pecas
        WHERE quantidade <= 5
        ORDER BY quantidade ASC, nome ASC
    """).fetchall()

    # Últimas dez movimentações do estoque
    movimentacoes = conexao.execute("""
        SELECT
            movimentacoes_estoque.tipo,
            movimentacoes_estoque.quantidade,
            movimentacoes_estoque.data_movimentacao,
            pecas.nome AS nome
        FROM movimentacoes_estoque
        JOIN pecas
            ON movimentacoes_estoque.peca_id = pecas.id
        ORDER BY movimentacoes_estoque.id DESC
        LIMIT 10
    """).fetchall()

    conexao.close()

    return render_template(
        "relatorios.html",
        os_abertas=os_abertas,
        os_execucao=os_execucao,
        os_finalizadas=os_finalizadas,
        total_os=total_os,
        faturamento=faturamento,
        pecas_baixo_estoque=pecas_baixo_estoque,
        movimentacoes=movimentacoes
    )


if __name__ == "__main__":
    app.run(debug=True)