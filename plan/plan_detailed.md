# Detailed Migration Plan

## DAG Migration Priority & Roadmap

The following DAGs have been identified as the simplest ones to migrate first, based on file size and complexity:

| # | DAG File | Size (bytes) | Status | Notes |
|---|----------|--------------|--------|-------|
| 1 | hello_world.py | 957 | ✅ COMPLETED | Basic Python/Bash operators |
| 2 | casa.py | 1058 | ✅ COMPLETED | FivetranOperator example |
| 3 | extensions.py | 1221 | 🔄 NEXT | Uses GKEPodOperator |
| 4 | play_store_export.py | 1412 | 📋 PLANNED | |
| 5 | publish_bqetl_static.py | 1427 | 📋 PLANNED | |
| 6 | contextual_services_import.py | 1469 | 📋 PLANNED | |
| 7 | clean_gke_pods.py | 1608 | 📋 PLANNED | |
| 8 | partybal.py | 1647 | 📋 PLANNED | |
| 9 | broken_site_report_ml.py | 1711 | 📋 PLANNED | |
| 10 | webcompat_kb.py | 1858 | 📋 PLANNED | |

After completing these initial DAGs, we'll move on to these medium-complexity DAGs:
- dbt_daily.py
- experiments_live.py
- search_alert.py
- operational_monitoring.py
- search_forecasting.py

## Testing Strategy & Implementation

### Determine Appropriate Test Coverage Plan

**Objective**: Establish the right level of test coverage for non-trivial flows before scaling testing approach.

**Actions**:
1. Select two converted flows that are not hello_world (casa.py and one more) for thorough testing
2. For each selected flow:
   - Identify all testable components (tasks, business logic, edge cases)
   - Determine which components are critical vs. nice-to-have for testing
   - Document expected inputs/outputs for each component

**Success Criteria**:
- Test coverage document outlining what aspects of flows should be tested
- Agreement on testing priorities based on business value

### Create Test Fixture Framework

**Objective**: Build reusable testing infrastructure that follows Prefect best practices.

**Actions**:
1. Create `tests/prefect_flows` directory structure
2. Implement a common `conftest.py` with the session-scoped `prefect_test_harness` fixture
3. Create mock utilities for external dependencies (API clients, database connections)

**Success Criteria**:
- Testing infrastructure that can be easily extended to all future flows
- Clear pattern for mocking external dependencies

### Implement Tests for Core Flows

**Objective**: Create comprehensive test suites for the two selected flows.

**Actions**:
1. Write unit tests for individual tasks using `.fn()` method
2. Write integration tests for the complete flow execution
3. Test error handling and edge cases
4. Document testing patterns with examples

**Success Criteria**:
- Passing test suite for two complex flows
- Template for testing other flows
- Documentation of learned testing patterns
