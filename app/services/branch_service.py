from dataclasses import dataclass
import traceback
import argparse
from automapper import mapper

from fastapi import Depends
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
    BranchResponse
)
from app.utils.constants import (
    BRANCH_CREATED_SUCCESSFULLY, 
    DB_NOT_UPTODATE
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

    def create_branch(self, request: BranchRequest) -> Branch:
        schema = get_randome_str()

        branch = Branch(
            name=request.name,
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

    def get_branch(self, id: int) -> Branch:
        branch = self.db.query(Branch).filter(Branch.id == id).first() 
        return mapper.to(BranchResponse).map(branch)
