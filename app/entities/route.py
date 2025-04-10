from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

from app.connectors.database_connector import Base


class Route(Base):
    __tablename__ = "routes"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    stops: list = sa.Column(JSON, nullable=False) 
    source: str = sa.Column(sa.String(50), nullable=False) 
    destination: str = sa.Column(sa.String(50), nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())