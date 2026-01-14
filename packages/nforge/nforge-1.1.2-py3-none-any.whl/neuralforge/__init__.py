"""
NeuralForge - AI-Native Web Framework
Core Application Class
"""

__version__ = "1.1.2"

from typing import Dict, List, Optional, Callable, Any, Union
from datetime import datetime
import asyncio
import logging

from .config import Settings
from .serving.loader import ModelLoader
from .resources.manager import ResourceManager
from .db.manager import DatabaseManager
from .cache.manager import CacheManager
from .auth.manager import AuthManager
from .metrics.collector import MetricsCollector
from .routing.router import Router
from .middleware.base import MiddlewareStack
from .health.checker import HealthChecker
from .observability.tracer import TracingManager
from .grpc.server import GRPCServer

logger = logging.getLogger(__name__)


class NeuralForge:
    """
    Main NeuralForge application class.

    This is the central object that manages all framework components
    including models, resources, databases, caching, and routing.

    Example:
        >>> app = NeuralForge(title="My ML API", version="1.0.0")
        >>>
        >>> @app.endpoint("/predict")
        >>> async def predict(data: Input) -> Output:
        >>>     model = await app.models.load("classifier")
        >>>     return await model.predict([data])[0]
    """
    def __init__(
        self,
        title: str = "NeuralForge Application",
        version: str = "0.1.0",
        description: str = "",
        settings: Optional[Settings] = None,
        debug: bool = False,
        docs_url: str = "/docs",
        redoc_url: str = "/redoc",
        openapi_url: str = "/openapi.json",
    ):
        """
        Initialize NeuralForge application.

        Args:
            title: Application title
            version: Application version
            description: Application description
            settings: Configuration settings object
            debug: Enable debug mode
            docs_url: Path for API documentation
            redoc_url: Path for ReDoc documentation
            openapi_url: Path for OpenAPI schema
        """
        self.title = title
        self.version = version
        self.description = description
        self.debug = debug
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.openapi_url = openapi_url

        # Load settings
        self.settings = settings or Settings()
        # Initialize core components
        self._models: Optional[ModelLoader] = None
        self._resources: Optional[ResourceManager] = None
        self._db: Optional[DatabaseManager] = None
        self._cache: Optional[CacheManager] = None
        self._auth: Optional[AuthManager] = None
        self._metrics: Optional[MetricsCollector] = None
        self._tracing: Optional[TracingManager] = None
        self._health: Optional[HealthChecker] = None
        self._grpc_server: Optional[GRPCServer] = None
        self._grpc_enabled: bool = False

        # Routing
        self._router = Router()
        self._middleware_stack = MiddlewareStack()

        # Lifecycle hooks
        self._startup_handlers: List[Callable] = []
        self._shutdown_handlers: List[Callable] = []

        # State
        self._is_initialized = False
        self._start_time = datetime.now()

        # Auto-register health check endpoint
        self._register_health_check()
        self._is_running = False
        self._accepting_requests = True

        # Background tasks
        self._background_tasks: List[asyncio.Task] = []

        logger.info(f"Initialized {self.title} v{self.version}")

    # ========================================================================
    # Component Properties
    # ========================================================================

    @property
    def models(self) -> ModelLoader:
        """Get model loader for runtime model serving."""
        if self._models is None:
            self._models = ModelLoader(app=self)
        return self._models

    @property
    def resources(self) -> ResourceManager:
        """Get resource manager."""
        if self._resources is None:
            self._resources = ResourceManager(app=self)
        return self._resources

    @property
    def db(self) -> DatabaseManager:
        """Get database manager."""
        if self._db is None:
            # DatabaseManager requires database_url, not app
            from .config import Settings
            settings = Settings()
            self._db = DatabaseManager(database_url=settings.database_url)
        return self._db

    @property
    def cache(self) -> CacheManager:
        """Get cache manager."""
        if self._cache is None:
            self._cache = CacheManager(app=self)
        return self._cache

    @property
    def auth(self) -> AuthManager:
        """Get authentication manager."""
        if self._auth is None:
            self._auth = AuthManager(app=self)
        return self._auth

    @property
    def metrics(self) -> MetricsCollector:
        """Get metrics collector."""
        if self._metrics is None:
            self._metrics = MetricsCollector(app=self)
        return self._metrics

    @property
    def tracing(self) -> TracingManager:
        """Get tracing manager."""
        if self._tracing is None:
            self._tracing = TracingManager(app=self)
        return self._tracing

    @property
    def health(self) -> HealthChecker:
        """Get health checker."""
        if self._health is None:
            self._health = HealthChecker(app=self)
        return self._health

    @property
    def grpc(self) -> Optional[GRPCServer]:
        """Get gRPC server if enabled."""
        return self._grpc_server

    def enable_grpc(
        self,
        port: int = 50051,
        max_workers: int = 10,
        max_message_length: int = 100 * 1024 * 1024,
        enable_reflection: bool = True,
    ) -> GRPCServer:
        """
        Enable gRPC server alongside HTTP.

        Creates and configures a gRPC server that can be started
        alongside the main HTTP server.

        Args:
            port: gRPC server port (default: 50051)
            max_workers: Maximum worker threads
            max_message_length: Max message size in bytes (default: 100MB)
            enable_reflection: Enable server reflection for debugging

        Returns:
            GRPCServer instance for registering services

        Example:
            >>> app = NeuralForge()
            >>> grpc_server = app.enable_grpc(port=50051)
            >>>
            >>> @grpc_service("InferenceService")
            >>> class MyService(GRPCServicer):
            ...     async def Predict(self, request, context):
            ...         return PredictResponse(...)
            >>>
            >>> grpc_server.register_service(MyService)
        """
        if self._grpc_server is not None:
            logger.warning("gRPC already enabled, returning existing server")
            return self._grpc_server

        self._grpc_server = GRPCServer(
            port=port,
            max_workers=max_workers,
        )
        self._grpc_enabled = True

        logger.info(f"gRPC enabled on port {port}")
        return self._grpc_server

    async def start_grpc(self):
        """
        Start the gRPC server.

        Call this after enabling gRPC and registering services.
        """
        if self._grpc_server is None:
            raise RuntimeError("gRPC not enabled. Call enable_grpc() first.")

        await self._grpc_server.start()
        logger.info("gRPC server started")

    async def stop_grpc(self, grace: float = 5.0):
        """
        Stop the gRPC server gracefully.

        Args:
            grace: Grace period in seconds for pending requests
        """
        if self._grpc_server is not None:
            await self._grpc_server.stop(grace=grace)
            logger.info("gRPC server stopped")

    def _register_health_check(self):
        """
        Auto-register health check endpoint.

        Registers a /health endpoint that returns system status.
        """
        @self.endpoint("/health", methods=["GET"])
        async def health_check():
            """
            Health check endpoint.

            Returns:
                System health status including uptime and version
            """
            uptime_seconds = (datetime.now() - self._start_time).total_seconds()

            return {
                "status": "healthy",
                "version": self.version,
                "app_name": self.title,
                "uptime_seconds": uptime_seconds,
                "timestamp": datetime.now().isoformat()
            }

    # ========================================================================
    # Routing Decorators
    # ========================================================================

    def endpoint(
        self,
        path: str,
        methods: List[str] = None,
        tags: List[str] = None,
        **kwargs
    ):
        """
        Decorator to register an endpoint.

        Example:
            >>> @app.endpoint("/predict", methods=["POST"])
            >>> async def predict(data: Input) -> Output:
            >>>     return Output(...)
        """
        if methods is None:
            methods = ["GET"]

        def decorator(func: Callable):
            """Register function as route endpoint.

            Args:
                func: Endpoint function to register

            Returns:
                Registered function
            """
            self._router.add_route(
                path=path,
                endpoint=func,
                methods=methods,
                tags=tags or [],
                **kwargs
            )
            return func

        return decorator

    def route(self, path: str, methods: List[str] = None, **kwargs):
        """Alias for endpoint decorator."""
        return self.endpoint(path, methods, **kwargs)

    def get(self, path: str, **kwargs):
        """Decorator for GET endpoints."""
        return self.endpoint(path, methods=["GET"], **kwargs)

    def post(self, path: str, **kwargs):
        """Decorator for POST endpoints."""
        return self.endpoint(path, methods=["POST"], **kwargs)

    def put(self, path: str, **kwargs):
        """Decorator for PUT endpoints."""
        return self.endpoint(path, methods=["PUT"], **kwargs)

    def delete(self, path: str, **kwargs):
        """Decorator for DELETE endpoints."""
        return self.endpoint(path, methods=["DELETE"], **kwargs)

    def websocket(self, path: str, **kwargs):
        """
        Decorator to register WebSocket endpoint.

        Example:
            >>> @app.websocket("/ws")
            >>> async def websocket_endpoint(websocket: WebSocket):
            >>>     await websocket.accept()
            >>>     ...
        """
        def decorator(func: Callable):
            """Register function as WebSocket endpoint.

            Args:
                func: WebSocket handler function

            Returns:
                Registered function
            """
            self._router.add_websocket_route(path, func, **kwargs)
            return func
        return decorator

    def stream(self, path: str, methods: List[str] = None, **kwargs):
        """
        Decorator to register a streaming endpoint (SSE).

        The decorated function should return an async generator
        or a StreamingResponse/SSEResponse object.

        Example:
            >>> @app.stream("/generate")
            >>> async def generate_text(prompt: str):
            >>>     async for token in model.generate(prompt):
            >>>         yield {"token": token}

            >>> # Or with explicit response
            >>> @app.stream("/chat")
            >>> async def chat(message: str):
            >>>     return SSEResponse(generate_tokens(message))

        Args:
            path: URL path for the endpoint
            methods: HTTP methods (default: ["GET", "POST"])
            **kwargs: Additional route options
        """
        if methods is None:
            methods = ["GET", "POST"]

        def decorator(func: Callable):
            """Register function as streaming endpoint."""
            import functools
            from neuralforge.streaming import SSEResponse, SSEMessage

            @functools.wraps(func)
            async def streaming_wrapper(*args, **inner_kwargs):
                result = await func(*args, **inner_kwargs)

                # If already a specialized response object, return as-is
                from neuralforge.streaming import SSEResponse, TokenStreamResponse, StreamingResponse
                if isinstance(result, (SSEResponse, TokenStreamResponse, StreamingResponse)):
                    return result

                # If it's an async generator, wrap it in SSEResponse
                if hasattr(result, '__aiter__'):
                    async def wrapped_generator():
                        from neuralforge.streaming import SSEMessage
                        index = 0
                        async for item in result:
                            if isinstance(item, SSEMessage):
                                yield item
                            else:
                                yield SSEMessage(
                                    data=item,
                                    event="message",
                                    id=str(index)
                                )
                            index += 1
                        yield SSEMessage(
                            data={"finished": True},
                            event="done"
                        )

                    return SSEResponse(generator=wrapped_generator())

                # Otherwise treat as single response
                return result

            # Register the route
            streaming_wrapper._is_streaming = True
            self._router.add_route(path, streaming_wrapper, methods=methods, **kwargs)
            return streaming_wrapper

        return decorator


    # ========================================================================
    # Middleware
    # ========================================================================

    def add_middleware(self, middleware_class: type, **options):
        """
        Add middleware to the application.

        Args:
            middleware_class: Middleware class to add
            **options: Options to pass to middleware

        Example:
            >>> from neuralforge.middleware import CORSMiddleware
            >>> app.add_middleware(
            >>>     CORSMiddleware,
            >>>     allow_origins=["*"],
            >>>     allow_methods=["*"]
            >>> )
        """
        middleware = middleware_class(**options)
        self._middleware_stack.add(middleware)
        logger.info(f"Added middleware: {middleware_class.__name__}")

    def middleware(self, middleware_type: Union[str, Callable] = "http"):
        """
        Decorator to add middleware function.

        Example:
            >>> @app.middleware
            >>> # or
            >>> @app.middleware("http")
            >>> async def custom_middleware(request, call_next):
            >>>     # ...
        """
        if callable(middleware_type):
            func = middleware_type
            self._middleware_stack.add_function(func, "http")
            return func

        def decorator(func: Callable):
            self._middleware_stack.add_function(func, middleware_type)
            return func
        return decorator

    # ========================================================================
    # Lifecycle Hooks
    # ========================================================================

    def on_event(self, event_type: str):
        """
        Decorator to register event handler.

        Example:
            >>> @app.on_event("startup")
            >>> async def startup():
            >>>     print("Application starting...")
        """
        def decorator(func: Callable):
            """Register event handler.

            Args:
                func: Event handler function

            Returns:
                Original function
            """
            if event_type == "startup":
                self._startup_handlers.append(func)
            elif event_type == "shutdown":
                self._shutdown_handlers.append(func)
            else:
                raise ValueError(f"Unknown event type: {event_type}")
            return func
        return decorator

    def on_startup(self, func: Callable = None):
        """Decorator to register startup handler."""
        if func is None:
            return self.on_event("startup")
        self._startup_handlers.append(func)
        return func

    def on_shutdown(self, func: Callable = None):
        """Decorator to register shutdown handler."""
        if func is None:
            return self.on_event("shutdown")
        self._shutdown_handlers.append(func)
        return func

    # ========================================================================
    # Application Lifecycle
    # ========================================================================

    async def startup(self):
        """Run startup sequence."""
        if self._is_initialized:
            return

        logger.info(f"Starting {self.title}...")

        # Run startup handlers
        for handler in self._startup_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                logger.error(f"Error in startup handler: {e}", exc_info=True)
                raise

        self._is_initialized = True
        self._is_running = True
        logger.info("✓ Application started successfully")

    async def shutdown(self):
        """Run shutdown sequence."""
        if not self._is_running:
            return

        logger.info("Shutting down application...")

        # Stop accepting new requests
        self._accepting_requests = False

        # Cancel background tasks
        for task in self._background_tasks:
            task.cancel()

        # Wait for tasks to complete
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

        # Run shutdown handlers
        for handler in self._shutdown_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                logger.error(f"Error in shutdown handler: {e}", exc_info=True)

        # Cleanup components
        if self._models:
            await self._models.cleanup()
        if self._db:
            # DatabaseManager doesn't have cleanup, use dispose instead
            await self._db.engine.dispose()
        if self._cache:
            await self._cache.cleanup()

        self._is_running = False
        logger.info("✓ Application shutdown complete")

    # ========================================================================
    # ASGI Application Interface
    # ========================================================================

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        """
        ASGI application callable.

        This makes NeuralForge compatible with ASGI servers like Uvicorn.
        """
        if not self._is_initialized:
            await self.startup()

        # Apply middleware stack
        async def app(scope, receive, send):
            """ASGI application handler."""
            # Route the request
            await self._router.handle(scope, receive, send)

        await self._middleware_stack(scope, receive, send, app)

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def add_background_task(self, coro: Callable):
        """
        Add a background task.

        Example:
            >>> async def monitor_models():
            >>>     while True:
            >>>         await check_model_health()
            >>>         await asyncio.sleep(60)
            >>>
            >>> app.add_background_task(monitor_models())
        """
        task = asyncio.create_task(coro)
        self._background_tasks.append(task)
        return task

    def include_router(self, router, prefix: str = "", tags: List[str] = None):
        """
        Include routes from another router.

        Args:
            router: Router object to include
            prefix: URL prefix for all routes
            tags: Tags to add to all routes

        Example:
            >>> from neuralforge import Router
            >>> api_router = Router()
            >>>
            >>> @api_router.get("/users")
            >>> async def list_users():
            >>>     return []
            >>>
            >>> app.include_router(api_router, prefix="/api/v1", tags=["api"])
        """
        self._router.include_router(router, prefix=prefix, tags=tags or [])

    def mount(self, path: str, app: Any, name: str = None):
        """
        Mount a sub-application.

        Example:
            >>> from starlette.staticfiles import StaticFiles
            >>> app.mount("/static", StaticFiles(directory="static"), name="static")
        """
        self._router.mount(path, app, name=name)

    # ========================================================================
    # Configuration Helpers
    # ========================================================================

    def configure(self, **kwargs):
        """
        Update application configuration.

        Example:
            >>> app.configure(
            >>>     max_request_size=100 * 1024 * 1024,  # 100MB
            >>>     timeout=30.0
            >>> )
        """
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
            else:
                logger.warning(f"Unknown configuration key: {key}")

    def get_openapi_schema(self) -> Dict[str, Any]:
        """Generate OpenAPI schema for the application."""
        return self._router.get_openapi_schema(
            title=self.title,
            version=self.version,
            description=self.description
        )

    # ========================================================================
    # Development Helpers
    # ========================================================================

    def run(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        reload: bool = False,
        workers: int = 1,
        **kwargs
    ):
        """
        Run the application (development only).

        For production, use a proper ASGI server:
            uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

        Args:
            host: Host to bind to
            port: Port to bind to
            reload: Enable auto-reload
            workers: Number of worker processes
            **kwargs: Additional arguments passed to uvicorn
        """
        try:
            import uvicorn
        except ImportError:
            raise ImportError(
                "uvicorn is required to run the application. "
                "Install it with: pip install uvicorn"
            )

        if self.debug and not reload:
            reload = True

        uvicorn.run(
            self,
            host=host,
            port=port,
            reload=reload,
            workers=workers,
            **kwargs
        )

    def __repr__(self) -> str:
        """Return string representation of NeuralForge application."""
        return f"<NeuralForge(title='{self.title}', version='{self.version}')>"


# ============================================================================
# Convenience Router Class
# ============================================================================

class APIRouter:
    """
    Router for organizing related endpoints.

    Example:
        >>> router = APIRouter(prefix="/api/v1", tags=["api"])
        >>>
        >>> @router.get("/users")
        >>> async def list_users():
        >>>     return []
        >>>
        >>> app.include_router(router)
    """

    def __init__(
        self,
        prefix: str = "",
        tags: List[str] = None,
        dependencies: List[Any] = None
    ):
        """Initialize APIRouter.

        Args:
            prefix: URL prefix for all routes
            tags: Tags to apply to all routes
            dependencies: Dependencies for all routes
        """
        self.prefix = prefix
        self.tags = tags or []
        self.dependencies = dependencies or []
        self._routes = []

    def add_route(self, path: str, endpoint: Callable, **kwargs):
        """Add a route to the router."""
        self._routes.append({
            "path": self.prefix + path,
            "endpoint": endpoint,
            "tags": self.tags + kwargs.pop("tags", []),
            "dependencies": self.dependencies + kwargs.pop("dependencies", []),
            **kwargs
        })

    def get(self, path: str, **kwargs):
        """Decorator for GET endpoint."""
        def decorator(func: Callable):
            """Register GET endpoint.

            Args:
                func: Endpoint function

            Returns:
                Registered function
            """
            self.add_route(path, func, methods=["GET"], **kwargs)
            return func
        return decorator

    def post(self, path: str, **kwargs):
        """Decorator for POST endpoint."""
        def decorator(func: Callable):
            """Register POST endpoint.

            Args:
                func: Endpoint function

            Returns:
                Registered function
            """
            self.add_route(path, func, methods=["POST"], **kwargs)
            return func
        return decorator

    def put(self, path: str, **kwargs):
        """Decorator for PUT endpoint."""
        def decorator(func: Callable):
            """Register PUT endpoint.

            Args:
                func: Endpoint function

            Returns:
                Registered function
            """
            self.add_route(path, func, methods=["PUT"], **kwargs)
            return func
        return decorator

    def delete(self, path: str, **kwargs):
        """Decorator for DELETE endpoint."""
        def decorator(func: Callable):
            """Register DELETE endpoint.

            Args:
                func: Endpoint function

            Returns:
                Registered function
            """
            self.add_route(path, func, methods=["DELETE"], **kwargs)
            return func
        return decorator

    def include_router(self, router: "APIRouter"):
        """Include another router."""
        for route in router._routes:
            route["path"] = self.prefix + route["path"]
            route["tags"] = self.tags + route["tags"]
            self._routes.append(route)
