"""init3

Revision ID: 7cff272eadbd
Revises: bf05da1a0279
Create Date: 2023-12-04 03:39:11.779851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7cff272eadbd'
down_revision: Union[str, None] = 'bf05da1a0279'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.user_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_id'), 'chat', ['id'], unique=True)
    op.create_table('message',
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('sender_type', sa.String(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=True)
    op.drop_index('ix_chat_message_id', table_name='chat_message')
    op.drop_table('chat_message')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_message',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('doctor_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('patient_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.user_id'], name='chat_message_doctor_id_fkey'),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.user_id'], name='chat_message_patient_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='chat_message_pkey')
    )
    op.create_index('ix_chat_message_id', 'chat_message', ['id'], unique=False)
    op.drop_index(op.f('ix_message_id'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_chat_id'), table_name='chat')
    op.drop_table('chat')
    # ### end Alembic commands ###