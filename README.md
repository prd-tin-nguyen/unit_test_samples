## Test single test file

```shell
PYTHONPATH=./src pytest -vv tests/unit_tests/test_main.py --html=report.html
```

## Test entire folder test

```shell
PYTHONPATH=./src pytest -vv tests/unit_tests/ --html=report.html
```

## Test specific class

```shell
PYTHONPATH=./src pytest -vv tests/unit_tests/test_main.py::TestUserProfile \
--html=report.html
```

## Test specific method

```shell
PYTHONPATH=./src pytest -vv tests/unit_tests/test_main.py::TestUserProfile::test__is_valid_email \
--html=report.html
```

## Show test coverage

> must install pytest-cov first

```shell
PYTHONPATH=./src python -m pytest -vv --cov ./tests/unit_tests
```
