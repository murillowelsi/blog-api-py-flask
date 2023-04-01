"""adding sample users

Revision ID: 3614ab2f61f2
Revises: ba4632c7a715
Create Date: 2023-04-01 09:58:33.728958

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.database import db
from app.models.post_model import Post

# revision identifiers, used by Alembic.
revision = '3614ab2f61f2'
down_revision = 'ba4632c7a715'
branch_labels = None
depends_on = None


def upgrade():
    post1 = Post(title='Post de Teste 1', body='Este é o post de teste 1', created_at=datetime.utcnow())
    post2 = Post(title='Post de Teste 2', body='Este é o post de teste 2', created_at=datetime.utcnow())
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='posts_pkey')
    )
    # ### end Alembic commands ###