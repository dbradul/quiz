#!make
include .env


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

top:
	docker-compose top

collect:
	docker-compose exec backend python src/manage.py collectstatic --settings=app.settings.prod

shellc:
	docker-compose exec backend python src/manage.py shell_plus --print-sql

shell:
	python src/manage.py shell_plus --print-sql --settings=app.settings.dev

dump:
	python src/manage.py dumpdata --settings=app.settings.dev --exclude auth.permission --exclude contenttypes > src/quiz/tests/fixtures/dump.json

test:
	cd src && python manage.py test --settings=app.settings.dev

coverage:
	cd src && coverage run --rcfile=../.coveragerc --source=. manage.py test --settings=app.settings.dev && coverage html -d ../coverage_html

expr:
	export $(cat .env | sed 's/#.*//g' | xargs)
