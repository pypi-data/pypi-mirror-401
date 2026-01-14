# Neva

> A  web framework built on top of FastAPI.
>
## Why Neva?

Neva aims for two things:

- Improved developer experience and productivity for web developers.
- Lavarel-like API and methodologies to keep up with the companies technical directions driven by the Laravel community.

Neva accomplishes this by building on top of FastAPI and meshing it with a few chosen libraries. As such, it is very much an opinionated framework.

Currently, Neva provides:
✅ **Service Provider Pattern** - Laravel-style providers that automatically register and bootstrap services
✅ **Static Facades** - Convenient static access to services without DI ceremony (when appropriate)
✅ **Structured Configuration** - File-based config with dot notation, validation, and freezing
✅ **Result Types** - Rust-like `Result[T, E]` and `Option[T]` for explicit error handling
✅ **Built-in Observability** - Structured logging, correlation IDs, and profiling middleware out of the box

A fair warning: Some of these features are still a little barebone! Don't hesitate to open an issue if you have any suggestions.

## Installation

```bash
pip install python-neva
# or with uv
uv add python-neva
```

## Quick Start

### 1. Create Configuration Files

Neva uses file-based configuration instead of scattered environment variables. Create a `config/` directory:

```python
# config/app.py
import os

config = {
    "title": os.getenv("APP_NAME", "My Application"),
    "debug": bool(os.getenv("APP_DEBUG", 0)),
    "url": os.getenv("APP_URL", "http://localhost:8000"),
}
```

```python
# config/providers.py
import os

config = {
    "providers":[
        # Your custom providers
        EventServiceProvider,
        SearchEngineProvider,
    ],
}
```

### 2. Create Your Application

```python
from neva.arch import App
from neva.support.facade import Config, Log

app = App()

@app.get("/")
async def root():
    Log.info("Request received")
    return {
        "app": Config.get("app.title").unwrap(),
        "debug": Config.get("app.debug").unwrap(),
    }
```

### 3. Run Your Application

```bash
fastapi dev main.py
# or
uvicorn main:app --reload
```

## Core Architecture

### IoC Container

Neva embarks the Dishka library to provide expanded dependency injection capabilities. With FastAPI, you are limited to doing injection directly in your route. Here, you have a few more options that we'll explore.

#### Binding things

As a general rule you would only bind things within the `register` method of service providers.

Within a service provider, you always have access to the application instance via `self.app`. You may then use the `bind` method to bind things into the container:

```python
self.app.bind(CacheManager)
```

This will bind the `CacheManager` class into the container. If your class has no dependencies whatsoever, this is enough, however if your class has dependencies in its constructor, you also need to register them (this is very different from the zero-configuration from Laravel).

You may also provide another type to the `interface` parameter of the `bind` method.
This will instruct the container to bind the class to the interface instead of the concrete class, so whenever it needs to resolve this interface, it will return the bound concrete class.

#### Resolving things

To resolve a class from the container, you have a few options. Generally, you will use the `make` method from the `App` facade.

```python
manager = App.make(CacheManager)
```

This will return a `Result` object to help you deal with any potential errors. As explained above, you may request an interface in that way and the container will resolve the bound concrete class.

```python
self.app.bind(ConcreteCacheManager, interface=CacheManager)
...
App.make(CacheManager) # returns a ConcreteCacheManager instance
```

Because `App` is a facade on the application instance, you can also use the `make` method directly wherever you have access to said application instance, such as a service provider. You must be extremely careful with this tho, as this may lead to calling upon the container before it has been fully initialized and all dependencies registered.

Lastly, you may also use dependencies within routes like so:

```python
@router.get("/data")
@inject
async def get_data(cache: FromDishka[CacheManager]):
  ...
```

### Service Providers

Service providers are where most of the bootstrapping happens for your application. Many of the core components of Neva are initialized through service providers. This

```python
from neva.arch import ServiceProvider
from neva import Ok, Result
from typing import Self, override

class CacheServiceProvider(ServiceProvider):
    @override
    def register(self) -> Result[Self, str]:
        self.app.bind(CacheManager)
        return Ok(self)
```

**With Lifecycle Management:**

```python
from contextlib import asynccontextmanager

class DatabaseServiceProvider(ServiceProvider):
    def register(self) -> Result[Self, str]:
        self.app.bind(DatabaseManager)
        return Ok(self)

    @asynccontextmanager
    async def lifespan(self):
        # Startup logic
        db = self.app.make(DatabaseManager).unwrap()
        await db.connect()

        yield

        # Shutdown logic
        await db.disconnect()
```

**Auto-Register Providers:**

Add providers to your config to auto-load them:

```python
# config/providers.py
from myapp.providers import CacheServiceProvider, QueueServiceProvider

config = {
    "providers": [
        CacheServiceProvider,
        QueueServiceProvider,
    ]
}
```

### Facades: Static Access Without DI Overhead

Facades provide convenient static access to services from the DI container. Perfect for cross-cutting concerns like logging, configuration, and caching.

**Creating a Facade:**

```python
from neva.arch import Facade

class Cache(Facade):
    @classmethod
    def get_facade_accessor(cls) -> type:
        return CacheManager
```

**Using a Facade:**

```python
from myapp.facades import Cache

# No need for Depends() or dependency injection
@app.get("/data")
async def get_data():
    cached = Cache.get("key")
    if cached:
        return cached

    data = fetch_expensive_data()
    Cache.set("key", data)
    return data
```

**Built-in Facades:**

- `Config` - Access configuration: `Config.get("app.debug")`
- `Log` - Structured logging: `Log.info("message", user_id=123)`
- `App` - Access the application instance

**When to Use Facades vs. DI:**

- ✅ **Use Facades for**: Logging, configuration, caching, events - things you access everywhere
- ✅ **Use DI for**: Repositories, services, domain logic - things specific to a route/handler

### Configuration Management

**Dot Notation Access:**

```python
from neva.support.facade import Config

# Get nested config values with dot notation
db_host = Config.get("database.connections.default.credentials.host").unwrap()
app_name = Config.get("app.title").unwrap_or("Default App Name")

# Check if config exists
if Config.has("features.new_ui"):
    enable_new_ui()
```

**Type-Safe Configuration:**

Since configs are Python files, you get full IDE support and can use TypedDicts:

```python
# config/cache.py
from typing import TypedDict

class RedisConfig(TypedDict):
    host: str
    port: int
    db: int

config: dict[str, RedisConfig] = {
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }
}
```

### Result Types: Explicit Error Handling

Replace exceptions and `Optional` returns with explicit `Result[T, E]` types:

**Before:**

```python
def get_user(id: int) -> User | None:
    user = find_user(id)
    if not user:
        return None
    return user

# Usage - easy to forget None check
user = get_user(123)
print(user.name)  # Potential AttributeError!
```

**After:**

```python
from neva import Ok, Err, Result

def get_user(id: int) -> Result[User, str]:
    user = find_user(id)
    if not user:
        return Err(f"User {id} not found")
    return Ok(user)

# Usage - forced to handle error
match get_user(123):
    case Ok(user):
        print(user.name)
    case Err(error):
        print(f"Error: {error}")

# Or use helper methods
user = get_user(123).unwrap()  # Raises if Err
user = get_user(123).unwrap_or(default_user)
user = get_user(123).unwrap_or_else(lambda: create_guest_user())
```

**Chaining Operations:**

```python
result = (
    get_user(123)
    .and_then(lambda u: get_user_permissions(u))
    .and_then(lambda p: validate_permissions(p))
    .map(lambda p: format_permissions(p))
)

if result.is_ok:
    return result.unwrap()
else:
    raise HTTPException(status_code=404, detail=result.unwrap_err())
```

### Event System

Decouple your application logic with an event-driven architecture:

**Define Events:**

```python
from neva.events import Event

class UserCreated(Event):
    user_id: int
    email: str
    name: str
```

**Define Listeners:**

```python
from neva import Result, Ok

class SendWelcomeEmailListener:
    async def handle(self, event: UserCreated) -> Result[None, str]:
        await email_service.send_welcome(
            to=event.email,
            name=event.name
        )
        return Ok(None)

class CreateUserProfileListener:
    async def handle(self, event: UserCreated) -> Result[None, str]:
        await profile_service.create(user_id=event.user_id)
        return Ok(None)
```

**Register Listeners:**

```python
from neva.arch import ServiceProvider
from neva.events import Event

class EventServiceProvider(ServiceProvider):
    @asynccontextmanager
    async def lifespan(self):
        Event.listen(UserCreated, SendWelcomeEmailListener)
        Event.listen(UserCreated, CreateUserProfileListener)
        yield
```

**Dispatch Events:**

```python
@app.post("/users")
async def create_user(data: UserCreateSchema):
    user = await User.create(**data.dict())

    # Dispatch event - all listeners execute
    await Event.dispatch(UserCreated(
        user_id=user.id,
        email=user.email,
        name=user.name
    ))

    return {"id": user.id}
```

**Execution Policies:**

```python
# Immediate execution (default)
class SendEmailListener:
    policy = "immediate"  # Executes immediately

# Deferred execution (after transaction commits)
class UpdateSearchIndexListener:
    policy = "deferred"  # Waits for DB commit

# Background execution (via queue)
class GenerateReportListener:
    policy = "outbox"  # Executes as background task
```

### Observability

Neva includes built-in observability features:

**Structured Logging:**

```python
from neva.support.facade import Log

# Structured logs with context
Log.info("User logged in", user_id=123, ip="192.168.1.1")
Log.error("Payment failed", order_id=456, amount=99.99, error="Card declined")

# Automatic correlation IDs in logs (via middleware)
```

**Correlation Middleware:**

Automatically adds correlation IDs to track requests across services:

```python
from neva.obs import CorrelationMiddleware

app = App(middlewares=[CorrelationMiddleware])
```

**Profiling Middleware:**

Profile slow requests automatically:

```python
from neva.obs import ProfilerMiddleware

app = App(middlewares=[ProfilerMiddleware])
# Slow requests automatically profiled
```

## Database Integration

Neva uses Tortoise ORM with automatic lifecycle management:

**Define Models:**

```python
from tortoise import Model, fields

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
```

**Use in Routes:**

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user
```

Database connection/disconnection is handled automatically via the DatabaseServiceProvider.

## Comparison with FastAPI + dependency-injector

| Feature | FastAPI + DI | Neva |
|---------|-------------|------|
| **DI Container Setup** | Manual `containers.DeclarativeContainer` | Auto-configured via Application |
| **Service Registration** | Manual provider definitions | Service Providers with `register()` |
| **Lifecycle Management** | Manual startup/shutdown events | Provider `lifespan()` context managers |
| **Configuration** | YAML/JSON + env vars | Python files with validation |
| **Accessing Services** | `Depends(Provide[Container.service])` | Facades or standard DI |
| **Error Handling** | Exceptions / Optional | Result types |
| **Events** | Manual implementation | Built-in event system |
| **Logging** | Standard logging | Structured logging with context |
| **Observability** | Manual middleware | Built-in correlation + profiling |

## Advanced Patterns

### Custom Config Path

```python
from pathlib import Path

app = App(config_path=Path("/etc/myapp/config"))
```

### Dependency Injection in Routes

You can still use standard FastAPI dependency injection when needed:

```python
from dishka.integrations.fastapi import FromDishka

@app.get("/orders/{order_id}")
async def get_order(
    order_id: int,
    order_service: FromDishka[OrderService]  # Resolved from container
):
    return await order_service.get(order_id)
```

### Custom Lifespan Logic

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(app: App) -> AsyncIterator[None]:
    Log.info("🚀 Application starting")
    # Runs after all provider lifespans

    yield

    Log.info("👋 Application shutting down")

app = App(lifespan=app_lifespan)
```

## Development

```bash
# Install dependencies
uv sync

# Run linter
poe lint  # or: ruff check

# Format code
poe fmt   # or: ruff format

# Type check
poe tc    # or: ty check

# Run tests
pytest

# Build package
uv build
```

## Philosophy

Neva's design principles:

1. **Convention over Configuration** - Sensible defaults, minimal boilerplate
2. **Explicit over Implicit** - Result types, type hints, clear error handling
3. **FastAPI First** - Built on FastAPI, not replacing it
4. **Laravel-Inspired** - Service providers, facades, events from Laravel
5. **Python Idioms** - Leverages Python 3.12+ features (type parameters, pattern matching)

## When NOT to Use Neva

Neva might be overkill if you:

- Have a simple API with 3-4 routes and no complex dependencies
- Don't need lifecycle management or configuration structure
- Prefer a more minimal, explicit approach to everything
- Don't want to learn new patterns (service providers, facades)

For simple APIs, vanilla FastAPI is perfect. Neva shines when your application grows and you need structure.

## License

MIT

## Contributing

This is an internal tool for our team. If you find issues or have suggestions, open an issue or PR.
