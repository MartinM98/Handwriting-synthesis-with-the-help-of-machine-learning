coverage run "tests/run_all_tests.py"
coverage report
coverage html --rcfile="scripts/tests/.coveragerc"