from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    bus_id: int = sa.Column(sa.Integer, sa.ForeignKey("buses.id") ,nullable=False) 
    route_id: int = sa.Column(sa.Integer, sa.ForeignKey("routes.id"), nullable=False)
    departure_time: datetime = sa.Column(sa.DateTime, nullable=False)
    arrival_time: datetime = sa.Column(sa.DateTime, nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 