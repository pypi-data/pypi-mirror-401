# NestDI

NestDI is a lightweight and powerful Dependency Injection (DI) container for Python, heavily inspired by the architecture of [NestJS](https://nestjs.com/). It allows you to organize your code into modules, making your applications easier to maintain, test, and scale.

## 🚀 Features

- **Decorator-based**: Use `@Module()`, `@Injectable()`, and `@Controller()` to define your structure.
- **Scope Management**: Support for `SINGLETON`, `TRANSIENT`, and `REQUEST` scopes.
- **Automatic Injection**: Automatic dependency resolution through type hints in constructors.
- **Module System**: Encapsulation and reuse of logic through imports and exports.
- **Flexible Providers**: Support for classes, constant values, and factories.
- **Circular Dependency Detection**: Throws clear exceptions when cycles are detected.
- **Strongly Typed**: Full support for MyPy and Pyright with `.typed`.

## 📦 Installation

Since this project uses [PDM](https://pdm.fming.dev/), you can install it via:

```bash
pdm add nestdi
```

Or via pip (if published):

```bash
pip install nestdi
```

## 🛠️ Usage Guide

### 1. Defining Providers

Mark your classes with `@Injectable()` so NestDI can instantiate and inject them.

```python
from nestdi import Injectable

@Injectable()
class LoggingService:
    def log(self, message: str):
        print(f"[LOG]: {message}")

@Injectable()
class UserService:
    def __init__(self, logger: LoggingService):
        self.logger = logger

    def get_user(self):
        self.logger.log("Fetching user...")
        return {"id": 1, "name": "John Doe"}
```

### 2. Creating Modules

Modules organize related components.

```python
from nestdi import Module

@Module(
    providers=[LoggingService, UserService],
    exports=[UserService] # Export so other modules can use it
)
class UserModule:
    pass
```

### 3. Controllers and Root Container

Controllers are entry points for your logic.

```python
from nestdi import Controller, Module

@Controller()
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def detail(self):
        return self.user_service.get_user()

@Module(
    imports=[UserModule],
    controllers=[UserController]
)
class AppModule:
    pass
```

### 4. Initialization and Usage

```python
from nestdi import ModuleClass

# The @Module decorator returns a ModuleClass instance
app: ModuleClass = AppModule

# Getting the resolved controller
user_controller = app.get(UserController)
print(user_controller.detail())
```

## 🌍 Global Modules

If you want a module's providers to be available throughout the application without needing to import it in every module, use the `@Global()` decorator.

```python
from nestdi import Module, Global, Injectable

@Injectable()
class GlobalService:
    pass

@Global()
@Module(
    providers=[GlobalService],
    exports=[GlobalService]
)
class CommonModule:
    pass
```

## 📐 Provider Scopes

You can define how instances are created:

- **ProviderScope.SINGLETON** (Default): A single instance is created and shared across the entire application.
- **ProviderScope.TRANSIENT**: A new instance is created every time the provider is requested.
- **ProviderScope.REQUEST**: A new instance is created for each "request" (useful in web contexts).

```python
from nestdi import Injectable, ProviderScope

@Injectable(scope=ProviderScope.TRANSIENT)
class GeneratorService:
    pass
```

## 🏭 Factory Providers

```python
from nestdi import Provider, Module

def connection_factory(config_service: ConfigService):
    return DatabaseConnection(config_service.db_url)

@Module(
    providers=[
        Provider(
            provide="DATABASE_CONNECTION",
            use_factory=connection_factory,
            inject=[ConfigService]
        )
    ]
)
class DatabaseModule:
    pass
```

## 📝 License

This project is licensed under the [MIT](LICENSE) License.
