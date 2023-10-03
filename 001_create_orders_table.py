from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'orders',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(100), nullable=False),
        sa.Column('route', sa.String(100), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(100), nullable=False),
        sa.Column('date_added', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('order_id')
    )

def downgrade():
    op.drop_table('orders')
