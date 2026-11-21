# AutoForce

**Sistema web para gerenciamento de oficinas mecânicas e lojas de autopeças.**

## 1. Sobre o projeto

O AutoForce é um sistema desenvolvido para facilitar a administração de oficinas mecânicas e lojas de autopeças, centralizando informações de clientes, veículos, funcionários, peças, estoque e ordens de serviço.

Projeto acadêmico desenvolvido no Centro Universitário dos Guararapes (UNIFG).

## 2. Funcionalidades

- Cadastro, consulta, edição e exclusão de clientes.
- Gerenciamento de veículos.
- Cadastro e gerenciamento de funcionários.
- Cadastro e gerenciamento de peças.
- Controle de entrada e saída de estoque.
- Criação e acompanhamento de ordens de serviço.
- Associação de veículos e funcionários às ordens de serviço.
- Adição de peças às ordens de serviço.
- Baixa automática de peças utilizadas no estoque.
- Atualização do status das ordens de serviço.
- Relatórios administrativos.

## 3. Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Fetch API

## 4. Banco de dados

O sistema utiliza SQLite, com sete tabelas principais:

1. Clientes
2. Veículos
3. Funcionários
4. Peças
5. Ordens de serviço
6. Itens de ordem de serviço
7. Movimentações de estoque

O banco de dados e suas tabelas são criados automaticamente durante a inicialização do sistema.

O arquivo do banco de dados é local e não precisa ser enviado ao GitHub.

## 5. API

O projeto possui uma API desenvolvida com Flask, localizada no arquivo `api.py`.

A API disponibiliza operações para gerenciamento de veículos:

- GET: consultar veículos.
- POST: cadastrar veículos.
- PUT: atualizar veículos.
- DELETE: excluir veículos.

A interface do módulo de veículos consome a API utilizando JavaScript e Fetch API, com comunicação por dados JSON.

## 6. Como executar o projeto

### Requisitos

- Python instalado.
- Git instalado ou possibilidade de baixar o projeto pelo GitHub.

### 1. Clonar o repositório

```bash
git clone https://github.com/vinigcs/AutoForce.git
```

### 2. Entrar na pasta

```bash
cd AutoForce
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual (Windows)

```bash
venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Iniciar a aplicação web

Em um primeiro terminal:

```bash
python app.py
```

### 7. Iniciar a API

Em um segundo terminal, com o ambiente virtual ativado:

```bash
python api.py
```

### 8. Acessar o sistema

Aplicação web:

http://127.0.0.1:5000

API de veículos:

http://127.0.0.1:5001/api/veiculos

**Importante:** os dois servidores precisam permanecer em execução para o funcionamento completo do sistema.

## 7. Desenvolvedores

Projeto acadêmico desenvolvido no Centro Universitário dos Guararapes (UNIFG).

Orientador: Prof. Me. Petros Barreto da Silva.

## 8. Status do projeto

Projeto desenvolvido para fins acadêmicos, contendo interface web, API integrada ao módulo de veículos e banco de dados SQLite.