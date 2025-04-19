# Airflow to Prefect Migration Scope

This document outlines the scope and key parameters for the migration from Apache Airflow to Prefect based on initial discovery discussions.

## Target Version

- **Prefect 3.0** (latest version)
- Will require researching up-to-date features and best practices for this version

## Migration Strategy Highlights

- No need to maintain both systems in parallel during migration
- Convert Airflow DAGs back to native Python functions with `@flow` decorators
- Focus on testing and validating each flow before moving to deployment configuration
- Start with converting simple workflows before tackling complex orchestration

## Out of Scope

- Maintenance of original Airflow DAGs after migration
- Complete re-architecture of workflows (focus on direct conversion while improving where possible)
- Changes to underlying business logic or data processing

## Infrastructure & Deployment

- **Development Environment**: 
  - Local execution with `pip install prefect`
  - Zero infrastructure requirements for development and testing

- **Production Environment**:
  - GCP-based deployment
  - Options under consideration:
    - Kubernetes Jobs
    - Cloud Run Jobs (decision pending)

- **Deployment Configuration**:
  - YAML-based approach for defining deployments
  - Using `prefect.yaml` files rather than `python.deploy()` syntax
  - Focus on successful local runs before configuring deployments

## Existing Codebase Analysis

- **DAG Complexity**: Mixed
  - Simple DAGs (e.g., `hello_world.py`) with basic Python/Bash operations
  - Complex DAGs (e.g., `glam.py`) with extensive dependencies, custom operators, and complex orchestration
  - Approximately 60+ DAG files to migrate

- **Technology Integrations**:
  - GCP services integration
  - Docker containers
  - DataHub integration
  - SQL execution
  - Custom operators and utilities

## Success Criteria

- All workflows successfully converted to Prefect flows
- Local execution validated for all flows
- Production deployment patterns established
- Documentation created for future flow development

## Testing Strategy

- Leverage existing Airflow tests to validate Prefect flow functionality
- Create test patterns for the first few simple flows as conversion templates
- Use pytest with `prefect_test_harness` as a session-scoped fixture for efficient testing
- Test tasks individually using the `.fn()` method to access the original function
- Use `disable_run_logger` when testing tasks that use logging
- Tests will serve as a validation mechanism throughout the migration process

## Migration Goals

- Enable data engineers to build workflows faster with a more pythonic framework
- Reduce complexity compared to Airflow's DAG-centric approach
- Leverage Prefect's minimal invasiveness to Python code
- Improve development velocity through simpler local testing