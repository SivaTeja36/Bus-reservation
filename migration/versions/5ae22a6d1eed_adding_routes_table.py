from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '5ae22a6d1eed'
down_revision = '6da0a94fad8f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create the routes table
    op.create_table('routes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stops', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('source',  sa.String(length=50), nullable=False),
        sa.Column('destination', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Realistic route data
    routes_data = [
        # Telangana
        {'id': 1, 'stops': ["Hyderabad", "Shadnagar", "Mahbubnagar", "Kurnool"], 'source': "Hyderabad", 'destination': "Kurnool", 'created_at': datetime.utcnow()},
        {'id': 2, 'stops': ["Hyderabad", "Siddipet", "Karimnagar", "Ramagundam"], 'source': "Hyderabad", 'destination': "Ramagundam", 'created_at': datetime.utcnow()},

        # Andhra Pradesh
        {'id': 3, 'stops': ["Vijayawada", "Guntur", "Ongole", "Nellore"], 'source': "Vijayawada", 'destination': "Nellore", 'created_at': datetime.utcnow()},
        {'id': 4, 'stops': ["Tirupati", "Rajampet", "Kadapa", "Rayachoti"], 'source': "Tirupati", 'destination': "Rayachoti", 'created_at': datetime.utcnow()},

        # Chennai
        {'id': 5, 'stops': ["Chennai", "Vellore", "Krishnagiri", "Hosur"], 'source': "Chennai", 'destination': "Hosur", 'created_at': datetime.utcnow()},
        {'id': 6, 'stops': ["Chennai", "Pondicherry", "Cuddalore", "Villupuram"], 'source': "Chennai", 'destination': "Villupuram", 'created_at': datetime.utcnow()},

        # Bangalore
        {'id': 7, 'stops': ["Bangalore", "Tumkur", "Chitradurga", "Davangere"], 'source': "Bangalore", 'destination': "Davangere", 'created_at': datetime.utcnow()},
        {'id': 8, 'stops': ["Bangalore", "Mandya", "Mysore"], 'source': "Bangalore", 'destination': "Mysore", 'created_at': datetime.utcnow()},

        # Inter-State
        {'id': 9, 'stops': ["Hyderabad", "Anantapur", "Bangalore"], 'source': "Hyderabad", 'destination': "Bangalore", 'created_at': datetime.utcnow()},
        {'id': 10, 'stops': ["Vijayawada", "Tirupati", "Chennai"], 'source': "Vijayawada", 'destination': "Chennai", 'created_at': datetime.utcnow()},
        {'id': 11, 'stops': ["Chennai", "Hosur", "Bangalore"], 'source': "Chennai", 'destination': "Bangalore", 'created_at': datetime.utcnow()},
        {'id': 12, 'stops': ["Bangalore", "Mysore", "Wayanad"], 'source': "Bangalore", 'destination': "Wayanad", 'created_at': datetime.utcnow()},

        # Additional Routes
        {'id': 13, 'stops': ["Hyderabad", "Warangal"], 'source': "Hyderabad", 'destination': "Warangal", 'created_at': datetime.utcnow()},
        {'id': 14, 'stops': ["Tirupati", "Chittoor"], 'source': "Tirupati", 'destination': "Chittoor", 'created_at': datetime.utcnow()},
        {'id': 15, 'stops': ["Vijayawada", "Rajahmundry"], 'source': "Vijayawada", 'destination': "Rajahmundry", 'created_at': datetime.utcnow()},

        # 🆕 Tirupati to Bangalore (via Rajampet, Kadapa, Rayachoti, Kurnool)
        {'id': 16, 'stops': ["Tirupati", "Rajampet", "Kadapa", "Rayachoti", "Kurnool", "Bangalore"], 'source': "Tirupati", 'destination': "Bangalore", 'created_at': datetime.utcnow()},

        # 🆕 Hyderabad to Chennai (via Kurnool, Kadapa, Tirupati)
        {'id': 17, 'stops': ["Hyderabad", "Kurnool", "Kadapa", "Tirupati", "Chennai"], 'source': "Hyderabad", 'destination': "Chennai", 'created_at': datetime.utcnow()},

        # 🆕 Vijayawada to Bangalore (via Guntur, Kadapa, Anantapur)
        {'id': 18, 'stops': ["Vijayawada", "Guntur", "Kadapa", "Anantapur", "Bangalore"], 'source': "Vijayawada", 'destination': "Bangalore", 'created_at': datetime.utcnow()},
    ]

    # Insert route data
    for route in routes_data:
        import json
        op.execute(
            sa.text(
                """
                INSERT INTO routes (id, stops, source, destination, created_at)
                VALUES (:id, :stops, :source, :destination, :created_at)
                """
            ).bindparams(
                id=route['id'],
                stops=json.dumps(route['stops']),
                source=route['source'],
                destination=route['destination'],
                created_at=route['created_at']
            )
        )


def downgrade() -> None:
    op.drop_table('routes')
    # ### end Alembic commands ###