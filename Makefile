start:
	docker-compose up

stop:
	docker-compose down

restart:
	docker-compose down && docker-compose up

startd:
	docker-compose up -d

restartd:
	docker-compose down && docker-compose up -d

logs:
	docker-compose logs -f

export:
	export $(cat .env | sed 's/#.*//g' | xargs)
