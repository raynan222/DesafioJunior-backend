## Builds




#### Imagens separados

````shell
# Executar a parte da raiz dos dois projetos

docker build -t desafio-junior-backend -f desafioJunior-backend/build/backend.Dockerfile .

docker build -t desafio-junior-frontend -f desafioJunior-backend/build/frontend.Dockerfile .

docker build -t desafio-junior-postgres -f desafioJunior-backend/build/postgres.Dockerfile .


docker compose --project-directory . -f desafioJunior-backend/build/docker-compose.yaml up

docker compose --project-directory . -f desafioJunior-backend/build/docker-compose.yaml up --force-recreate   


````