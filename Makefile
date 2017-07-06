venv:
	virtualenv venv
	venv/bin/pip install -r test-requirements.txt

test:
	venv/bin/py.test tests/ -vsx
