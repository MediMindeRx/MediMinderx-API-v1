"""empty message

Revision ID: 67fad8450277
Revises: ab191bdb11f5
Create Date: 2020-10-27 14:02:58.819499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67fad8450277'
down_revision = 'ab191bdb11f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_name', sa.String(length=80), nullable=False),
    sa.Column('longitude', sa.String(length=50), nullable=False),
    sa.Column('latitude', sa.String(length=50), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('location_name')
    )
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schedule_name', sa.String(length=80), nullable=False),
    sa.Column('unix_time', sa.Integer(), nullable=False),
    sa.Column('days', sa.String(length=250), nullable=False),
    sa.Column('times', sa.String(length=250), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('schedule_name')
    )
    op.add_column('reminders', sa.Column('location_id', sa.Integer(), nullable=True))
    op.add_column('reminders', sa.Column('schedule_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reminders', 'locations', ['location_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'reminders', 'schedules', ['schedule_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reminders', type_='foreignkey')
    op.drop_constraint(None, 'reminders', type_='foreignkey')
    op.drop_column('reminders', 'schedule_id')
    op.drop_column('reminders', 'location_id')
    op.drop_table('schedules')
    op.drop_table('locations')
    # ### end Alembic commands ###
