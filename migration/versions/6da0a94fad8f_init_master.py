"""init master

Revision ID: 6da0a94fad8f
Revises: 
Create Date: 2023-06-04 20:24:53.919957

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa

from app.utils.constants import MASTER_SCHEMA
from app.utils.enums import Roles
from app.utils.utils import get_randome_str


# revision identifiers, used by Alembic.
revision = "6da0a94fad8f"
down_revision = None
branch_labels = None
depends_on = None
schema_name = get_randome_str()

  
def upgrade() -> None:
    if op.get_context().dialect.default_schema_name != MASTER_SCHEMA:
        pass
        return
    # Create the schema and commit it immediately
    # This ensures the schema exists before we try to create tables in it
    conn = op.get_bind()
    conn.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {schema_name.lower()}"))
    conn.execute(sa.text("COMMIT"))
    
    # Now create tables in that schema
    op.create_table(
        "branches",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("city", sa.String(length=50), nullable=False),
        sa.Column("domain_name", sa.String(length=10), nullable=False),
        sa.Column("schema", sa.String(length=50), nullable=False),
        sa.Column("logo_path", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id")
    )
    
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=20), nullable=False),
        sa.Column("contact", sa.String(length=50), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(['branch_id'], ['branches.id']),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("contact")
    )
    
    op.create_index(op.f("ix_users_password"), "users", ["password"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    
    # Insert initial branch data
    branch_insert = sa.sql.table(
        'branches',
        sa.sql.column('name', sa.String),
        sa.sql.column('city', sa.String),
        sa.sql.column('domain_name', sa.String),
        sa.sql.column('schema', sa.String),
        sa.sql.column('logo_path', sa.String),
        sa.sql.column('created_at', sa.DateTime),
        sa.sql.column('updated_at', sa.DateTime),
        sa.sql.column('is_active', sa.Boolean),
        schema=MASTER_SCHEMA
    )
    
    now = datetime.utcnow()
    op.bulk_insert(
        branch_insert,
        [
            {
                "name": "Bus Travels",
                "city": "Kadapa",
                "domain_name": "kdp",
                "schema": schema_name.lower(),
                "logo_path": None,
                "created_at": now,
                "updated_at": now,
                "is_active": True
            }
        ]
    )
    
    # Get the branch ID for user creation
    branch_id_result = conn.execute(
        sa.text(f"SELECT id FROM {MASTER_SCHEMA}.branches WHERE name = 'Bus Travels' LIMIT 1")
    ).fetchone()
    branch_id = branch_id_result[0] if branch_id_result else None
    
    # Insert initial user data
    user_insert = sa.sql.table(
        'users',
        sa.sql.column('name', sa.String),
        sa.sql.column('email', sa.String),
        sa.sql.column('password', sa.String),
        sa.sql.column('contact', sa.String),
        sa.sql.column('role', sa.String),
        sa.sql.column('branch_id', sa.Integer),
        sa.sql.column('created_at', sa.DateTime),
        sa.sql.column('updated_at', sa.DateTime),
        sa.sql.column('is_active', sa.Boolean),
        schema=MASTER_SCHEMA
    )
    
    op.bulk_insert(
        user_insert,
        [
            {
                "name": "Super Admin",  # Using a string instead of Roles.SuperAdmin for clarity
                "email": "siva.teja@in.nspglobaltech.com",
                "password": "String@123",
                "contact": "1234567890",
                "role": Roles.SuperAdmin,  # Assuming Roles.SuperAdmin is a string like this
                "branch_id": branch_id,
                "created_at": now,
                "updated_at": now,
                "is_active": True
            }
        ]
    )


def downgrade() -> None:
    if op.get_context().dialect.default_schema_name != MASTER_SCHEMA:
        pass
        return
    # Get the schema name from the database
    conn = op.get_bind()
    result = conn.execute(
        sa.text("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'schema_%' ORDER BY schema_name DESC LIMIT 1")
    ).fetchone()
    
    if result:
        schema_name = result[0]
        
        # Delete inserted user data
        conn.execute(sa.text(f"DELETE FROM {MASTER_SCHEMA}.users WHERE email = 'siva.teja@in.nspglobaltech.com'"))
        
        # Delete inserted branch data
        conn.execute(sa.text(f"DELETE FROM {MASTER_SCHEMA}.branches WHERE name = 'Bus Travels'"))
        
        # Drop tables in the schema
        op.drop_index(op.f("ix_users_email"), table_name="users", schema=schema_name)
        op.drop_index(op.f("ix_users_password"), table_name="users", schema=schema_name)
        op.drop_table("users", schema=schema_name)
        op.drop_table("branches", schema=schema_name)
        
        # Drop the schema
        conn.execute(sa.text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))