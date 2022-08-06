## Builds




#### Imagens separados

````shell
# Executar a parte da raiz dos dois projetos

docker build -t desafio-junior-backend -f DesafioJunior-backend/build/backend.Dockerfile .

docker build -t desafio-junior-frontend -f DesafioJunior-backend/build/frontend.Dockerfile .

docker build -t desafio-junior-postgres -f DesafioJunior-backend/build/postgres.Dockerfile .


docker compose --project-directory . -f DesafioJunior-backend/build/docker-compose.yaml up

docker compose --project-directory . --env-file DesafioJunior-backend/.env -f desafioJunior-backend/build/docker-compose.yaml up --force-recreate   


docker compose --project-directory . --env-file DesafioJunior-backend/.env.dev -f desafioJunior-backend/build/docker-compose.yaml -f desafioJunior-backend/build/docker-compose.dev.yaml up --force-recreate   



````