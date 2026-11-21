# AutoForce

**Sistema web para gerenciamento de oficinas mecânicas e lojas de autopeças.**

## Sobre o projeto

O AutoForce é um sistema desenvolvido com o objetivo de facilitar a administração de oficinas mecânicas e lojas de autopeças, centralizando informações de clientes, veículos, funcionários, peças, estoque e ordens de serviço.

## Funcionalidades

- Cadastro, consulta, edição e exclusão de clientes.
- Cadastro, consulta, edição e exclusão de veículos.
- Cadastro e gerenciamento de funcionários.
- Cadastro e gerenciamento de peças.
- Controle de entrada e saída de estoque.
- Criação e acompanhamento de ordens de serviço.
- Associação de veículos e funcionários às ordens de serviço.
- Adição de peças às ordens de serviço.
- Baixa automática de peças utilizadas no estoque.
- Atualização do status das ordens de serviço.
- Relatórios e indicadores administrativos.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Fetch API

## Banco de dados

O sistema utiliza SQLite e possui sete tabelas principais:

1. Clientes
2. Veículos
3. Funcionários
4. Peças
5. Ordens de serviço
6. Itens de ordem de serviço
7. Movimentações de estoque

O banco de dados utiliza relacionamentos e chaves estrangeiras para manter a integridade das informações.

## API

O projeto possui uma API desenvolvida com Flask, localizada no arquivo `api.py`.

A API disponibiliza operações para gerenciamento de veículos:

- GET: consultar veículos.
- POST: cadastrar veículos.
- PUT: atualizar veículos.
- DELETE: excluir veículos.

A interface do módulo de veículos consome a API utilizando JavaScript e Fetch API, com comunicação por meio de dados JSON.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/vinigcs/AutoForce.git
```

### 2. Entrar na pasta

```bash
cd AutoForce
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instalar dependências

```bash
pip install flask
```

### 6. Iniciar a aplicação web

Em um terminal:

```bash
python app.py
```

### 7. Iniciar a API

Em outro terminal:

```bash
python api.py
```

### 8. Acessar o sistema

Aplicação web:

http://127.0.0.1:5000

API de veículos:

http://127.0.0.1:5001/api/veiculos

## Desenvolvedores

Projeto acadêmico desenvolvido no Centro Universitário dos Guararapes (UNIFG).

Orientador: Prof. Me. Petros Barreto da Silva.

## Status do projeto

**Concluído para fins acadêmicos.**

O sistema possui interface web, API integrada ao módulo de veículos e banco de dados SQLite, com funcionalidades de gerenciamento de clientes, veículos, funcionários, peças, estoque e ordens de serviço.