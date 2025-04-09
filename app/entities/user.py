from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base
from app.utils.enums import Roles
from app.utils.hasher import Hasher


class User(Base):
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(50), nullable=False)
    email: str = sa.Column(sa.String(100), nullable=False, index=True, unique=True)
    __password: str = sa.Column(name="password", type_=sa.String(20), nullable=False, index=True)
    contact: str = sa.Column(sa.String(50), nullable=False, unique=True)
    role: str = sa.Column(sa.String(50), nullable=False)
    branch_id: int = sa.Column(sa.Integer, sa.ForeignKey("branches.id"), nullable=True)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute, use verify_password method for verifying')
    
    @password.setter
    def password(self, password:str):
        self.__password = Hasher.get_password_hash(password)
    
    def verify_password(self, password:str):
        return Hasher.verify_password(password,self.__password)