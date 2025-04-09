from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base



class Company(Base):
    __tablename__ = "companies"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    name: str = sa.Column(sa.String(50), nullable=False) 
    contact_person_name: str = sa.Column(sa.String(50), nullable=False)
    email: sa.Text = sa.Column(sa.Text, nullable=False)
    address: str = sa.Column(sa.String(300), nullable=False)
    phone_number: str = sa.Column(sa.String(50), nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) 