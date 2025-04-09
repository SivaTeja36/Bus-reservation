from dataclasses import dataclass
import traceback
import argparse
from typing import List
from automapper import mapper

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy as sa
from alembic import (
    command, 
    script
)
from alembic.config import Config
from alembic.migration import MigrationContext

from app.connectors.database_connector import (
    get_master_database, 
    get_master_db
)
from app.entities.branch import Branch
from app.models.branch_models import (
    BranchRequest, 
    BranchResponse,
    GetBranchResponse
)
from app.utils.constants import (
    BRANCH_CREATED_SUCCESSFULLY,
    BRANCH_NOT_FOUND,
    BRANCH_UPDATED_SUCCESSFULLY,
    CITY_NAME_ALREADY_EXISTS, 
    DB_NOT_UPTODATE,
    DOMAIN_NAME_ALREADY_EXISTS
)
from app.utils.utils import (
    get_project_root, 
    get_randome_str
)


@dataclass
class BranchService:
    db: Session = Depends(get_master_db)

    @staticmethod
    def __get_current_head(db: Session):
        connection = db.connection()
        context = MigrationContext.configure(connection)
        current_head = context.get_current_revision()

        if current_head == None:
            raise Exception(DB_NOT_UPTODATE)
        return current_head

    @staticmethod
    def __upgrade(schema: str, current_head: str):
        alembic_config = Config(get_project_root().joinpath("alembic.ini"))
        alembic_script = script.ScriptDirectory.from_config(alembic_config)
        config_head = alembic_script.get_current_head()

        if current_head != config_head:
            raise RuntimeError(
                "Database is not up-to-date. Execute migrations before adding new tenants."
            )
        
        # If it is required to pass -x parameters to alembic
        x_arg = "".join(["tenant=", schema])  # "dry_run=" + "True"
        alembic_config.cmd_opts = argparse.Namespace()  # arguments stub
        
        if not hasattr(alembic_config.cmd_opts, "x"):
            if x_arg is not None:
                setattr(alembic_config.cmd_opts, "x", [x_arg])
            else:
                setattr(alembic_config.cmd_opts, "x", None)

        command.upgrade(alembic_config, "head")

    @staticmethod
    def upgrade_all():
        db = get_master_database()

        try:
            current_head = BranchService.__get_current_head(db)

            for branch in db.query(Branch).all():
                BranchService.__upgrade(branch.schema, current_head)

            db.commit()
            db.flush()
        except:
            db.rollback()
            traceback.print_exc()
        finally:
            db.close()

    def validate_branch_name(self, city_name: str) -> bool:
        existing_branch = (
            self.db.query(Branch)
            .filter(sa.func.lower(Branch.city) == city_name.lower())
            .first()
        )

        if existing_branch:
            raise HTTPException(
                status_code=400, 
                detail=CITY_NAME_ALREADY_EXISTS
            )
    
    def validate_domain_name(self, domain_name: str) -> bool:
        existing_domain = (
            self.db.query(Branch)
            .filter(sa.func.lower(Branch.domain_name) == domain_name.lower())
            .first()
        )

        if existing_domain:
            raise HTTPException(
                status_code=400, 
                detail=DOMAIN_NAME_ALREADY_EXISTS
            )

    def create_branch(self, request: BranchRequest) -> Branch:
        self.validate_branch_name(request.city)
        self.validate_domain_name(request.domain_name)

        schema = get_randome_str()

        branch = Branch(
            city=request.city,
            domain_name=request.domain_name,
            schema=schema,
        )
    
        self.db.execute(sa.schema.CreateSchema(schema, True))
        self.db.add(branch)
        self.db.commit()

        current_head = BranchService.__get_current_head(self.db)
        BranchService.__upgrade(schema, current_head)

        return BranchResponse(message=BRANCH_CREATED_SUCCESSFULLY)
    
    def get_all_branches(self) -> List[GetBranchResponse]:
        branches = self.db.query(Branch).all() 
        return [mapper.to(GetBranchResponse).map(branch) for branch in branches]
    
    def get_branch_data_by_id(self, id: int) -> Branch:
        branch = self.db.query(Branch).filter(Branch.id == id).first() 
        return branch
    
    def validate_branch_exists(self, branch: Branch):
        if not branch:
            raise HTTPException(
                status_code=404, 
                detail=BRANCH_NOT_FOUND
            )
    
    def get_branch_by_id(self, id: int) -> Branch:
        branch = self.get_branch_data_by_id(id) 
        self.validate_branch_exists(branch)
        return mapper.to(GetBranchResponse).map(branch)
    
    def validate_branch_name_update(self, existing_branch_city: str, new_city_name: str) -> bool:
        if existing_branch_city.lower() != new_city_name.lower():
            self.validate_branch_name(new_city_name)

    def validate_domain_name_update(self, existing_branch_domain: str, new_domain_name: str) -> bool:
        if existing_branch_domain.lower() != new_domain_name.lower():
            self.validate_domain_name(new_domain_name)        
    
    
    def update_branch_by_id(self, id: int, request: BranchRequest) -> Branch:
        branch = self.get_branch_data_by_id(id) 
        self.validate_branch_exists(branch)
        self.validate_branch_name_update(branch.city, request.city)
        self.validate_domain_name_update(branch.domain_name, request.domain_name)

        branch.city = request.city
        branch.domain_name = request.domain_name
        branch.logo_path = request.logo
        branch.updated_at = sa.func.now()
    
        self.db.commit()

        return BranchResponse(message=BRANCH_UPDATED_SUCCESSFULLY)