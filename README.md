# 'Mini' PicPay Simplificado - API Backend

## Descrição

O **PicPay Simplificado** é uma plataforma de pagamentos fictícia onde é possível depositar e realizar transferências de dinheiro entre usuários. O sistema oferece dois tipos de usuários: **usuários comuns** e **lojistas**. Ambos os tipos de usuários possuem carteiras com saldo, e podem realizar transferências entre eles, mas os lojistas só podem receber transferências. Este é um projeto BASEADO no desafio técnico para avaliação de candidatos, conforme o modelo do **PicPay Simplificado**.

## Requisitos do Sistema

- Cadastro de usuários (com CPF único, e-mail único e senha).
- Realização de transferências entre usuários comuns e entre usuários e lojistas.
- Validação de saldo antes de realizar uma transferência.
- Consulta a um serviço de autorização externo para validar a operação de transferência.
- Envio de notificações (por email ou SMS) sobre transferências realizadas (simulado com serviço externo).
- O sistema deve ser **RESTful**.

## Tecnologias Utilizadas

- **Django** como framework.
- **Django REST Framework** para construção da API RESTful.
- **Simple JWT** biblioteca para autenticação via JWT.
- **PostgreSQL** como banco de dados.
- **Docker** para containerização da aplicação.

## Estrutura de Contêineres

O projeto usa o Docker para criar um ambiente isolado para a aplicação e o banco de dados.

### Arquitetura

- **Banco de Dados**: PostgreSQL para armazenamento de dados persistentes.
- **API**: Django com Django REST Framework para criar os endpoints necessários.
- **Notificações via Email**: Serviço de envio de Email para notificação de transferências.
- **Autorização**: Mock de serviço externo para validar a transferência (via `GET`).
- **Containerização**: Docker para facilitar a execução e o ambiente de desenvolvimento.

## Endpoints

### 1. Cadastro de Usuário
- **Endpoint**: `POST /users/register`
- **Descrição**: Registra um novo usuário no sistema.
- **Corpo da Requisição**:
  ```json
  {
    "name": "João Silva",
    "email": "teste.email@gmail.com",
    "cpf": "12345678900",
    "password": "Senha@123",
    "lojista": false
  }

### 2. Login e Geração de Token JWT
- **Endpoint**: `POST /users/token`
- **Descrição**: Registra um novo usuário no sistema.
- **Corpo da Requisição**:
  ```json
  {
    "email": "teste.email@gmail.com",
    "password": "Senha@123",
  }

### 3. Renovação de Token
- **Endpoint**: `POST /users/token`
- **Descrição**: Renova o token de acesso.
- **Corpo da Requisição**:
  ```json
  {
    "refresh": "token..."
  }

### 4. Consulta de conta
- **Endpoint**: `GET /account/`
- **Descrição**: Retorna os detalhes da conta do usuario autenticado.
- **Resposta da Requisição**:
  ```json
  {
  "name": "teste user",
  "balance": "1000.50",
  "transfers": [
    {
      "id": 1,
      "sender": "teste user",
      "receiver": "teste recebedor",
      "value": 1000.50
    }
  ],
  "transactions": [
    {
      "id": 1,
      "status": "completa",
      "transfer": 1
    }
  ]
  }

### 5. Transferência de Dinheiro
- **Endpoint**: `POST /account/transfer`
- **Descrição**: Realiza uma transferência de dinheiro entre usuários.
- **Corpo para Requisição**
  ```json
  {
    "receiver_cpf": "00000000000",
    "value": 1000.50
  }

- OU

  ```json
  {
    "receiver_email": "teste@gmail.com",
    "value": 1000.50
  }

- **Corpo da Resposta**:
  ```json
  {
  "status": "success",
  "message": "Transferência realizada com sucesso.",
  "value": 1000.50,
  "payer": 4,
  "payee": 15
  }


### 6. Depósito na conta
- **Endpoint**: `POST /account/deposit`
- **Descrição**: Realiza uma transferência de dinheiro entre usuários.
- **Corpo para Requisição**
  ```json
  {
    "value": 500.50
  }



## Requisitos

- O sender deve ter saldo suficiente.
- O receiver ou sender pode ser um usuário comum ou lojista.
- O usuario "lojista" não pode realizar tranferências.
- Antes de finalizar, deve ser consultado o serviço de autorização.
- Em caso de falha, a transação deve ser revertida.

## Notificações por Email

- **Endpoint**: Realizado por meio de sistemas de email Django
- Em caso de cadastro de email existente, tanto o sender quanto o receiver receberão emails.

## Autorização

- **Endpoint**: Simulado por meio de um serviço externo.
  - **Método**: `GET` para autorizar a transferência de dinheiro.

## Como Rodar o Projeto

### Pré-requisitos

- **Docker** e **Docker Compose** instalados.
- **Python 3.8+** (para rodar ou desenvolver localmente sem Docker).

### Passos

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/AngelusDaniel/Desafio-Mini-PicPay.git
   cd picpay-simplificado

2. **Rodar os Contêiners docker**: se você estiver utilizando docker,
   basta rodar o comando abaixo para iniciar os containers 

   ```bash
   docker-compose up --build

3. **Rodar localmente (sem Docker)**: 

   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

## Considerações Finais

Certifique-se de que as variáveis de ambiente estão configuradas corretamente, principalmente para o banco de dados e os serviços externos simulados.

Em produção, use variáveis de ambiente para gerenciar credenciais e tokens.

Para autenticação, inclua o token JWT no cabeçalho Authorization de cada requisição protegida:

  ```bash
   curl -H "Authorization: Bearer <seu_token>" <URL_do_endpoint>
  ```

Ou se estiver utilizando Postman. Vá até headers e insira:
Chave: Authorization  
Valor: Bearer seu-token-aqui


#### O projeto foi baseado e não totalmente feito para cumprir o desafio
  Ficou faltando por exemplo, os testes unitários.


