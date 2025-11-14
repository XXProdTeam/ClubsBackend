help:
	@echo "Available commands:"
	@echo "  make up           | Run all prod services"
	@echo "  make down         | Stop all services"

up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

up-at:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build

down-tot:
	sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml down

down:
	docker compose down
