venv:
	virtualenv venv
	venv/bin/pip install -r test-requirements.txt

test:
	venv/bin/py.test tests/ -vsx

release:
	@git checkout v$(VERSION)
	@-rm dist/*
	venv/bin/python setup.py sdist bdist_wheel
	@read -n 1 -r -p "Release $(VERSION) to PyPI? " REPLY; \
	if [ "$$REPLY" == "y" ]; then\
		twine upload dist/*.tar.gz;\
		twine upload dist/*.whl;\
	else\
		echo "Not uploading..";\
	fi
	git checkout $(GIT_BRANCH)

version:
	echo "__version__ = '$(VERSION)'" > needinit/_version.py
	git commit --allow-empty -a -m "Bumping version to $(VERSION)"
	git tag -a v$(VERSION)
