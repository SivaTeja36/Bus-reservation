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
from app.entities.bus import Bus
from app.entities.company import Company
from app.entities.schedule import Schedule
from app.models.bus_models import (
    BusRequest,
    BusResponse,
    BusScheduleRequest,
    GetBusResponse
)
from app.models.company_models import GetCompanyResponse
from app.utils.constants import (
    A_BUS_WITH_THIS_NUMBER_ALREADY_EXISTS,
    BUS_CREATED_SUCCESSFULLY,
    BUS_DELETED_SUCCESSFULLY,
    BUS_NOT_FOUND,
    BUS_SCHEDULE_CREATED_SUCCESSFULLY,
    BUS_UPDATED_SUCCESSFULLY,
    COMPANY_NOT_FOUND
)



@dataclass
class BusService:
    db: Session = Depends(get_tenant_db)

    def get_company_data_by_id(self, id: int) -> Company:
        """
            Get company data by ID.
        """
        return self.db.query(Company).filter(Company.id == id).first()
    
    def validate_bus_number(self, bus_number: str):
        """
            Validate bus name for uniqueness.
        """
        existing_bus_number = (
            self.db.query(Bus)
            .filter(func.lower(Bus.bus_number) == bus_number.lower())
            .first()
        )

        if existing_bus_number:
            raise HTTPException(
                status_code=400,
                detail=A_BUS_WITH_THIS_NUMBER_ALREADY_EXISTS
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

    def create_bus(self, request: BusRequest) -> BusResponse:
        """
            Create a new bus in the database.
        """
        self.validate_bus_number(request.bus_number)
        company = self.get_company_data_by_id(request.company_id)
        self.validate_company_exists(company)

        bus = Bus(
            bus_number=request.bus_number,
            bus_type=request.bus_type,
            total_seats=request.total_seats,
            company_id=request.company_id
        )

        self.db.add(bus)
        self.db.commit()
        
        return BusResponse(
            message=BUS_CREATED_SUCCESSFULLY
        )
    
    def get_all_buses(self) -> list[GetBusResponse]:
        """
            Get all buses from the database along with company data.
        """
        buses = self.db.query(Bus).all()
        company_ids = {bus.company_id for bus in buses}
        companies = self.db.query(Company).filter(Company.id.in_(company_ids)).all()
        company_map = {company.id: company for company in companies}

        bus_responses = []
        for bus in buses:
            bus_response = mapper.to(GetBusResponse).map(bus)
            bus_response.company_data = mapper.to(GetCompanyResponse).map(company_map.get(bus.company_id))
            bus_responses.append(bus_response)
            
        return bus_responses
    
    def validate_bus_exists(self, bus: Bus):
        """
            Validate if company exists.
        """        
        if not bus:
            raise HTTPException(
                status_code=404,
                detail=BUS_NOT_FOUND
            )

    def get_bus_data_by_id(self, id: int) -> Bus:
        """
            Get company data by ID.
        """
        return self.db.query(Bus).filter(Bus.id == id).first()
    
    def get_bus_by_id(self, id: int) -> GetBusResponse:
        """
            Get a bus by ID along with company data.
        """
        bus = self.get_bus_data_by_id(id)
        self.validate_bus_exists(bus)

        company = self.db.query(Company).filter(Company.id == bus.company_id).first()

        bus_response = mapper.to(GetBusResponse).map(bus)
        bus_response.company_data = mapper.to(GetCompanyResponse).map(company)

        return bus_response
    
    def validate_update_bus_number(self, existing_bus_number: str, new_bus_number: str):
        """
            Validate bus number for uniqueness during update.
        """
        if existing_bus_number.lower() != new_bus_number.lower():
            self.validate_bus_number(new_bus_number)
    
    def update_bus_by_id(self, id: int, request: BusRequest) -> BusResponse:
        """
            Update bus data by ID.
        """
        bus = self.get_bus_data_by_id(id)
        self.validate_bus_exists(bus)
        company = self.get_company_data_by_id(request.company_id)
        self.validate_company_exists(company)
        self.validate_update_bus_number(bus.bus_number, request.bus_number)

        bus.bus_number = request.bus_number
        bus.bus_type = request.bus_type
        bus.total_seats = request.total_seats
        bus.company_id = request.company_id
        bus.updated_at = func.now()

        self.db.commit()

        return BusResponse(message=BUS_UPDATED_SUCCESSFULLY)
    
    def delete_bus_by_id(self, id: int) -> BusResponse:
        """
            Delete bus by ID.
        """
        bus = self.get_bus_data_by_id(id)
        self.validate_bus_exists(bus)

        self.db.delete(bus)
        self.db.commit()

        return BusResponse(message=BUS_DELETED_SUCCESSFULLY)
    
    def create_bus_schedule(self, request: BusScheduleRequest) -> BusResponse:
        """
            Create a new bus schedule.
        """
        bus = self.get_bus_data_by_id(request.bus_id)
        self.validate_bus_exists(bus)

        schedule = Schedule(
            bus_id=request.bus_id,
            route_id=request.route_id,
            departure_time=request.departure_time,
            arrival_time=request.arrival_time
        )
        
        self.db.add(schedule)
        self.db.commit()

        return BusResponse(message=BUS_SCHEDULE_CREATED_SUCCESSFULLY)