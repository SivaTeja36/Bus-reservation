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
from app.entities.schedule import Schedule
from app.models.bus_models import (
    BusRequest,
    BusResponse,
    BusScheduleRequest,
    GetBusResponse
)
from app.utils.constants import (
    A_BUS_WITH_THIS_NUMBER_ALREADY_EXISTS,
    BUS_CREATED_SUCCESSFULLY,
    BUS_DELETED_SUCCESSFULLY,
    BUS_NOT_FOUND,
    BUS_SCHEDULE_CREATED_SUCCESSFULLY,
    BUS_UPDATED_SUCCESSFULLY
)



@dataclass
class BusService:
    db: Session = Depends(get_tenant_db)
    
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

    def create_bus(self, request: BusRequest) -> BusResponse:
        """
            Create a new bus in the database.
        """
        self.validate_bus_number(request.bus_number)

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
            Get all buses from the database.
        """
        buses = self.db.query(Bus).all()
        return [mapper.to(GetBusResponse).map(bus) for bus in buses]
    
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
            Get a company by ID.
        """
        bus = self.get_bus_data_by_id(id)
        self.validate_bus_exists(bus)

        return mapper.to(GetBusResponse).map(bus)
    
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