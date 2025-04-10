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
from app.entities.route import Route
from app.entities.schedule import Schedule
from app.models.bus_models import (
    BusRequest,
    BusResponse,
    BusScheduleRequest,
    GetBusResponse,
    GetBusScheduleResponse,
    GetRouteResponse
)
from app.models.company_models import GetCompanyResponse
from app.utils.constants import (
    A_BUS_WITH_THIS_NUMBER_ALREADY_EXISTS,
    BUS_CREATED_SUCCESSFULLY,
    BUS_DELETED_SUCCESSFULLY,
    BUS_NOT_FOUND,
    BUS_SCHEDULE_CREATED_SUCCESSFULLY,
    BUS_SCHEDULE_DELETED_SUCCESSFULLY,
    BUS_SCHEDULE_UPDATED_SUCCESSFULLY,
    BUS_UPDATED_SUCCESSFULLY,
    COMPANY_NOT_FOUND,
    SCHEDULE_NOT_FOUND
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
            bus_response = GetBusResponse(
                id=bus.id,
                company_id=bus.company_id,
                bus_number=bus.bus_number,
                bus_type=bus.bus_type,
                total_seats=bus.total_seats,
                created_at=bus.created_at,
                is_active=bus.is_active,
                company_data=mapper.to(GetCompanyResponse).map(company_map.get(bus.company_id))
            )
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
    
    def get_all_bus_schedules(self) -> list[GetBusScheduleResponse]:
        """
            Get all bus schedules from the database in ascending order of departure time.
        """
        schedules = self.db.query(Schedule).order_by(Schedule.departure_time.asc()).all()
        bus_ids = {schedule.bus_id for schedule in schedules}
        buses = self.db.query(Bus).filter(Bus.id.in_(bus_ids)).all()
        bus_map = {bus.id: bus for bus in buses}

        company_ids = {bus.company_id for bus in buses}
        companies = self.db.query(Company).filter(Company.id.in_(company_ids)).all()
        company_map = {company.id: company for company in companies}

        route_ids = {schedule.route_id for schedule in schedules}
        routes = self.db.query(Route).filter(Route.id.in_(route_ids)).all()
        route_map = {route.id: route for route in routes}

        schedule_responses = []
        for schedule in schedules:
            schedule_response = mapper.to(GetBusScheduleResponse).map(schedule)
            bus = bus_map.get(schedule.bus_id)
            schedule_response.bus_data = mapper.to(GetBusResponse).map(bus)

            if bus:
                schedule_response.bus_data.company_data = mapper.to(GetCompanyResponse).map(company_map.get(bus.company_id))

            route = route_map.get(schedule.route_id)
            if route:
                schedule_response.route_data = mapper.to(GetRouteResponse).map(route)

            schedule_responses.append(schedule_response)
        
        return schedule_responses
    
    def get_schedule_data_by_id(self, id: int):
        return self.db.query(Schedule).filter(Schedule.id == id).first()
    
    def validate_schedule_exists(self, schedule: Schedule):
        if not schedule:
            raise HTTPException(
                status_code=404,
                detail=SCHEDULE_NOT_FOUND
            )
    
    def update_bus_schedule_by_id(self, id: int, request: BusScheduleRequest) -> BusResponse:
        """
            Update an existing bus schedule by ID.
        """
        schedule = self.get_schedule_data_by_id(id)
        self.validate_schedule_exists(schedule)
        
        bus = self.get_bus_data_by_id(request.bus_id)
        self.validate_bus_exists(bus)

        schedule.bus_id = request.bus_id
        schedule.route_id = request.route_id
        schedule.departure_time = request.departure_time
        schedule.arrival_time = request.arrival_time
        schedule.updated_at = func.now()

        self.db.commit()

        return BusResponse(message=BUS_SCHEDULE_UPDATED_SUCCESSFULLY)

    def delete_bus_schedule_by_id(self, id: int) -> BusResponse:
        """
            Delete a bus schedule by ID.
        """
        schedule = self.get_schedule_data_by_id(id)
        self.validate_schedule_exists(schedule)
        
        self.db.delete(schedule)
        self.db.commit()

        return BusResponse(message=BUS_SCHEDULE_DELETED_SUCCESSFULLY)