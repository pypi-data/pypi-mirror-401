# 33. Python test

## Task 1
See what exit code do the test provide.

## Task 2
Mock some tests

## Task 3
Create python standalone executable with pyinstaller

## Task 4
Create a pipeline, do tests, package and push python package to pypi




## Commands used 
```bash
python3 setup.py sdist

python3 -m venv env_setuptools

. ./env_setuptools/bin/activate

pip install dist/mocking-0.1.tar.gz
```


## Commands used for upload
```bash
python3 setup.py sdist

python3 -m venv env_setuptools

. ./env_setuptools/bin/activate

pip install dist/mocking-0.1.tar.gz

python3 -m twine upload dist/*
```


## Upload to pypi tip
```bash
python3 -m twine upload dist/* --verbose
```

Use unique project name in setup.py. You can use your github username as a prefix.