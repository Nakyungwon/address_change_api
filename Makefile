all:
	docker-compose up --build

run:
	docker-compose up

build:
	docker-compose build

bash:
	docker container exec -it address_change_api bash

web_bash:
	docker container exec -it web_server bash

db_bash:
	docker container exec -it mysql_service bash