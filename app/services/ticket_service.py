from dataclasses import dataclass
from datetime import datetime

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
from app.entities.ticket import Ticket
from app.models.bus_models import GetBusResponse
from app.models.company_models import GetCompanyResponse
from app.models.ticket_models import (
    TicketRequest,
    TicketResponse,
    GetTicketResponse
)
from app.utils.constants import (
    BUS_NOT_FOUND,
    TICKET_CREATED_SUCCESSFULLY,
    TICKET_UPDATED_SUCCESSFULLY,
    TICKET_DELETED_SUCCESSFULLY,
    TICKET_NOT_FOUND
)



@dataclass
class TicketService:
    db: Session = Depends(get_tenant_db)

    def validate_bus_exists_by_id(self, bus_id: int):
        """
            Validate if a bus exists by its ID.
        """
        bus = self.db.query(Bus).filter(Bus.id == bus_id).first()

        if not bus:
            raise HTTPException(
                status_code=404,
                detail=BUS_NOT_FOUND
            )
        
    def generate_ticket_number(self, bus_id: int) -> str:
        """
            Generate a unique ticket number based on the company name, year, and ticket count.
        """
        company_name = (
            self.db.query(Company.name)
            .join(Bus, Bus.company_id == Company.id)
            .filter(Bus.id == bus_id)
            .first()
        )
        company_name = company_name[0][:3].upper()  
        year = datetime.now().year
        ticket_count = self.db.query(func.count(Ticket.id)).scalar() + 1
        return f"{company_name}{year}{ticket_count:07d}"    

    def create_ticket(self, request: TicketRequest) -> TicketResponse:
        """
            Create a new ticket in the database.
        """
        self.validate_bus_exists_by_id(request.bus_id)
        ticket_number = self.generate_ticket_number(request.bus_id)

        ticket = Ticket(
            ticket_number=ticket_number,
            bus_id=request.bus_id,
            seat_number=request.seat_number,
            passenger_name=request.passenger_name,
            passenger_contact=request.passenger_contact,
            passenger_email=request.passenger_email,
            status=request.status
        )

        self.db.add(ticket)
        self.db.commit()

        return TicketResponse(
            message=TICKET_CREATED_SUCCESSFULLY
        )

    def get_all_tickets(self) -> list[GetTicketResponse]:
        """
            Get all tickets from the database with bus and company data.
            Optimized to reduce the number of queries.
        """
        tickets = self.db.query(Ticket).all()
        bus_ids = {ticket.bus_id for ticket in tickets}
        buses = self.db.query(Bus).filter(Bus.id.in_(bus_ids)).all()
        bus_map = {bus.id: bus for bus in buses}

        company_ids = {bus.company_id for bus in buses}
        companies = self.db.query(Company).filter(Company.id.in_(company_ids)).all()
        company_map = {company.id: company for company in companies}

        responses = []
        for ticket in tickets:
            bus = bus_map.get(ticket.bus_id)
            
            ticket_response = GetTicketResponse(
                id=ticket.id,
                seat_number=ticket.seat_number,
                passenger_name=ticket.passenger_name,
                passenger_contact=ticket.passenger_contact,
                passenger_email=ticket.passenger_email,
                status=ticket.status,
                created_at=ticket.created_at,
                updated_at=ticket.updated_at,
                bus_data=GetBusResponse(
                    id=bus.id,
                    company_id=bus.company_id,
                    bus_number=bus.bus_number,
                    bus_type=bus.bus_type,
                    total_seats=bus.total_seats,
                    created_at=bus.created_at,
                    is_active=bus.is_active,
                    company_data=mapper.to(GetCompanyResponse).map(company_map.get(bus.company_id))
                )
            )
            responses.append(ticket_response)

        return responses
    
    def validate_ticket_exists(self, ticket: Ticket):
        """
            Validate if ticket exists.
        """        
        if not ticket:
            raise HTTPException(
                status_code=404,
                detail=TICKET_NOT_FOUND
            )

    def get_ticket_data_by_id(self, id: int) -> Ticket:
        """
            Get ticket data by ID.
        """
        return self.db.query(Ticket).filter(Ticket.id == id).first()
    
    def get_ticket_by_id(self, id: int) -> GetTicketResponse:
        """
            Get a ticket by ID with bus and company data.
        """
        ticket = self.get_ticket_data_by_id(id)
        self.validate_ticket_exists(ticket)

        bus = self.db.query(Bus).filter(Bus.id == ticket.bus_id).first()
        company = self.db.query(Company).filter(Company.id == bus.company_id).first()

        ticket_response = GetTicketResponse(
            id=ticket.id, 
            seat_number=ticket.seat_number,
            passenger_name=ticket.passenger_name,
            passenger_contact=ticket.passenger_contact, 
            passenger_email=ticket.passenger_email, 
            status=ticket.status, 
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,  
            bus_data=GetBusResponse(
                id=bus.id,
                company_id=bus.company_id,
                bus_number=bus.bus_number,
                bus_type=bus.bus_type,
                total_seats=bus.total_seats,
                created_at=bus.created_at,
                is_active=bus.is_active,
                company_data=mapper.to(GetCompanyResponse).map(company)
            )

        )

        return ticket_response
    
    def update_ticket_by_id(self, id: int, request: TicketRequest) -> TicketResponse:
        """
            Update ticket data by ID.
        """
        ticket = self.get_ticket_data_by_id(id)
        self.validate_ticket_exists(ticket)

        ticket.seat_number = request.seat_number
        ticket.passenger_name = request.passenger_name
        ticket.passenger_contact = request.passenger_contact
        ticket.passenger_email = request.passenger_email
        ticket.status = request.status
        ticket.updated_at = func.now()

        self.db.commit()

        return TicketResponse(message=TICKET_UPDATED_SUCCESSFULLY)
    
    def delete_ticket_by_id(self, id: int) -> TicketResponse:
        """
            Delete ticket by ID.
        """
        ticket = self.get_ticket_data_by_id(id)
        self.validate_ticket_exists(ticket)

        self.db.delete(ticket)
        self.db.commit()

        return TicketResponse(message=TICKET_DELETED_SUCCESSFULLY)