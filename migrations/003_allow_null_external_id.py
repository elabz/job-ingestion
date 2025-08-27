#!/usr/bin/env python3
"""
Migration 003: Allow NULL values for external_id in both jobs and rejected_jobs tables.

This migration removes the NOT NULL constraint from external_id columns to allow
jobs without external identifiers to be stored with NULL values.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from job_ingestion.utils.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


def upgrade(engine: Engine) -> None:
    """Apply the migration - allow NULL values for external_id columns."""
    print("Updating external_id columns to allow NULL values...")

    with engine.connect() as conn:
        if engine.dialect.name == "postgresql":
            # PostgreSQL: Remove NOT NULL constraint
            try:
                conn.execute(text("ALTER TABLE jobs ALTER COLUMN external_id DROP NOT NULL"))
                print("  Updated jobs.external_id to allow NULL")
            except Exception as e:
                print(f"  Warning: Could not update jobs.external_id: {e}")

            try:
                conn.execute(
                    text("ALTER TABLE rejected_jobs ALTER COLUMN external_id DROP NOT NULL")
                )
                print("  Updated rejected_jobs.external_id to allow NULL")
            except Exception as e:
                print(f"  Warning: Could not update rejected_jobs.external_id: {e}")

        elif engine.dialect.name == "sqlite":
            # SQLite: Need to recreate tables since ALTER COLUMN is limited
            print("  SQLite detected - recreating tables to allow NULL external_id")

            # For jobs table
            try:
                # Create new table with proper schema and nullable external_id
                conn.execute(
                    text(
                        """
                    CREATE TABLE jobs_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        external_id TEXT,
                        title TEXT NOT NULL,
                        salary_min DECIMAL(12,2),
                        salary_max DECIMAL(12,2),
                        estimated_salary_min DECIMAL(12,2),
                        estimated_salary_max DECIMAL(12,2),
                        base_salary TEXT,
                        salary_currency TEXT,
                        salary_unit TEXT,
                        is_salary_estimate BOOLEAN,
                        is_salary_confidential BOOLEAN DEFAULT 0,
                        company_name TEXT,
                        is_company_confidential BOOLEAN DEFAULT 0,
                        short_description TEXT,
                        full_description TEXT,
                        primary_location TEXT,
                        zipcode TEXT,
                        county TEXT,
                        latitude DECIMAL(10,8),
                        longitude DECIMAL(11,8),
                        years_experience INTEGER,
                        years_experience_id INTEGER,
                        industry_name TEXT,
                        industry_id INTEGER,
                        job_type_id INTEGER,
                        remote_flag BOOLEAN DEFAULT 0,
                        posting_date DATETIME,
                        entry_date DATETIME,
                        update_date DATETIME,
                        external_application_url TEXT,
                        seo_job_link TEXT,
                        seo_location TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        allows_external_apply BOOLEAN DEFAULT 1,
                        is_promoted BOOLEAN DEFAULT 0,
                        is_featured BOOLEAN DEFAULT 0,
                        is_marketing BOOLEAN DEFAULT 0,
                        recruiter_anonymous BOOLEAN DEFAULT 0,
                        score DECIMAL(5,2),
                        collapse_key TEXT,
                        approval_status TEXT DEFAULT 'pending',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                    )
                )

                # Copy data from old table
                conn.execute(
                    text(
                        """
                    INSERT INTO jobs_new SELECT * FROM jobs
                """
                    )
                )

                # Drop old table and rename new one
                conn.execute(text("DROP TABLE jobs"))
                conn.execute(text("ALTER TABLE jobs_new RENAME TO jobs"))
                print("  Recreated jobs table with nullable external_id")

            except Exception as e:
                print(f"  Warning: Could not recreate jobs table: {e}")

            # For rejected_jobs table
            try:
                # Create new table with proper schema and nullable external_id
                conn.execute(
                    text(
                        """
                    CREATE TABLE rejected_jobs_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rejection_reasons TEXT NOT NULL,
                        external_id TEXT,
                        title TEXT NOT NULL,
                        salary_min DECIMAL(12,2),
                        salary_max DECIMAL(12,2),
                        estimated_salary_min DECIMAL(12,2),
                        estimated_salary_max DECIMAL(12,2),
                        base_salary TEXT,
                        salary_currency TEXT,
                        salary_unit TEXT,
                        is_salary_estimate BOOLEAN,
                        is_salary_confidential BOOLEAN DEFAULT 0,
                        company_name TEXT,
                        is_company_confidential BOOLEAN DEFAULT 0,
                        short_description TEXT,
                        full_description TEXT,
                        primary_location TEXT,
                        zipcode TEXT,
                        county TEXT,
                        latitude DECIMAL(10,8),
                        longitude DECIMAL(11,8),
                        years_experience INTEGER,
                        years_experience_id INTEGER,
                        industry_name TEXT,
                        industry_id INTEGER,
                        job_type_id INTEGER,
                        remote_flag BOOLEAN DEFAULT 0,
                        posting_date DATETIME,
                        entry_date DATETIME,
                        update_date DATETIME,
                        external_application_url TEXT,
                        seo_job_link TEXT,
                        seo_location TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        allows_external_apply BOOLEAN DEFAULT 1,
                        is_promoted BOOLEAN DEFAULT 0,
                        is_featured BOOLEAN DEFAULT 0,
                        is_marketing BOOLEAN DEFAULT 0,
                        recruiter_anonymous BOOLEAN DEFAULT 0,
                        score DECIMAL(5,2),
                        collapse_key TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                    )
                )

                # Copy data from old table (if any exists)
                conn.execute(
                    text(
                        """
                    INSERT INTO rejected_jobs_new SELECT * FROM rejected_jobs
                """
                    )
                )

                # Drop old table and rename new one
                conn.execute(text("DROP TABLE rejected_jobs"))
                conn.execute(text("ALTER TABLE rejected_jobs_new RENAME TO rejected_jobs"))
                print("  Recreated rejected_jobs table with nullable external_id")

            except Exception as e:
                print(f"  Warning: Could not recreate rejected_jobs table: {e}")

        conn.commit()

    print("Migration completed successfully!")


def downgrade(engine: Engine) -> None:
    """Rollback the migration - restore NOT NULL constraint for external_id."""
    print("Rolling back migration - restoring NOT NULL constraint...")

    with engine.connect() as conn:
        if engine.dialect.name == "postgresql":
            # First update any NULL values to a default
            try:
                conn.execute(
                    text(
                        """
                    UPDATE jobs SET external_id = 'unknown_' || LOWER(REPLACE(title, ' ', '_'))
                    WHERE external_id IS NULL
                """
                    )
                )
                conn.execute(
                    text(
                        """
                    UPDATE rejected_jobs
                    SET external_id = 'unknown_' || LOWER(REPLACE(title, ' ', '_'))
                    WHERE external_id IS NULL
                """
                    )
                )

                # Then add NOT NULL constraint back
                conn.execute(text("ALTER TABLE jobs ALTER COLUMN external_id SET NOT NULL"))
                conn.execute(
                    text("ALTER TABLE rejected_jobs ALTER COLUMN external_id SET NOT NULL")
                )
                print("  Restored NOT NULL constraint for external_id columns")

            except Exception as e:
                print(f"  Warning: Could not restore NOT NULL constraint: {e}")

        conn.commit()

    print("Migration rollback completed!")


def main() -> None:
    """Run the migration."""
    settings = get_settings()
    engine = create_engine(settings.database_url)

    print(f"Running migration on database: {settings.database_url}")
    print(f"Database dialect: {engine.dialect.name}")

    try:
        upgrade(engine)
    except Exception as e:
        print(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    main()
