from datetime import datetime
import subprocess

from prefect import flow, task


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
