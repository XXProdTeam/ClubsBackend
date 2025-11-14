help:
	@echo "Available commands:"
	@echo "  make up           | Run all prod services"
	@echo "  make down         | Stop all services"

up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

down:
	docker compose down