"""Remove deprecated value field from assets table

Revision ID: remove_value_field_assets
Revises: 2a5ec4710cc8
Create Date: 2024-12-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'remove_value_field_assets'
down_revision = '2a5ec4710cc8'
branch_labels = None
depends_on = None


def upgrade():
    """Remove the deprecated value field from assets table"""
    # For SQLite, we need to recreate the table
    connection = op.get_bind()
    
    if connection.engine.name == 'sqlite':
        # Create new table without value column
        op.execute("""
            CREATE TABLE assets_new (
                id INTEGER NOT NULL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                asset_type VARCHAR(50) NOT NULL,
                acquisition_date DATE,
                details JSON,
                family_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(family_id) REFERENCES family (id)
            )
        """)
        
        # Copy data from old table to new table
        op.execute("""
            INSERT INTO assets_new (id, name, asset_type, acquisition_date, details, family_id, created_at)
            SELECT id, name, asset_type, acquisition_date, details, family_id, created_at
            FROM assets
        """)
        
        # Drop old table
        op.execute("DROP TABLE assets")
        
        # Rename new table
        op.execute("ALTER TABLE assets_new RENAME TO assets")
    else:
        # For other databases, try to drop the column
        try:
            op.drop_column('assets', 'value')
        except Exception:
            # If column doesn't exist, that's fine
            pass


def downgrade():
    """Add back the value field for rollback purposes"""
    # Add the value column back (nullable for backward compatibility)
    op.add_column('assets', sa.Column('value', sa.Float(), nullable=True))
