# Project Context for AI Agents

## Project Overview

**Name**: django-saas-base
**Description**: The foundation for building a SaaS product with Django.

## Tech Stack

- **Language**: Python 3.12+
- **Framework**: Django (5.0+)
- **API**: Django Rest Framework (DRF)
- **Build System**: Hatchling
- **Testing**: pytest, pytest-django
- **Linting/Formatting**: Ruff

## Project Structure

### Root Directory

- `pyproject.toml`: Project configuration and dependencies.
- `manage.py`: Django management script.
- `src/`: Source code directory.
- `tests/`: Test suite.
- `demo/`: Demo application for local development/testing.

### Core Module (`src/saas_base`)

This is the main library package.

- **Models** (`src/saas_base/models/`):
  - `tenant.py`: Tenant model.
  - `group.py`: Group model.
  - `member.py`: Member model.
  - `role.py`: Role model.
  - `permission.py`: Permission model.
  - `user_email.py`: User email management.
- **DRF Enhancement**: (`src/saas_base/drf/`):
  - `filters.py`: Custom filters for DRF.
  - `permissions.py`: Tenant based permissions for DRF.
  - `serializers.py`: Enhanced serializers for DRF.
- **API** (`src/saas_base/endpoints/`, `src/saas_base/serializers/`):
  - DRF integration, serializers, and API endpoints.
- **Authentication & Authorization**:
  - `src/saas_base/auth/`: Authentication logic.
  - `src/saas_base/permissions.py`: DRF permissions.
  - `src/saas_base/rules/`: Security rules for authentication.
- **Configuration**:
  - `src/saas_base/settings.py`: Default settings.
  - `src/saas_base/apps.py`: App configuration.

### Testing (`tests/`)

- Uses `pytest`.
- Configuration in `pyproject.toml` under `[tool.pytest.ini_options]`.
- `tests/apis`: API tests.
- `tests/models`: Model tests.

## Development Guidelines

- **Code Style**: Follows `ruff` configuration (single quotes, line length 120).
- **Testing**: Run tests using `pytest`.
- **Dev Server**: `python manage.py runserver` to start a local development server.

## Key Concepts

- **SaaS Foundation**: Provides multi-tenancy primitives (Tenants, Members, Groups).
- **RBAC**: Role-Based Access Control via Roles, Groups and Permissions.
