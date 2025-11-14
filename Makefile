help:
	@echo "Available commands:"
	@echo "  make up           | Run all prod services in detached mode"
	@echo "  make up-at        | Run all prod services in attached mode"
	@echo "  make up-dev       | Run all services in dev mode"
	@echo "  make down         | Stop all services"
	@echo "  make down-tot     | Stop all services with sudo"

up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

up-at:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build

up-dev:
	docker compose up --build

down-tot:
	sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml down

down:
	docker compose down
