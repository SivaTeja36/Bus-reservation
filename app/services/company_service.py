from dataclasses import dataclass

from automapper import mapper
from fastapi import (
    Depends, 
    HTTPException
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.connectors.database_connector import (
    get_tenant_db
)
from app.entities.branch import Branch
from app.entities.company import Company
from app.models.company_models import (
    CompanyRequest, 
    CompanyResponse,
    GetCompanyResponse
)
from app.utils.constants import (
    A_COMPANY_WITH_THIS_NAME_ALREADY_EXISTS, 
    A_COMPANY_WITH_THIS_EMAIL_ALREADY_EXISTS,
    COMPANY_CREATED_SUCCESSFULLY,
    COMPANY_DELETED_SUCCESSFULLY,
    COMPANY_NOT_FOUND,
    COMPANY_UPDATED_SUCCESSFULLY
)



@dataclass
class CompanyService:
    db: Session = Depends(get_tenant_db)
    
    def validate_company_name(self, name: str):
        """
            Validate company name for uniqueness.
        """
        existing_company = (
            self.db.query(Company)
            .filter(func.lower(Company.name) == name.lower())
            .first()
        )

        if existing_company:
            raise HTTPException(
                status_code=400,
                detail=A_COMPANY_WITH_THIS_NAME_ALREADY_EXISTS
            )

    def validate_company_email(self, email: str):
        """
            Validate company email for uniqueness.
        """
        existing_company = (
            self.db.query(Company)
            .filter(func.lower(Company.email) == email.lower())
            .first()
        )

        if existing_company:
            raise HTTPException(
                status_code=400,
                detail=A_COMPANY_WITH_THIS_EMAIL_ALREADY_EXISTS
            )

    def create_company(self, request: CompanyRequest) -> CompanyResponse:
        """
            Create a new company in the database.
        """
        self.validate_company_name(request.name)
        self.validate_company_email(request.email)

        company = Company(
            name=request.name,
            contact_person_name=request.contact_person_name,
            email=request.email,
            address=request.address,
            phone_number=request.phone_number
        )

        self.db.add(company)
        self.db.commit()
        
        return CompanyResponse(
            message=COMPANY_CREATED_SUCCESSFULLY
        )
    
    def validate_company_exists(self, company: Company):
        """
            Validate if company exists.
        """        
        if not company:
            raise HTTPException(
                status_code=404,
                detail=COMPANY_NOT_FOUND
            )

    def get_company_data_by_id(self, id: int) -> Company:
        """
            Get company data by ID.
        """
        return self.db.query(Company).filter(Company.id == id).first()
    
    def get_company_by_id(self, id: int) -> GetCompanyResponse:
        """
            Get a company by ID.
        """
        company = self.get_company_data_by_id(id)
        self.validate_company_exists(company)

        return mapper.to(GetCompanyResponse).map(company)
    
    def validate_update_name(self, existing_name: str, new_name: str):
        """
            Validate company name for uniqueness during update.
        """
        if existing_name.lower() != new_name.lower():
            self.validate_company_name(new_name)
    
    def validate_update_email(self, existing_email: str, new_email: str):
        """
            Validate company email for uniqueness during update.
        """
        if existing_email.lower() != new_email.lower():
            self.validate_company_email(new_email)
    
    def update_company_by_id(self, id: int, request: CompanyRequest) -> CompanyResponse:
        """
            Update company data by ID.
        """
        company = self.get_company_data_by_id(id)
        self.validate_company_exists(company)
        self.validate_update_name(company.name, request.name)
        self.validate_update_email(company.email, request.email)

        company.name = request.name
        company.contact_person_name = request.contact_person_name
        company.email = request.email
        company.address = request.address
        company.phone_number = request.phone_number

        self.db.commit()

        return CompanyResponse(message=COMPANY_UPDATED_SUCCESSFULLY)
    
    def delete_company_by_id(self, id: int) -> CompanyResponse:
        """
            Delete company by ID.
        """
        company = self.get_company_data_by_id(id)
        self.validate_company_exists(company)

        self.db.delete(company)
        self.db.commit()

        return CompanyResponse(message=COMPANY_DELETED_SUCCESSFULLY)