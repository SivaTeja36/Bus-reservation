from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    bus_id: int = sa.Column(sa.Integer, sa.ForeignKey("buses.id"), nullable=False)
    seat_number: int = sa.Column(sa.Integer, nullable=False) 
    passenger_name: str = sa.Column(sa.String(50), nullable=False)
    passenger_contact: str = sa.Column(sa.String(20), nullable=False)
    passenger_email: str = sa.Column(sa.String(50), nullable=False)
    status: str = sa.Column(sa.String(50), nullable=False) 
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 