test:
	python3 runtests.py

testc:
	coverage run --source=clickthroughs runtests.py
	coverage report -m --skip-covered

# lint:
# 	@pylint --ignore migrations clickthroughs

clean:
	rm -rf dist
	rm -rf django_clickthroughs.egg-info

build: clean
	python -m build

publish: build
	twine upload dist/*
