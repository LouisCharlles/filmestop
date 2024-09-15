# FilmesTop - Sistema de Aluguel de Filmes

Este é um projeto Django para gerenciar o aluguel de filmes. Ele permite que os usuários visualizem os filmes disponíveis, façam o aluguel e avaliem os filmes alugados.

## Pré-requisitos

Antes de começar, você precisará ter os seguintes itens instalados em sua máquina:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Certifique-se de que o Docker está rodando corretamente.

## Variáveis de Ambiente

Você precisará de um arquivo `.env` na raiz do projeto. Ele deve conter as variáveis de ambiente necessárias para o Django, como exemplo:

SECRET_KEY=your_secret_key DEBUG=True ALLOWED_HOSTS=localhost,127.0.0.1 DATABASE_URL=postgres://user
@db:5432/filmestop


Certifique-se de ajustar essas variáveis conforme necessário para o seu ambiente.

## Instruções para Executar o Projeto

1. **Clone o repositório:**

   Clone este repositório para a sua máquina local usando o comando:

   ```bash
   git clone https://github.com/usuario/filmestop.git

2. **Navegue até o diretório do projeto:**

    Entre no diretório do projeto: 
    ```bash
    cd filmestop

3. **Configure o Docker:**

    Certifique-se de que o arquivo `Dockerfile` e o arquivo `docker-compose.yml` estão corretamente configurados. Se você não tiver o arquivo `docker-compose.yml`, pode adicionar o seguinte:

```bash
version: '3'

services:
  web:
    build: .
    command: gunicorn setup.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/filmestop
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: filmestop
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:

```
4. **Construir e executar o container:**

    Execute os comandos abaixo para construir e iniciar o container

    ```
    docker-compose build
    docker-compose up
Isso irá construir a imagem Docker e iniciar o projeto. O Django estará acessível em http://localhost:8000.

5. **Rodar migrações:**

    Após a inicialização do container, abra um novo terminal e execute as migrações do banco de dados:

    ```
    docker-compose exec web python manage.py migrate

6. **Criar superusuário:**

    Para acessar a área administrativa do Django, crie um superusuário executando o comando: 

    ```
    docker-compose exec web python manage.py createsuperuser

7. **Acessar aplicação:**

    Agora você pode acessar a aplicação através do navegador no endereço:

    ```
    http://localhost:8000
    ```
    A área administrativa estará disponível em http://localhost:8000/admin.

## Testes

Você pode executar os testes do Django dentro do container com o comando:

    docker-compose exec web python manage.py test

## Contribuição
Sinta-se à vontade para abrir issues ou pull requests no repositório para sugestões ou correções.