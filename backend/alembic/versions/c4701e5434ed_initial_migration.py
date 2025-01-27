"""Initial migration

Revision ID: c4701e5434ed
Revises: 
Create Date: 2024-12-27 13:27:15.461611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4701e5434ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grupe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('naziv', sa.String(), nullable=True),
    sa.Column('opis', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('klijenti',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ime', sa.String(), nullable=False),
    sa.Column('prezime', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('datum_rodjenja', sa.Date(), nullable=False),
    sa.Column('broj_telefona', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('fotografija', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('broj_telefona'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('psiholozi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ime', sa.String(), nullable=False),
    sa.Column('prezime', sa.String(), nullable=False),
    sa.Column('datum_rodjenja', sa.Date(), nullable=False),
    sa.Column('broj_telefona', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('fotografija', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tipovi_termina',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('naziv', sa.String(), nullable=False),
    sa.Column('opis', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('naziv')
    )
    op.create_table('klijent_grupa',
    sa.Column('klijent_id', sa.Integer(), nullable=False),
    sa.Column('grupa_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grupa_id'], ['grupe.id'], ),
    sa.ForeignKeyConstraint(['klijent_id'], ['klijenti.id'], ),
    sa.PrimaryKeyConstraint('klijent_id', 'grupa_id')
    )
    op.create_table('termini',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('zakazan', 'blokiran', name='status_enum'), nullable=False),
    sa.Column('datum_vrijeme', sa.DateTime(), nullable=False),
    sa.Column('nacin_izvodjenja', sa.Enum('uzivo', 'online', name='nacin_izvodjenja_status'), nullable=True),
    sa.Column('napomena', sa.String(), nullable=True),
    sa.Column('psiholog_id', sa.Integer(), nullable=False),
    sa.Column('klijent_id', sa.Integer(), nullable=True),
    sa.Column('grupa_id', sa.Integer(), nullable=True),
    sa.Column('tip_termina_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grupa_id'], ['grupe.id'], ),
    sa.ForeignKeyConstraint(['klijent_id'], ['klijenti.id'], ),
    sa.ForeignKeyConstraint(['psiholog_id'], ['psiholozi.id'], ),
    sa.ForeignKeyConstraint(['tip_termina_id'], ['tipovi_termina.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('datum_vrijeme')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('termini')
    op.drop_table('klijent_grupa')
    op.drop_table('tipovi_termina')
    op.drop_table('psiholozi')
    op.drop_table('klijenti')
    op.drop_table('grupe')
    # ### end Alembic commands ###
