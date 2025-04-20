# Airflow to Prefect Migration Scope

This document outlines the scope and key parameters for the migration from Apache Airflow to Prefect based on initial discovery discussions.

## Target Version

- **Prefect 3.0** (latest version)
- Will require researching up-to-date features and best practices for this version
- Approximately 60+ DAG files to migrate
- Migration Goal: Enable data engineers to build workflows faster with a more pythonic framework

## Out of Scope

- Maintenance of original Airflow DAGs after migration
- Complete re-architecture of workflows (focus on direct conversion while improving where possible)
- Changes to underlying business logic or data processing

## Success Criteria

- All workflows successfully converted to Prefect flows
- Local execution validated for all flows
- Production deployment patterns established
- Documentation created for future flow development

## Migration Strategy Highlights

- No need to maintain both systems in parallel during migration
- Convert Airflow DAGs back to native Python functions with `@flow` decorators
- Many Airflow operators can be replaced with Prefect blocks, available through Prefect integration libraries
- Focus on testing and validating each flow before moving to deployment configuration
- Start with converting simple workflows before tackling complex orchestration
- Airflow has a lot of anti-patterns that we can avoid in Prefect
  - Don't fall in the trap of repeating them in the Prefect implementation just because they exist in Airflow


# Extra Scoping Considerations


## Testing Strategy

- Leverage existing Airflow tests to validate Prefect flow functionality
- Create test patterns for the first few simple flows as conversion templates
- Use pytest with `prefect_test_harness` as a session-scoped fixture for efficient testing
- Test tasks individually using the `.fn()` method to access the original function
- Use `disable_run_logger` when testing tasks that use logging
- Tests will serve as a validation mechanism throughout the migration process

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



