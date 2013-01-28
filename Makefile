.PHONY: tests help hooks coverage full-coverage dev latex-doc doc static-analysis abgabe

help:
	@echo "Please use \`make <target>', targets:"
	@echo "    - tests: run unittests"
	@echo "    - coverage: gather coverage and produce html about relevant parts"
	@echo "    - full-coverage: gather coverage and produce html output"
	@echo "    - coverage-upload: gather coverage and upload it to 0x0b.de"
	@echo "    - dev: pip install all developmet dependencies"
	@echo "    - doc: generate html documentation"
	@echo "    - clean: removes all *.pyc *.pyo and logfiles"

tests:
	cd algolab && nosetests algolab
coverage: .coverage
	coverage report -i --omit='algolab/tests/*' --include='algolab/*' --omit='algolab/tests'
	coverage html
	coverage erase

full-coverage: .coverage
	coverage html --omit='algolab/tests/*' --include='algolab/*'
	coverage erase

.DELETE_ON_ERROR:
.coverage:
	coverage run -m unittest2 discover -p '*.py' -s algolab/tests -t .

doc:
	PYTHONPATH=${PYTHONPATH}:`pwd` make -C docs html

doc-upload:
	rsync -avz doc/_build/html/* 0x0b.de:/var/www/algolab.0x0b.de/htdocs

latex-doc:
	PYTHONPATH=${PYTHONPATH}:`pwd` make -C docs latex
	make -C docs/_build/latex

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -regex '.*.log\(.[0-9]+\)?' -delete
