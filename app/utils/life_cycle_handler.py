from fastapi import FastAPI

from app.services.branch_service import BranchService


def __on_app_started():
    BranchService.upgrade_all()
   
   
def __on_app_finished():
    pass


def setup_event_handlers(app: FastAPI):
    app.add_event_handler("startup", __on_app_started)
    app.add_event_handler("shutdown", __on_app_finished)
