from app.connectors.database_connector import Base
from .user import User
from .branch import Branch
from .route import Route
from .company import Company
from .bus import Bus
from .schedule import Schedule
from .ticket import Ticket

# import your application specific entities here for creating migration scripts automatically (alembic)