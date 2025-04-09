from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base


class Bus(Base):
    __tablename__ = "buses"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    branch_id: int = sa.Column(sa.Integer, sa.ForeignKey("branches.id"), nullable=False) 
    bus_number: str = sa.Column(sa.String(10), nullable=False)
    bus_type: str = sa.Column(sa.String(10), nullable=False) 
    total_seats: int = sa.Column(sa.Integer, nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) 