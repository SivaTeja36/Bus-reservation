from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e773eaaf2341'
down_revision = '5ae22a6d1eed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the buses table
    op.create_table('buses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('branch_id', sa.Integer(), nullable=False),
    sa.Column('bus_number', sa.String(length=10), nullable=False),
    sa.Column('bus_type', sa.String(length=10), nullable=False),
    sa.Column('total_seats', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # Drop the buses table
    op.drop_table('buses')
    # ### end Alembic commands ###
