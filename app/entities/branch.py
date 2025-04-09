from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base



class Branch(Base):
    __tablename__ = "branches"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    city: str = sa.Column(sa.String(50), nullable=False)
    domain_name: str = sa.Column(sa.String(10), nullable=False)
    schema: str = sa.Column(sa.String(50), nullable=False) 
    logo_path: str = sa.Column(sa.String(500), nullable=True) 
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()) 
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) 