import os
from datetime import datetime
from dotenv import load_dotenv
import traceback

from fastapi import Request
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker, 
    Session
)

from app.utils.constants import ( 
    MASTER_SCHEMA
)

load_dotenv()  # Load environment variables from .env file

SQL_USER = os.getenv("POSTGRES_USER")
SQL_PASSWORD = os.getenv("POSTGRES_PASSWORD")
SQL_HOST = os.getenv("POSTGRES_HOST")
SQL_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = f"postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DB}"

db_connections: dict[str, dict[str, Session | datetime]] = {}

# Create a SQLAlchemy engine
engine = sa.create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=280,
    pool_size=200,
    max_overflow=0,
)
# Create a base class for declarative models
Base = declarative_base(metadata=sa.MetaData())


class TenantNotFoundError(Exception):
    def __init__(self, id):
        self.message = f"Tenant with ID '{id}' not found!"
        super().__init__(self.message)


def get_master_database():
    return build_db_session(MASTER_SCHEMA)


def build_db_session(schema: str) -> Session:
    if schema:
        schema_translate_map = dict(tenant=schema)
    else:
        raise TenantNotFoundError("Tenant %s not found!" % schema)
    
    connectable = engine.execution_options(schema_translate_map=schema_translate_map)
    connectable.dialect.default_schema_name = schema
    db = sessionmaker(bind=connectable, expire_on_commit=False)()
    db.execute(sa.text('set search_path to "%s"' % schema))

    return db


def get_connected_schema(db: Session) -> str:
    return db.connection().dialect.default_schema_name or ""


def get_tenant_db(request: Request):
    branch_id = request.state.user.branch_id
    master_db = get_master_database()

    result = master_db.execute(
        sa.text("SELECT schema FROM branches WHERE id='" + branch_id + "';")
    ).fetchall()

    master_db.close()

    if not result or not result[0] or not result[0][0]:
        raise TenantNotFoundError(branch_id)
    
    print("transaction starting, opening db. ", datetime.now())
    db = build_db_session(result[0][0])

    try:
        yield db
    finally:
        try:
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()
        finally:
            db.close()

        print("transaction completed, closing db. ", datetime.now())


def get_master_db():
    print("transaction starting, opening master db. ", datetime.now())
    db = get_master_database()

    try:
        yield db
    finally:
        try:
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()
        finally:
            db.close()

        print("transaction completed, closing master db. ", datetime.now())
