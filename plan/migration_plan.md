# Airflow to Prefect 3 Migration Plan

## 1. Repository Analysis

- **Current Setup**: Apache Airflow 2.10.5 with ~60 DAG files
- **DAG Complexity**: Ranges from simple (hello_world.py) to complex (glam.py) with GCP integrations

## 2. Environment Setup

bash
# Using existing venv or creating one if needed
source .venv/bin/activate  # or your preferred venv location

# Install Prefect 3
pip install prefect>=3.0.0

## 3. Migration Approach

### Phase 1: Basic Syntax Migration

1. **Start with simple DAGs**
   - hello_world.py
   - extensions.py
   - other simple DAGs with minimal operators

2. **Core Conversion Patterns**:

   | Airflow Concept | Prefect Equivalent |
   |----------------|--------------------|
   | DAG object + with DAG() | @flow-decorated function |
   | PythonOperator | @task-decorated function |
   | BashOperator | @task with subprocess or shell command utils |
   | XCom push/pull | Direct function returns and parameters |
   | DAG dependencies (>>) | Function calls (result = task_a(); task_b(result)) |

3. **Example Conversion** (hello_world.py):

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

### Phase 2: Medium Complexity DAGs

- Handle scheduling, retries, notifications, and other metadata
- Focus on direct translation of business logic
- Keep tasks in the same file as flows unless there's a clear need for reuse

### Phase 3: Complex DAGs

- Break apart large DAGs if needed
- Convert Airflow subDAGs to Prefect subflows
- Handle GCP integrations

## 4. Testing Strategy

1. **Leverage Existing Tests**
   - Convert existing Airflow tests in the `/tests` directory to work with Prefect flows
   - Maintain test coverage for critical business logic

2. **Simple Test Approach**
   - After converting the first 3 simple flows, create basic test patterns
   - Use these test patterns as templates for validating other migrations

3. **Test Framework**
   - Use pytest (already in the repository) for testing Prefect flows
   - Example test for hello_world flow:

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

## 5. Directory Structure

Simple approach to start with:

prefect-migration/
├── prefect_flows/            # Converted flows
│   ├── __init__.py
│   ├── hello_world.py        # Each file contains both flow and its tasks
│   ├── extensions.py
│   └── ...
├── utils/                    # Keep existing utilities where possible
└── deployment/               # For later YAML deployment configurations

## 6. Next Steps (Post-Syntax Migration)

- Create YAML-based deployment configurations
- Set up GCP authentication blocks
- Configure work pools for production deployment