coverage run -m --rcfile="scripts/tests/.coveragerc" --source="src" pytest "tests/run_all_tests.py"
coverage report --rcfile="scripts/tests/.coveragerc"
coverage html --rcfile="scripts/tests/.coveragerc"
coverage erase