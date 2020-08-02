clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

run_flask_local:
	. venv/bin/activate && python3 src/manage.py run -h 0.0.0.0

docker_build:
	docker-compose up -d --build

docker_run:
	docker-compose up

run_tests:
	. venv/bin/activate && cd src/ && pytest -s