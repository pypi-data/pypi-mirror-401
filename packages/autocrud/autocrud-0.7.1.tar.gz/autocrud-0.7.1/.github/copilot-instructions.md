# AutoCRUD Agent Instructions

You are an AI developer working on the AutoCRUD project, a model-driven automated FastAPI framework with built-in versioning, permissions, and search.

## 🏗 Project Architecture

### Core Components

- **`AutoCRUD`** ([autocrud/crud/core.py](autocrud/crud/core.py)): Entry point that orchestrates model registration and route generation. Supports customization via `route_templates`, `storage_factory`, and `event_handlers`.
- **`ResourceManager`** ([autocrud/resource_manager/core.py](autocrud/resource_manager/core.py)): Core business logic layer managing CRUD operations, versioning, permissions, events, and data migration.
- **`IRouteTemplate`** ([autocrud/crud/route_templates/basic.py](autocrud/crud/route_templates/basic.py)): Defines API endpoint generation. Each template (Create, Read, Update, Delete, Search, etc.) generates specific routes.
- **Storage Abstraction**:
  - `IStorage` provides unified interface for metadata and resource data
  - `IStorageFactory` creates storage instances per model
  - Implementations: `MemoryStorageFactory`, `DiskStorageFactory` ([autocrud/resource_manager/storage_factory.py](autocrud/resource_manager/storage_factory.py))
  - Storage is split into `IMetaStore` (indexes/metadata), `IResourceStore` (payload), and `IBlobStore` (binary data)

### Key Architectural Patterns

- **Versioning**: Every modification creates a new revision with `revision_id`. Status can be `draft` (mutable via `modify`) or `stable` (immutable, new version required). Parent-child revision chains enable full history tracking.
- **Binary Data Optimization**: `Binary` struct ([autocrud/types.py](autocrud/types.py)) automatically extracts bytes to blob store using content hash as `file_id`, avoiding duplication.
- **Partial Operations**: Uses `msgspec` for efficient partial reads/writes. `get_partial` returns subset of fields; `patch` applies JSON Patch operations ([RFC 6902](https://tools.ietf.org/html/rfc6902)).
- **Event System**: Lifecycle hooks (Before/After/OnSuccess/OnFailure) for Create, Read, Update, Delete, Patch, Switch, etc. Registered via `IEventHandler` ([autocrud/types.py](autocrud/types.py#L1713)).

## 🛠 Development Workflow

### Package Manager: `uv`

**CRITICAL**: Always use `uv run` to execute scripts in the project environment.

```bash
uv sync              # Install dependencies
uv run pytest        # Run tests
uv run python script.py  # Execute scripts
```

### Build & Test Commands

```bash
make test            # Run tests (excluding benchmarks) + coverage report
make test-benchmark  # Run performance benchmarks
make coverage        # Generate coverage report (target: ≥90%)
make cov-html        # Generate HTML coverage report in htmlcov/
make style           # Auto-format with ruff format + ruff check --fix
make check           # Lint check (ruff check)
make dev             # Quick dev cycle: style + test
make ci              # CI/CD flow: check + test + coverage
```

### Testing Guidelines

- All new features **MUST** include tests
- Target: **90% code coverage** (currently ~86%)
- Use `msgspec.Struct` for test models
- Integration tests in [tests/test_autocrud.py](tests/test_autocrud.py)
- Event handler tests in [tests/test_event_handlers.py](tests/test_event_handlers.py)

## 📝 Coding Conventions

### Data Models: `msgspec.Struct` ONLY

**DO NOT use Pydantic `BaseModel`**. AutoCRUD is optimized for `msgspec`:

```python
from msgspec import Struct, UNSET, UnsetType

class User(Struct):
    name: str
    age: int
    email: str | None = None
    tags: list[str] = []
    
class OptionalFields(Struct, kw_only=True):
    field: str | UnsetType = UNSET  # Distinguish null vs missing
```

### Async/Await

All FastAPI routes and storage operations are async. Always `await`:

```python
async def create_resource(mgr: ResourceManager, data):
    with mgr.meta_provide(user="system", now=dt.datetime.now()):
        info = mgr.create(data)  # Synchronous context manager
    return info
```

### Type Hints

Extensive type annotations required. Use `typing_extensions.Literal`, `Generic[T]`, etc.

### Language

- **Code & Comments**: English
- **User Interaction**: Taiwan Traditional Chinese (台灣繁體中文) when specified in instructions

## 🔍 Implementation Patterns

### Adding New Route Templates

1. Inherit from `BaseRouteTemplate` ([autocrud/crud/route_templates/basic.py](autocrud/crud/route_templates/basic.py))
2. Implement `apply(model_name, resource_manager, router)` 
3. Set `order` property for route registration sequence
4. Example: [autocrud/crud/route_templates/create.py](autocrud/crud/route_templates/create.py)

```python
class CustomRouteTemplate(BaseRouteTemplate):
    def apply(self, model_name: str, resource_manager: IResourceManager[T], router: APIRouter):
        @router.get(f"/{model_name}/custom")
        async def custom_endpoint():
            # Implementation
            pass
```

### Event Handling

Implement `IEventHandler` with lifecycle methods:

```python
class AuditEventHandler(IEventHandler):
    def before_create(self, ctx: EventContext, data: dict):
        # Pre-create validation
        pass
    
    def after_create(self, ctx: EventContext, resource: Resource):
        # Post-create audit logging
        pass
```

Register with `ResourceManager` or `AutoCRUD`:

```python
crud = AutoCRUD(event_handlers=[AuditEventHandler()])
```

### Search & Indexing

- Define indexed fields: `crud.add_model(User, indexed_fields=[("wage", int | None)])`
- Search uses `ResourceMetaSearchQuery` for metadata and `DataSearchCondition` for indexed data fields
- Implementation: [autocrud/crud/route_templates/search.py](autocrud/crud/route_templates/search.py)

### Data Migration

Use `IMigration` to handle schema evolution:

```python
def migrate_v1_to_v2(data: dict) -> dict:
    data["new_field"] = "default"
    return data

crud.add_model(User, migration={"1": ("2", migrate_v1_to_v2)})
```

## 📂 Critical File Reference

- **Core Types**: [autocrud/types.py](autocrud/types.py) - All interfaces (`IResourceManager`, `IStorage`, `IEventHandler`, etc.)
- **AutoCRUD Entry**: [autocrud/crud/core.py](autocrud/crud/core.py) - Main API
- **ResourceManager**: [autocrud/resource_manager/core.py](autocrud/resource_manager/core.py) - Business logic
- **Route Templates**: [autocrud/crud/route_templates/](autocrud/crud/route_templates/) - Endpoint generators
- **Storage Factories**: [autocrud/resource_manager/storage_factory.py](autocrud/resource_manager/storage_factory.py)
- **Test Suite**: [tests/test_autocrud.py](tests/test_autocrud.py) - Integration tests
