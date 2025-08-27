#!/usr/bin/env python3
"""
Simple script to run the database migration for expanded job schema.
This creates tables with the new schema directly using SQLAlchemy models.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from job_ingestion.storage.models import Base
from job_ingestion.storage.repositories import get_engine
from job_ingestion.utils.config import get_settings


def main() -> None:
    """Run the migration to create tables with expanded schema."""
    print("Running database migration...")

    settings = get_settings()
    print(f"Database URL: {settings.database_url}")

    engine = get_engine(settings.database_url)
    print(f"Database dialect: {engine.dialect.name}")

    try:
        # Create all tables with the new schema
        Base.metadata.create_all(bind=engine)
        print("✅ Migration completed successfully!")
        print("✅ Tables created: jobs, rejected_jobs")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
