.DEFAULT_GOAL := run-app

run-app:
	docker compose --project-directory ../ -f build/docker-compose.yaml up
recreate-app:
	docker compose --project-directory ../ -f build/docker-compose.yaml up --force-recreate
