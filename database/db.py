import sqlite3
from pathlib import Path

# Caminho do banco de dados
DATABASE_PATH = Path(__file__).resolve().parent / "autoforce.db"


def conectar():
    conexao = sqlite3.connect(DATABASE_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            placa TEXT NOT NULL UNIQUE,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER,
            tipo TEXT NOT NULL CHECK(tipo IN ('Carro', 'Motocicleta')),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL,
            telefone TEXT
        );

        CREATE TABLE IF NOT EXISTS pecas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            marca TEXT,
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0),
            preco REAL NOT NULL DEFAULT 0 CHECK(preco >= 0)
        );

        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL,
            funcionario_id INTEGER,
            data_entrada TEXT NOT NULL,
            descricao_problema TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Aberta',
            valor_mao_obra REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
        );

        CREATE TABLE IF NOT EXISTS itens_os (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ordem_servico_id INTEGER NOT NULL,
            peca_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            valor_unitario REAL NOT NULL,
            FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico(id),
            FOREIGN KEY (peca_id) REFERENCES pecas(id)
        );

        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peca_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('Entrada', 'Saida')),
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            data_movimentacao TEXT NOT NULL,
            descricao TEXT,
            FOREIGN KEY (peca_id) REFERENCES pecas(id)
        );
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados AutoForce criado com sucesso!")   