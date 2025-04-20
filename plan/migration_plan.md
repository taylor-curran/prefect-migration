# Airflow to Prefect 3 Migration Plan

## 1. Repository Analysis

- **Current Setup**: Apache Airflow 2.10.5 with ~60 DAG files
- **DAG Complexity**: Ranges from simple (hello_world.py) to complex (glam.py) with GCP integrations

## 2. Migration Approach

### Phase 1: Basic Syntax Migration

1. **Start with simple DAGs**
   - hello_world.py 
   - casa.py 
   - Other simple DAGs with minimal operators

2. **Core Conversion Patterns**:

   | Airflow Concept | Prefect Equivalent |
   |----------------|--------------------|  
   | DAG object + with DAG() | @flow-decorated function |
   | PythonOperator | @task-decorated function |
   | BashOperator | @task with subprocess or shell command utils |
   | Custom operators | @task with appropriate implementation |
   | XCom push/pull | Direct function returns and parameters |
   | DAG dependencies (>>) | Function calls (result = task_a(); task_b(result)) |
   | Variables & connections | Environment variables or Prefect blocks |

3. **Learned Conversion Tips**:
   - Keep each flow file standalone and runnable
   - Use `log_prints=True` for simple debugging in the flow decorator
   - Document the original DAG's purpose and ownership in the flow docstring
   - Create placeholder implementations for external integrations
   - Flows can be tested by simply calling them as Python functions

4. **Example Conversion** (hello_world.py):

python
# Original Airflow DAG
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def print_hello():
    return "Hello from Airflow!"

with DAG(
    dag_id="hello_world",
    # other parameters...
) as dag:
    python_task = PythonOperator(
        task_id="python_hello",
        python_callable=print_hello,
    )
    bash_task = BashOperator(
        task_id="bash_hello",
        bash_command="echo 'Hello from Bash!'" 
    )
    python_task >> bash_task

python
# Converted Prefect flow
from prefect import flow, task
import subprocess

@task
def print_hello():
    return "Hello from Prefect!"

@task
def run_bash_command():
    subprocess.run(["echo", "Hello from Bash!"], check=True)

@flow(name="hello_world", log_prints=True)
def hello_world_flow():
    # Execute tasks in order
    hello_result = print_hello()
    print(hello_result) 
    run_bash_command()
    return hello_result

if __name__ == "__main__":
    hello_world_flow()

## 3. Testing Strategy

### Avoiding Airflow Testing Antipatterns

- **Don't port over structural validation tests** - they're less relevant in Prefect
- **Don't test that flows can be imported/parsed** - this is unnecessary in Prefect's model
- **Don't focus on testing flow metadata** - focus on behavior instead

### Prefect-Native Testing Approach

1. **Test actual flow execution and outputs**
   - Test that flows complete successfully and return expected results
   - Focus on business logic validation, not structure

2. **Test task functionality**
   - Use `.fn()` method to access the original function
   - Use `disable_run_logger` when testing tasks that use logging

3. **Use `prefect_test_harness` efficiently**
   - Set up as a session-scoped fixture rather than per-test
   - Avoids overhead of creating new test database for each test

python
# tests/prefect_flows/test_hello_world.py
import pytest
from prefect.testing.utilities import prefect_test_harness
from prefect.logging import disable_run_logger

from prefect_flows.hello_world import hello_world_flow, print_hello

# Create a session-scoped fixture for more efficient testing
@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield

def test_print_hello():
    # Test individual task using .fn() to access the original function
    # Use disable_run_logger if the task uses logging
    with disable_run_logger():
        assert print_hello.fn() == "Hello from Prefect!"

def test_hello_world_flow():
    # Test the entire flow
    result = hello_world_flow()
    assert result == "Hello from Prefect!"

## 4. Complex DAG Migration

- Break apart large DAGs if needed
- Convert Airflow subDAGs to Prefect subflows 
- Consider organizing shared utilities to avoid duplication

## 5. Deployment and Scheduling

- Create YAML-based deployment configurations
- Replace Airflow schedules with Prefect schedules in deployment configs
- Replace Airflow sensors with Prefect Deployment triggers (via prefect.yaml)
- Finalize directory structure based on deployment needs

prefect-migration/
├── prefect_flows/            # Converted flows
│   ├── __init__.py
│   ├── hello_world.py        # Each file contains both flow and its tasks
│   ├── casa.py
│   └── ...
├── utils/                    # Keep existing utilities where possible
└── deployment/               # For YAML deployment configurations
    ├── dev/
    └── prod/

## 6. Infrastructure Integration

- Configure work pools for production deployment
- Handle GCP integrations with appropriate Prefect patterns