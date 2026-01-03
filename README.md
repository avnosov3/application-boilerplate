## Application Architecture

```
├── alembic.ini
├── database.db
├── docker-compose.yaml
├── Dockerfile
├── Makefile
├── pyproject.toml (using uv, mypy, pytest, pytest-mock, ruff)
├── README.md
├── src
│   ├── api
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── v1
│   │       ├── exception_handlers.py
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── routes
│   │           ├── excel_processing.py
│   │           ├── __init__.py
│   │           └── reports.py
│   │       └── schemas
│   │           ├── __init__.py
│   │           └── reports.py
│   ├── bootstrap (application startup and wiring layer)
│   │   ├── app_factory.py (builds and configures the FastAPI  or others applications)
│   │   ├── container.py (the dependency injection container)
│   │   ├── __init__.py
│   │   └── logging.py (configures application logging)
│   ├── core
│   │   ├── base
│   │   │   ├── custom_enums.py
│   │   │   ├── custom_types.py
│   │   │   ├── exceptions.py
│   │   │   └── __init__.py
│   │   ├── config.py
│   │   ├── __init__.py
│   │   ├── interfaces (defines application interfaces between layers, including repositories, providers, and supporting tools)
│   │   │   ├── __init__.py
│   │   │   ├── providers
│   │   │   │   ├── cloud_storage_provider
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── provider.py
│   │   │   │   └── __init__.py
│   │   │   ├── repositories
│   │   │   │   ├── __init__.py
│   │   │   │   ├── raw_excel_repository
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── repository.py
│   │   │   │   ├── report_repository
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── repository.py
│   │   │   │   └── unit_of_work.py
│   │   │   └── tools
│   │   │       ├── excel_bytes_parser
│   │   │       │   ├── __init__.py
│   │   │       │   └── tool.py
│   │   │       ├── __init__.py
│   │   │       └── report_generator
│   │   │           ├── __init__.py
│   │   │           └── tool.py
│   │   ├── models
│   │   │   ├── base
│   │   │   │   ├── from_attributes.py
│   │   │   │   └── __init__.py
│   │   │   ├── excel_models.py
│   │   │   ├── __init__.py
│   │   │   └── reports.py
│   │   └── utils.py
│   ├── main.py
│   ├── providers (implementations of providers interfaces)
│   │   ├── azure_provider
│   │   │   ├── __init__.py
│   │   │   └── provider.py
│   │   └── __init__.py (exports provider implementations for use in other layers)
│   ├── repositories (implementations of repositories interfaces)
│   │   ├── __init__.py (exports repository implementations for use in other layers)
│   │   └── sqlalchemy_repositories
│   │       ├── __init__.py
│   │       ├── migrations
│   │       │   ├── env.py
│   │       │   ├── __init__.py
│   │       │   ├── README
│   │       │   ├── script.py.mako
│   │       │   └── versions
│   │       │       ├── 0001-2025_12_30_1839-created_raw_excel_table.py
│   │       │       └── 0002-2025_12_30_1843-created_report_table.py
│   │       ├── orm_models.py
│   │       ├── raw_excel_repository
│   │       │   ├── __init__.py
│   │       │   └── repository.py
│   │       ├── report_repository
│   │       │   ├── __init__.py
│   │       │   └── repository.py
│   │       └── unit_of_work.py
│   ├── services (orchestrating repositories, providers, and tools)
│   │   ├── excel_processing_service
│   │   │   ├── __init__.py
│   │   │   └── service.py
│   │   ├── __init__.py (exports services for use in other layers)
│   │   └── report_service
│   │       ├── __init__.py
│   │       └── service.py
│   ├── templates
│   │   └── __init__.py
│   └── tools  (implementations of tools interfaces)
│       ├── custom_report_generator
│       │   ├── __init__.py
│       │   └── tool.py
│       ├── __init__.py (exports tool implementations for use in other layers)
│       └── pandas_tool
│           ├── __init__.py
│           └── tool.py
├── tests
│   ├── conftest.py
│   ├── e2e
│   │   └── __init__.py
│   ├── fixtures
│   │   ├── app.py
│   │   ├── __init__.py
│   │   ├── providers.py
│   │   ├── repositories.py
│   │   ├── services.py
│   │   └── tools.py
│   ├── __init__.py
│   ├── integration
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   └── v1
│   │   │       ├── __init__.py
│   │   │       └── test_reports.py
│   │   ├── __init__.py
│   │   └── test_fastapi_app.py
│   └── unit
│       ├── __init__.py
│       └── providers
│           ├── azure_provider
│           │   ├── __init__.py
│           │   └── test_provider.py
│           └── __init__.py
└── uv.lock
```

## Layer Responsibilities

- providers: integrations with external APIs and services (not database access).
- repositories: data access layer for persistence (PostgreSQL, Elasticsearch, Redis, etc.).
- tools: helper components (parsers, generators, adapters).
- services: application orchestration that coordinates repositories, providers, and tools.

## Interfaces First

Each layer starts with an abstract interface in `core/interfaces`, and concrete implementations live in the corresponding layer directory (`providers`, `repositories`, `services`, `tools`).

## Implementation Exports

Implementations are re-exported via `__init__.py` in their package directories (e.g. `providers`, `repositories`, `services`, `tools`). This keeps import paths stable and allows the rest of the codebase to depend on the package-level API rather than concrete module paths.
 
## API Schemas

API schemas are defined under `api/v1/schemas` and represent request/response models for transport-level boundaries.
Domain models stay in `core/models` and are mapped to API schemas in routes (or dedicated mappers) to keep the domain layer transport-agnostic.
