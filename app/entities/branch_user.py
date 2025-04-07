from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base 
from app.utils.hasher import Hasher


class BranchUser(Base):
    __tablename__ = "branch_users"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(256), nullable=False)
    username: str = sa.Column(sa.String(256), nullable=False, index=True, unique=True)
    __password: str = sa.Column(name="password", type_=sa.String(500), nullable=False, index=True)
    contact: str = sa.Column(sa.String(500), nullable=False, unique=True)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute, use verify_password method for verifying')
    
    @password.setter
    def password(self, password:str):
        self.__password = Hasher.get_password_hash(password)
    
    def verify_password(self, password:str):
        return Hasher.verify_password(password,self.__password)