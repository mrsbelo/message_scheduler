clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

run_flask_local:
	. venv/bin/activate && python3 src/manage.py run -h 0.0.0.0

