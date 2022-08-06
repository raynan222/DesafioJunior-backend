.DEFAULT_GOAL := run-dev

run-dev:
	docker compose --project-directory ../ --env-file .env.dev -f build/docker-compose.yaml -f build/docker-compose.dev.yaml up
recreate-dev:
	docker compose --project-directory ../ --env-file .env.dev -f build/docker-compose.yaml -f build/docker-compose.dev.yaml up --force-recreate
run-app:
	docker compose --project-directory ../ --env-file .env -f build/docker-compose.yaml up
recreate-app:
	docker compose --project-directory ../ --env-file .env -f build/docker-compose.yaml up --force-recreate
