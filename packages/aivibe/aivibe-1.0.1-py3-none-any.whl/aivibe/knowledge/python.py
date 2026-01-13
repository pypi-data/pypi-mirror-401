"""
AIVibe Python Knowledge Module

Complete Python 3.12+ coding standards, FastAPI patterns,
async programming, type hints, and backend development.
"""


class PythonKnowledge:
    """Comprehensive Python development knowledge."""

    VERSION = "3.12"
    FASTAPI_VERSION = "0.111"
    PYDANTIC_VERSION = "2.7"

    LANGUAGE_FEATURES = {
        "type_hints": {
            "basic": "def greet(name: str) -> str:",
            "optional": "def find(id: str) -> User | None:",
            "union": "def process(data: str | bytes) -> Result:",
            "list": "def get_all() -> list[User]:",
            "dict": "def config() -> dict[str, Any]:",
            "callable": "handler: Callable[[Request], Response]",
            "typevar": "T = TypeVar('T', bound=BaseModel)",
            "generic": "class Repository(Generic[T]):",
            "literal": "status: Literal['active', 'inactive']",
            "typeddict": """
class UserDict(TypedDict):
    id: str
    name: str
    email: NotRequired[str]""",
            "self_type": "def clone(self) -> Self:",
            "paramspec": "P = ParamSpec('P') for decorator typing",
        },
        "pattern_matching": {
            "basic": """
match command:
    case "quit":
        return exit()
    case "help":
        return show_help()
    case _:
        return unknown_command()""",
            "with_guards": """
match point:
    case (x, y) if x == y:
        return "diagonal"
    case (x, y):
        return f"point({x}, {y})" """,
            "class_patterns": """
match event:
    case Click(x=x, y=y):
        handle_click(x, y)
    case KeyPress(key="enter"):
        submit()
    case KeyPress(key=k):
        handle_key(k)""",
            "or_patterns": """
match status:
    case 200 | 201 | 204:
        return "success"
    case 400 | 404:
        return "client_error"
    case 500 | 502 | 503:
        return "server_error" """,
        },
        "dataclasses": {
            "basic": """
from dataclasses import dataclass, field

@dataclass
class User:
    id: str
    name: str
    email: str
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)""",
            "frozen": "@dataclass(frozen=True) for immutability",
            "slots": "@dataclass(slots=True) for memory efficiency",
            "kw_only": "@dataclass(kw_only=True) for keyword-only args",
            "post_init": """
def __post_init__(self):
    if not self.email:
        raise ValueError("Email required")""",
        },
        "context_managers": {
            "class_based": """
class DatabaseConnection:
    def __enter__(self) -> 'DatabaseConnection':
        self.conn = connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.conn.close()
        return False  # Don't suppress exceptions""",
            "contextmanager": """
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name}: {time.time() - start:.2f}s")""",
            "asynccontextmanager": """
from contextlib import asynccontextmanager

@asynccontextmanager
async def db_session():
    session = await create_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()""",
        },
        "decorators": {
            "function_decorator": """
from functools import wraps

def retry(max_attempts: int = 3):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(2 ** attempt)
            raise RuntimeError("Unreachable")
        return wrapper
    return decorator""",
            "class_decorator": """
def singleton(cls: type[T]) -> type[T]:
    instances: dict[type, T] = {}
    @wraps(cls)
    def wrapper(*args, **kwargs) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper""",
        },
    }

    ASYNC_PROGRAMMING = {
        "basics": {
            "async_def": "async def fetch_data() -> Data:",
            "await": "result = await async_operation()",
            "gather": "results = await asyncio.gather(task1, task2)",
            "create_task": "task = asyncio.create_task(background_job())",
            "wait": "done, pending = await asyncio.wait(tasks)",
            "timeout": """
async with asyncio.timeout(10):
    result = await slow_operation()""",
            "taskgroup": """
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_a())
    task2 = tg.create_task(fetch_b())
# Both complete or all cancelled on exception""",
        },
        "generators": {
            "async_generator": """
async def fetch_pages() -> AsyncGenerator[Page, None]:
    page = 1
    while True:
        data = await fetch_page(page)
        if not data:
            break
        yield data
        page += 1""",
            "async_for": """
async for page in fetch_pages():
    process(page)""",
            "async_comprehension": """
results = [item async for item in async_iterator]
filtered = [x async for x in items if await is_valid(x)]""",
        },
        "concurrency": {
            "semaphore": """
semaphore = asyncio.Semaphore(10)

async def rate_limited_fetch(url: str) -> Response:
    async with semaphore:
        return await client.get(url)""",
            "lock": """
lock = asyncio.Lock()

async def update_shared_state():
    async with lock:
        state.value = await compute_new_value()""",
            "event": """
event = asyncio.Event()

async def waiter():
    await event.wait()
    print("Event triggered!")

async def trigger():
    event.set()""",
            "queue": """
queue: asyncio.Queue[Task] = asyncio.Queue()

async def producer():
    await queue.put(task)

async def consumer():
    task = await queue.get()
    try:
        await process(task)
    finally:
        queue.task_done()""",
        },
    }

    FASTAPI = {
        "basic_app": """
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI(
    title="API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str) -> UserResponse:
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate) -> UserResponse:
    return await user_service.create(data)""",
        "dependencies": """
from fastapi import Depends, Header

async def get_current_user(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    user = await db.get(User, payload["sub"])
    if not user:
        raise HTTPException(401, "Invalid token")
    return user

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user""",
        "middleware": """
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(f"{request.method} {request.url.path} - {duration:.2f}s")
        return response

app.add_middleware(LoggingMiddleware)""",
        "error_handling": """
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message}
    )""",
        "background_tasks": """
from fastapi import BackgroundTasks

async def send_notification(user_id: str, message: str):
    await notification_service.send(user_id, message)

@app.post("/orders")
async def create_order(
    data: OrderCreate,
    background_tasks: BackgroundTasks
):
    order = await order_service.create(data)
    background_tasks.add_task(send_notification, order.user_id, "Order created")
    return order""",
        "websocket": """
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for conn in self.connections:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)""",
    }

    PYDANTIC = {
        "models": """
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_default=True,
    )

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\\w.-]+@[\\w.-]+\\.\\w+$')
    age: int = Field(default=0, ge=0, le=150)
    tags: list[str] = Field(default_factory=list)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.lower()

    @model_validator(mode='after')
    def validate_model(self) -> 'User':
        if self.age < 13 and 'adult' in self.tags:
            raise ValueError("Invalid age for adult tag")
        return self""",
        "computed_fields": """
from pydantic import computed_field

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" """,
        "serialization": """
from pydantic import field_serializer

class User(BaseModel):
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime) -> str:
        return dt.isoformat()

# Usage
user.model_dump()  # dict
user.model_dump_json()  # JSON string
User.model_validate(data)  # from dict
User.model_validate_json(json_str)  # from JSON""",
    }

    SQLALCHEMY = {
        "async_setup": """
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)""",
        "repository": """
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> User | None:
        return await self.session.get(User, id)

    async def get_all(self, limit: int = 100) -> list[User]:
        result = await self.session.execute(
            select(User).order_by(User.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, data: UserCreate) -> User:
        user = User(id=str(uuid4()), **data.model_dump())
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, id: str, data: UserUpdate) -> User | None:
        user = await self.get_by_id(id)
        if not user:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.session.flush()
        return user""",
    }

    CODING_STANDARDS = {
        "naming": {
            "modules": "snake_case - user_service.py",
            "classes": "PascalCase - UserRepository",
            "functions": "snake_case - get_user_by_id",
            "variables": "snake_case - user_count",
            "constants": "SCREAMING_SNAKE_CASE - MAX_RETRIES",
            "private": "_prefix - _internal_method",
            "dunder": "__name__ for special methods only",
        },
        "formatting": {
            "tool": "black + isort + ruff",
            "line_length": 88,
            "indentation": "4 spaces",
            "quotes": "double quotes for strings",
            "trailing_comma": "always in multi-line",
        },
        "imports": {
            "order": "stdlib, third-party, local (isort)",
            "absolute": "prefer absolute imports",
            "explicit": "from module import specific_item",
            "avoid": "from module import * (wildcard)",
        },
        "docstrings": {
            "module": '"""Module description."""',
            "function": '''
def process_data(data: dict[str, Any], strict: bool = False) -> Result:
    """
    Process the input data and return a result.

    Args:
        data: The input data dictionary
        strict: If True, raises on validation errors

    Returns:
        Result object with processed data

    Raises:
        ValidationError: If data is invalid and strict=True
    """''',
            "class": '''
class DataProcessor:
    """
    Processes data from various sources.

    Attributes:
        source: The data source identifier
        config: Processing configuration

    Example:
        >>> processor = DataProcessor("api")
        >>> result = processor.process(data)
    """''',
        },
        "error_handling": {
            "specific": "except ValueError as e: (specific exceptions)",
            "avoid_bare": "never use bare except:",
            "context": "raise NewError('msg') from original_error",
            "logging": "logger.exception('Failed') in except block",
        },
    }

    TESTING = {
        "pytest": """
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
async def db_session():
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def mock_user_service():
    return AsyncMock(spec=UserService)

class TestUserService:
    @pytest.mark.asyncio
    async def test_get_user_success(self, db_session, mock_user_service):
        # Arrange
        expected = User(id="1", name="Test")
        mock_user_service.get.return_value = expected

        # Act
        result = await mock_user_service.get("1")

        # Assert
        assert result == expected
        mock_user_service.get.assert_called_once_with("1")

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mock_user_service):
        mock_user_service.get.return_value = None
        result = await mock_user_service.get("999")
        assert result is None""",
        "fixtures": """
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client""",
    }

    DEPRECATED = {
        "patterns": [
            "async with loop.create_task() (use asyncio.create_task)",
            "typing.Optional (use X | None)",
            "typing.Union (use X | Y)",
            "typing.List/Dict/Set (use list/dict/set)",
            "@asyncio.coroutine (use async def)",
            "yield from (use await)",
            "loop.run_until_complete (use asyncio.run)",
            "datetime.utcnow() (use datetime.now(UTC))",
        ],
        "packages": [
            "aiohttp for new projects (prefer httpx)",
            "requests for async code (use httpx)",
            "PyJWT < 2.0 (security issues)",
            "pydantic v1 (migrate to v2)",
        ],
    }

    def get_all(self) -> dict:
        """Get complete Python knowledge."""
        return {
            "version": self.VERSION,
            "language_features": self.LANGUAGE_FEATURES,
            "async_programming": self.ASYNC_PROGRAMMING,
            "fastapi": self.FASTAPI,
            "pydantic": self.PYDANTIC,
            "sqlalchemy": self.SQLALCHEMY,
            "coding_standards": self.CODING_STANDARDS,
            "testing": self.TESTING,
            "deprecated": self.DEPRECATED,
        }

    def get_coding_standards(self) -> dict:
        """Get Python coding standards."""
        return self.CODING_STANDARDS

    def get_async_guide(self) -> dict:
        """Get async programming guide."""
        return self.ASYNC_PROGRAMMING

    def get_fastapi_patterns(self) -> dict:
        """Get FastAPI patterns."""
        return self.FASTAPI
