from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_master_db
from app.entities.user import User
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse
)
from app.utils.constants import USER_CREATED_SUCCESSFULLY


@dataclass
class UserService:
    db: Session = Depends(get_master_db)

    def get_active_user_by_email(self, email: str) -> User | None:
        """
            Retrieve a user by their email address.
        """
        return (
            self.db.query(User)
            .filter(
                User.email == email,
                User.is_active == True
            ).first()   
        )

    def create_user(self, request: UserCreationRequest) -> User:
        user = User(
            name=request.name,
            email=request.email,
            password=request.password,
            role=request.role,
            contact=request.contact,
            branch_id=request.branch_id
        )

        self.db.add(user)
        self.db.commit()

        return UserCreationResponse(message=USER_CREATED_SUCCESSFULLY)
    
    def get_all_users(self):
        return self.db.query(User).all()