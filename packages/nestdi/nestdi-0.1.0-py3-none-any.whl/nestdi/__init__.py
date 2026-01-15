import inspect
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, cast, overload
import typing

__all__ = [
    "ProviderScope",
    "ProviderType",
    "CircularDependencyError",
    "ProviderNotFoundError",
    "Provider",
    "Injectable",
    "DIContainer",
    "ModuleClass",
    "Module",
]


type Factory[T] = Callable[[], T]


class ProviderScope(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    REQUEST = "request"


class ProviderType(Enum):
    CLASS = "class"
    VALUE = "value"
    FACTORY = "factory"


class CircularDependencyError(Exception):
    pass


class ProviderNotFoundError(Exception):
    pass


class Provider:
    def __init__(
        self,
        provide: Any,
        use_class: Optional[type[Any]] = None,
        use_value: Any = None,
        use_factory: Optional[Callable[..., Any]] = None,
        inject: Optional[List[type[Any]]] = None,
        scope: ProviderScope = ProviderScope.SINGLETON,
    ):
        self.provide = provide
        self.use_class = use_class
        self.use_value = use_value
        self.use_factory = use_factory
        self.inject = inject or []
        self.scope = scope

        if use_class:
            self.type = ProviderType.CLASS
        elif use_value is not None:
            self.type = ProviderType.VALUE
        elif use_factory:
            self.type = ProviderType.FACTORY
        else:
            self.type = ProviderType.CLASS
            self.use_class = provide


def Injectable[T](
    scope: ProviderScope = ProviderScope.SINGLETON,
) -> Callable[[type[T]], type[T]]:
    def decorator(cls: type[T]) -> type[T]:
        setattr(cls, "__injectable__", True)
        setattr(cls, "__scope__", scope)
        return cls

    return decorator


class DIContainer:
    _global_providers: Dict[Any, Provider] = {}
    __controllers: List[type] = []

    def __init__(self, name: str = "root"):
        self.name = name
        self._providers: Dict[Any, Provider] = {}
        self._instances: Dict[Any, Any] = {}
        self._resolving: set[Any] = set()
        self._exports: List[Any] = []
        self._imports: List["ModuleClass"] = []
        self._controllers: List[type] = []

    @property
    def providers(self):
        return {
            **self._global_providers,
            **self._providers,
        }

    def register_provider(self, provider: Provider, global_di: bool = False):
        if global_di:
            DIContainer._global_providers[provider.provide] = provider
        else:
            self._providers[provider.provide] = provider

    def register_controller(self, controller: type, global_di: bool = False):
        provider = Provider(provide=controller, use_class=controller)
        self.register_provider(provider, global_di=global_di)
        DIContainer.__controllers.append(controller)

    def register_value(self, token: type | str, value: Any, global_di: bool = False):
        provider = Provider(provide=token, use_value=value)
        self.register_provider(provider, global_di=global_di)

    def register_class(
        self,
        token: type | str,
        cls: type,
        scope: ProviderScope = ProviderScope.SINGLETON,
        global_di: bool = False,
    ):
        provider = Provider(provide=token, use_class=cls, scope=scope)
        self.register_provider(provider, global_di=global_di)

    def register_factory(
        self,
        token: type | str,
        factory: Callable[..., Any],
        inject: List[type] | None = None,
        scope: ProviderScope = ProviderScope.SINGLETON,
        global_di: bool = False,
    ):
        provider = Provider(
            provide=token, use_factory=factory, inject=inject or [], scope=scope
        )
        self.register_provider(provider, global_di=global_di)

    @overload
    def get[T](self, token: type[T]) -> T: ...

    @overload
    def get(self, token: str) -> Any: ...

    def get(self, token: Any, new: bool = False) -> Any:
        is_factory = False

        if typing.get_origin(token) == Factory:
            token = typing.get_args(token)[0]
            is_factory = True

            return lambda: self.get(token)

        provider = self.providers.get(token)

        if provider and provider.scope in (
            ProviderScope.REQUEST,
            ProviderScope.TRANSIENT,
        ):
            new = True

        if token in self._instances and not new:
            return self._instances[token]

        if token not in self.providers:
            for module in self._imports:
                if token in module.container._exports:
                    return module.container.get(token)

            raise ProviderNotFoundError(
                f"Provider '{token}' not found in '{self.name}'"
            )

        if token in self._resolving:
            raise CircularDependencyError(
                f"Circular dependency detected while resolving '{token}'"
            )

        self._resolving.add(token)

        try:
            provider = self.providers[token]
            instance = self._create_instance(provider)

            if provider.scope == ProviderScope.SINGLETON:
                self._instances[token] = instance

            return instance if not is_factory else lambda: instance
        finally:
            self._resolving.remove(token)

    def get_controllers(self) -> List[Any]:
        controllers: List[Any] = []
        for controller in self.__controllers:
            controller_instance = self._get_controller_recursive(controller)
            if controller_instance is not None:
                controllers.append(controller_instance)

        return controllers

    def _get_controller_recursive(self, controller: type) -> Optional[Any]:
        try:
            instance = cast(Any, self.get(controller))
            return instance
        except ProviderNotFoundError:
            pass

        for module in self._imports:
            result = module.container._get_controller_recursive(controller)
            if result is not None:
                return result

        return None

    def _create_instance(self, provider: Provider) -> Any:
        if provider.type == ProviderType.VALUE:
            return provider.use_value

        elif provider.type == ProviderType.CLASS:
            return self._instantiate_class(provider.use_class)  # type: ignore

        elif provider.type == ProviderType.FACTORY:
            deps = [self.get(dep) for dep in provider.inject]
            return provider.use_factory(*deps)  # type: ignore

        raise ValueError(f"Unknown provider type: {provider.type}")

    def _instantiate_class(self, cls: type) -> Any:
        sig = inspect.signature(cls.__init__)
        dependencies = {}

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            if param.annotation != inspect.Parameter.empty:
                dep_type = param.annotation
                dependencies[param_name] = self.get(dep_type)

        return cls(**dependencies)

    def set_exports(self, exports: List[Any]):
        self._exports = exports

    def add_import(self, module: "ModuleClass"):
        self._imports.append(module)


class ModuleClass:
    def __init__(
        self,
        providers: List[Provider | type] | None = None,
        imports: List["ModuleClass"] | None = None,
        exports: List[type | str] | None = None,
        controllers: List[type] | None = None,
        name: str = "unnamed",
        *,
        cls: type | None = None,
    ):
        self.container = DIContainer(name=name)
        self.name = name
        self.cls = cls
        self.__global__ = getattr(cls, "__global__", False)

        if providers:
            for provider in providers:
                if isinstance(provider, Provider):
                    self.container.register_provider(
                        provider, global_di=self.__global__
                    )
                else:
                    scope = getattr(provider, "__scope__", ProviderScope.SINGLETON)
                    self.container.register_class(
                        provider, provider, scope=scope, global_di=self.__global__
                    )

        if controllers:
            for controller in controllers:
                self.container.register_controller(
                    controller, global_di=self.__global__
                )

        if imports:
            for module in imports:
                self.container.add_import(module)

        if exports:
            self.container.set_exports(exports)

    @overload
    def get[T](self, token: type[T]) -> T: ...

    @overload
    def get(self, token: str) -> Any: ...

    def get(self, token: Any) -> Any:
        return self.container.get(token)


def Module(
    providers: List[Provider | type] | None = None,
    imports: List["ModuleClass"] | None = None,
    exports: List[type | str] | None = None,
    controllers: List[type] | None = None,
    name: str | None = None,
):
    def wrapper(
        cls: type,
    ):
        return ModuleClass(
            providers=providers,
            imports=imports,
            exports=exports,
            controllers=controllers,
            name=name or cls.__name__,
            cls=cls,
        )

    return wrapper


def Controller[T](scope: ProviderScope = ProviderScope.SINGLETON):
    def wrapper(cls: type[T]):
        setattr(cls, "__controller__", True)
        setattr(cls, "__injectable__", True)
        setattr(cls, "__scope__", scope)
        dec = Injectable(scope=scope)
        return dec(cls)

    return wrapper


def Global():
    def wrapper(cls: type):
        setattr(cls, "__global__", True)
        return cls

    return wrapper
