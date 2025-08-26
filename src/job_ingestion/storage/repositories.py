from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def get_engine(url: str, echo: bool = False) -> Engine:
    """Create a SQLAlchemy Engine for the given URL.

    Adds SQLite-specific connect_args for thread use in dev/tests.
    """
    connect_args: dict[str, object] | None = None
    if url.startswith("sqlite"):
        # Needed when using SQLite with threaded apps/tools
        connect_args = {"check_same_thread": False}
    args: dict[str, object] = connect_args or {}
    return create_engine(url, echo=echo, future=True, connect_args=args)


def get_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    """Return a configured sessionmaker bound to the engine."""
    return sessionmaker(bind=engine, class_=Session, expire_on_commit=False, future=True)


@contextmanager
def get_session(session_maker: sessionmaker[Session]) -> Generator[Session, None, None]:
    """Context manager that yields a Session and handles commit/rollback."""
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
