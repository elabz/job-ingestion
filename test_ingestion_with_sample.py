#!/usr/bin/env python3
"""
Test script to verify the updated ingestion system with the sample job data.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from job_ingestion.ingestion.service import IngestionService
from job_ingestion.storage.models import Job, RejectedJob
from job_ingestion.storage.repositories import get_engine, get_session, get_sessionmaker
from job_ingestion.utils.config import get_settings

# Sample job data from the user
sample_job = {
    "lowerBand": 90000,
    "upperBand": 110000,
    "isLaddersEstimate": False,
    "estimatedLowerBand": 100000,
    "estimatedUpperBand": 150000,
    "compensationBonus": "",
    "salary": "",
    "compensationMin": "90000",
    "compensationMax": "110000",
    "baseSalary": "90000 - 110000",
    "compensationOther": "",
    "jobId": "71195624",
    "title": "AI Engineer - Enterprise AI Enablement",
    "shortDescription": (
        "The AI Engineer will be responsible for designing and deploying intelligent agents "
        "and systems to support Rockefeller Capital Management's AI transformation. This role "
        "involves collaborating with business stakeholders to create scalable, AI-enabled "
        "solutions that enhance the firm's operational efficiency."
    ),
    "fullDescription": "<strong>About Rockefeller Capital Management</strong><br><br>Rockefeller .",
    "companyName": "Rockefeller Capital Management",
    "otherLocations": [],
    "locations": [
        {
            "id": "82561258",
            "text": "Trenton, NJ",
            "seoSlug": (
                "ai-engineer-enterprise-ai-enablement-rockefeller-capital-management-trenton-nj_82561258"
            ),
            "seoUri": (
                "/job/ai-engineer-enterprise-ai-enablement-rockefeller-capital-management-trenton-nj_82561258"
            ),
            "active": True,
            "coords": {"latitude": 40.2385, "longitude": -74.7175},
            "zipcode": "08619",
            "brokers": [],
        }
    ],
    "yearsExperience": "Less than 5",
    "yearsExperienceId": 1,
    "postingDate": "Jul 28, 2025, 2:43:15 PM",
    "postedDates": [{"postingDate": "Jul 28, 2025, 2:43:15 PM"}],
    "recruiterAnonymous": False,
    "zipcode": "08619",
    "county": "MERCER",
    "companyIsConfidential": False,
    "industryName": "Information Technology",
    "industryId": 2012,
    "score": 0.0,
    "promoted": False,
    "jobLocationId": {"id": "82561258", "numericId": 82561258},
    "location": "Trenton, NJ",
    "coordinates": {"latitude": 40.2385, "longitude": -74.7175},
    "marketing": False,
    "active": True,
    "allowExternalApply": True,
    "externalApplicationUrl": "https://careers-rcm.icims.com/jobs/4240/ai-engineer-%e2%80%93-enterprise-ai-enablement/job",
    "classifications": [{"roles": [3400], "source": "manual", "version": 3}],
    "classification": {"roles": [3400], "source": "manual", "version": 3},
    "jobStatus": "Approved",
    "jobTypeId": 3,
    "entryDate": "Jul 28, 2025, 2:43:15 PM",
    "updateTime": "Jul 28, 2025, 2:43:15 PM",
    "remoteFlag": "In-Person",
    "collapseKey": "ai-engineer-enterprise-ai-enablement-rockefeller-capital-management",
    "candidateResidency": [],
    "salaryIsConfidential": False,
    "questions": [],
    "seoJobLink": "https://www.theladders.com/job/ai-engineer-enterprise-ai-enablement-rockefeller-capital-management-trenton-nj_82561258",
    "featured": [],
    "currentlyFeatured": False,
    "seoLocation": "trenton-nj",
    "promotedLabelVisible": False,
}


def main() -> None:
    print("Testing ingestion system with sample job data...")

    # Initialize ingestion service
    service = IngestionService()

    # Ingest the sample job
    processing_id = service.ingest_batch([sample_job])
    print(f"Processing ID: {processing_id}")

    # Get processing status
    status = service.get_processing_status(processing_id)
    print(f"Processing status: {status}")

    # Check what was stored in the database
    settings = get_settings()
    engine = get_engine(settings.database_url)
    session_maker = get_sessionmaker(engine)

    with get_session(session_maker) as s:
        # Check approved jobs
        jobs = s.query(Job).all()
        print(f"\nApproved jobs count: {len(jobs)}")

        if jobs:
            job = jobs[0]
            print("Job details:")
            print(f"  External ID: {job.external_id}")
            print(f"  Title: {job.title}")
            print(f"  Company: {job.company_name}")
            print(f"  Location: {job.primary_location}")
            print(f"  Salary range: {job.salary_min} - {job.salary_max}")
            print(f"  Industry: {job.industry_name}")
            print(f"  Remote flag: {job.remote_flag}")
            print(f"  Coordinates: ({job.latitude}, {job.longitude})")
            print(f"  Locations data: {job.locations_data}")

        # Check rejected jobs
        rejected_jobs = s.query(RejectedJob).all()
        print(f"\nRejected jobs count: {len(rejected_jobs)}")

        if rejected_jobs:
            rejected_job = rejected_jobs[0]
            print("Rejected job details:")
            print(f"  External ID: {rejected_job.external_id}")
            print(f"  Title: {rejected_job.title}")
            print(f"  Rejection reasons: {rejected_job.rejection_reasons}")


if __name__ == "__main__":
    main()
