from dataclasses import dataclass

from fastapi import (
    Depends, 
    HTTPException
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_master_db
from app.entities.user import User
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse
)
from app.utils.constants import A_USER_WITH_THIS_CONTACT_ALREADY_EXISTS, USER_CREATED_SUCCESSFULLY, USER_WITH_THIS_EMAIL_ALREADY_EXISTS


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
    
    def validate_email(self, email: str):
        """
            Validate if the email already exists in the database.
        """
        existing_user_by_email = self.db.query(User).filter(func.lower(User.email) == email.lower()).first()

        if existing_user_by_email:
            raise HTTPException(
                status_code=400,
                detail=USER_WITH_THIS_EMAIL_ALREADY_EXISTS
            )

    def validate_contact(self, contact: str):
        """
            Validate if the contact already exists in the database.
        """
        existing_user_by_contact = self.db.query(User).filter(func.lower(User.contact) == contact.lower()).first()

        if existing_user_by_contact:
            raise HTTPException(
                status_code=400,
                detail=A_USER_WITH_THIS_CONTACT_ALREADY_EXISTS
            )

    def create_user(self, request: UserCreationRequest) -> UserCreationResponse:
        """
            Create a new user in the database.
        """
        self.validate_email(request.email)
        self.validate_contact(request.contact)

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