# Running pyfldm tests

## Functional Tests with only computer, no radio hooked up
1. Set up a python virtual environment
```
# start at the top level of pyfldm
cd pyfldm/
pip3 install virtualenv
python -m venv venv
```
2. Activate the virtual environment
```
source venv/bin/activate
```
3. Install the python test dependencies, including local pyfldm
```
pip install .   # this installs pyfldm in the venv
pip install -r requirements.txt
```
4. Select which tests to run
  - Move into tests folder (cd tests/)
  - Open run_functional_tests.py
  - Select either all the tests, a single test module, or a single test function to run as follows:
```
from functional_tests.testing_runner import TestingRunner
from functional_tests import TestAppMonitor, TestClient, ...

test_app_monitor = TestAppMonitor()
test_client = TestClient()
...

tests_to_run = [
    test_app_monitor,
    test_client,
    ...
]

# Select 0 for logging to console only, 1 for logging to a file only
# and 2 for logging to both
tester = TestingRunner(0)


# to run all the tests use the array of all test modules:
tester.run(tests_to_run)
# to run a test module:
tester.run(test_app_monitor)
# to run a single test function:
tester.run(test_app_monitor.test_app_launches)
```
5. Execute the tests
```
python3 run_functional_tests.py
```