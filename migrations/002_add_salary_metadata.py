#!/usr/bin/env python3
"""
Migration 002: Add salary currency and unit fields to jobs and rejected_jobs tables.

This migration adds:
1. salary_currency field to store currency information (USD, CAD, EUR, GBP, etc.)
2. salary_unit field to store unit information (annual, hourly, etc.)
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from job_ingestion.utils.config import get_settings
from sqlalchemy import Column, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


def upgrade(engine: Engine) -> None:
    """Apply the migration - add salary_currency and salary_unit columns."""
    print("Adding salary metadata columns...")

    # New columns to add
    new_columns = [
        Column("salary_currency", String(10), nullable=True),  # USD, CAD, EUR, GBP, etc.
        Column("salary_unit", String(20), nullable=True),  # annual, hourly, etc.
    ]

    # Tables to update
    tables = ["jobs", "rejected_jobs"]

    with engine.connect() as conn:
        for table_name in tables:
            print(f"  Updating {table_name} table...")

            for column in new_columns:
                try:
                    # Check if column already exists
                    if engine.dialect.name == "sqlite":
                        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
                        existing_columns = [row[1] for row in result.fetchall()]
                    else:  # PostgreSQL
                        result = conn.execute(
                            text(
                                "SELECT column_name FROM information_schema.columns "
                                f"WHERE table_name = '{table_name}'"
                            )
                        )
                        existing_columns = [row[0] for row in result.fetchall()]

                    if column.name not in existing_columns:
                        conn.execute(
                            text(f"ALTER TABLE {table_name} ADD COLUMN {column.name} {column.type}")
                        )
                        print(f"    Added column: {column.name}")
                    else:
                        print(f"    Column {column.name} already exists, skipping")

                except Exception as e:
                    print(f"    Warning: Could not add column {column.name} to {table_name}: {e}")

        conn.commit()

    print("Migration 002 completed successfully!")


def downgrade(engine: Engine) -> None:
    """Rollback the migration - remove salary metadata columns."""
    print("Rolling back migration 002...")

    # Note: Removing columns from SQLite is complex and requires recreating the table
    # For now, we'll just warn about this limitation
    print("  Warning: Column removal not implemented for SQLite. Manual intervention required.")
    print("  For PostgreSQL, you can manually run:")
    print("    ALTER TABLE jobs DROP COLUMN salary_currency;")
    print("    ALTER TABLE jobs DROP COLUMN salary_unit;")
    print("    ALTER TABLE rejected_jobs DROP COLUMN salary_currency;")
    print("    ALTER TABLE rejected_jobs DROP COLUMN salary_unit;")
    print("Migration 002 rollback completed!")


def main() -> None:
    """Run the migration."""
    settings = get_settings()
    engine = create_engine(settings.database_url)

    print(f"Running migration 002 on database: {settings.database_url}")
    print(f"Database dialect: {engine.dialect.name}")

    try:
        upgrade(engine)
    except Exception as e:
        print(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    main()
