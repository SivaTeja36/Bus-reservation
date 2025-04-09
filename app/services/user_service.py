from dataclasses import dataclass
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_master_db
from app.entities.user import User
from app.utils.enums import Roles


@dataclass
class UserService:
    db: Session = Depends(get_master_db)

    def create_user(
        self, 
        name: str, 
        username: EmailStr, 
        password: str, 
        role: str, 
        contact: str
    ) -> User:
        user = User(
            name=name, 
            username=username, 
            password=password, 
            role=role, 
            contact=contact
        )

        self.db.add(user)
        self.db.commit()

        return user

    def get_all_users(self):
        return self.db.query(User).all()

    def validate_user(self, username: EmailStr, password: str) -> User | None:
        # this logic should be remvoed once we create some users.
        if self.db.query(User).count() == 0:
            return self.create_user(
                name=username.split("@")[0],
                username=username,
                password=password,
                role=Roles.SuperAdmin,
                contact="0987654321",
            )
        
        user = self.db.query(User).where(User.username == username).first()  # type: ignore
        
        if user and user.verify_password(password):
            return user
        else:
            return None
