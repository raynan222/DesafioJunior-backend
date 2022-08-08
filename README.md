# DesafioJunior-backend
Api simples para cadastro de usuário, foram utilizados como principais frameworks Flask, Pydantic, SQLAlchemy, além de Swagger para documentação.

## Docker
Para executar o docker é necessário respeita a hierarquia de pastas a seguir
```
├─DesafioJunior-backend
│  ├─application
│  ├─build
│  │  ├─config
│  │  │  └─postgres.conf
│  │  ├─backend.Dockerfile
│  │  ├─docker-compose.dev.yaml
│  │  ├─docker-compose.yaml
│  │  ├─frontend.Dockerfile
│  │  ├─poetry.lock
│  │  ├─postgres.Dockerfile
│  │  ├─pyproject.toml
│  │  └─README.md
│  ├─migrations
│  ├─source
│  ├─tests
│  ├─utils
│  ├─.env
│  ├─.env.dev
│  ├─.env.local
│  ├─.gitignore
│  ├─config.py
│  ├─file.py
│  ├─Makefile
│  └─Procfile
└─DesafioJunior-frontend
```
Na pasta DesafioJunior-backend execute o comando:
> docker compose --project-directory ../ --env-file .env.dev -f build/docker-compose.yaml -f build/docker-compose.dev.yaml up --force-recreate --build

A aplicação fica acessivel em localhost:3000/

## Configuração do banco

Para gerar as tabelas deve ser executado os seguintes comandos:
> python run.py db init <br> python run.py db migrate <br> python run.py db upgrade

Para popular o banco execute:
> python run.py populate

Um usuário administrador sera gerado.
> Login: admin@local.com <br> Senha: admin

## Testes

Para primeiro uso é necessário acessar o banco através do docker e usar os comandos
> psql -U postgres <br> CREATE TABLE web_app_pytest;

## Documentação
A documentação pode ser acessa, enquanto o docker estiver ativo em:
>localhost:5000/api
