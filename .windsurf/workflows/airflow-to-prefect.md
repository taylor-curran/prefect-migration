---
description: Migrate a single Airflow DAG to Prefect 3 using TDD
---

# Airflow → Prefect (TDD) Workflow  
Slash-command: `/airflow-to-prefect`

> This workflow guides Cascade (and you) through converting **one** Airflow DAG into a Prefect flow using test-driven development, manual safety checks, and automatic doc updates.

## Steps

1. **Review Implicated Files**  
   - Cascade inspects the chosen DAG and any helper modules to understand its structure, operators, external integrations, and environment variables.  
   - additionally cascade reviews and relevant prefect files
   - Summarize findings (operators used, external integrations, env vars, etc.).

2. **Ask Clarifying Questions**  
   - Ask the user about expected behaviour, edge cases, external services, config, etc.  
   - Specifically flag GCP/DataHub integrations or anything complex.  
   - Wait for answers **before continuing**.

3. **Draft Migration Plan**  
   - Create `plan/migration_<dag_name>.md` containing:  
     - Objectives, Actions, Success Criteria (follow planning conventions).  
     - Mapping table of Airflow components → Prefect equivalents.  
     - Test strategy (tasks to test, flow outputs).  
   - Use `write_to_file`, then **pause** for user approval.

4. **Write Red Tests**  
   - Create `tests/prefect_flows/test_<dag_name>.py` with 1–2 failing tests that express desired behaviour.  
   - Ensure tests import a yet-to-be-written module `prefect_flows.<dag_name>`.  
   - Use Prefect testing best practices (`prefect_test_harness`, `.fn()`, etc.).  
   - Wait for user approval.

5. **Run Tests (Expect Failure)**  
   - Command: `pytest tests/prefect_flows/test_<dag_name>.py`  
   - Share output with user; confirm that failures are as expected.

6. **Implement Prefect Flow**  
   - Create `prefect_flows/<dag_name>.py` converting the DAG according to the approved plan.  
   - Keep flow & tasks in the same file.  
   - Preserve original DAG purpose in docstring.

7. **Run Tests Until Green**  
   - Re-run `pytest` (entire suite).  
   - Iterate with user until all tests pass.

8. **Update Documentation**  
   - Edit `plan/plan_detailed.md` (and any roadmap tables) to mark the DAG ✅ **COMPLETED**.  
   - Add notes/links to the new Prefect flow and tests.

9. **Optional Cleanup & Commit**  
   - Prompt user if they’d like to create a Git commit or PR.  
   - Provide summary of changes.

---
### Notes
- **Manual steps only**: No `// turbo` directives are included; each command requires explicit user approval.  
- **Testing first**: Implementation cannot begin until the red tests are written and acknowledged.  
- **Complex DAGs**: Use Step 2 to surface special considerations (GCP creds, environment variables, secrets).  
- **Directory conventions**: Converted flows live in `prefect_flows/`; tests in `tests/prefect_flows/`.