from enum import StrEnum

class Roles(StrEnum):
    SuperAdmin = "Super Admin"
    Admin = "Admin"


class BusTypeEnum(StrEnum):
    AC = "AC"
    NON_AC = "NON_AC"


class TicketStatusEnum(StrEnum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"    