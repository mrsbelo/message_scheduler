clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

create_venv:
	python3.8 -m venv venv

requirements_dev:
	. venv/bin/activate && pip install -r src/app/requirements/dev.txt

requirements_prod:
	. venv/bin/activate && pip install -r src/app/requirements/prod.txt

run_flask_local:
	. venv/bin/activate && python3 src/manage.py run -h 0.0.0.0

docker_build:
	docker-compose up -d --build

docker_run:
	docker-compose up

run_tests:
	. venv/bin/activate && cd src/ && pytest -s