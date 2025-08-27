#!/usr/bin/env python3
"""
Test script to verify salary approval logic with sample data.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from job_ingestion.approval.rules.salary_rules import salary_meets_requirements
from job_ingestion.ingestion.job_mapper import JobDataMapper

# Test data 1 - Object format with salary info
test_data_1 = [
    {
        "title": "Backend Engineer",
        "description": (
            "Join our backend team to build scalable APIs using Go and "
            "microservices architecture."
        ),
        "company": "NextGen Systems",
        "location": {"city": "Austin", "state": "TX", "country": "USA"},
        "salary": {"value": 145000, "currency": "USD"},
        "employment_type": "Full-Time",
        "posting_date": "2023-10-03",
        "company_type": "Direct Employer",
        "language": "English",
        "remote": False,
    },
    {
        "title": "Frontend Developer Intern",
        "description": (
            "Looking for an enthusiastic intern to assist in frontend "
            "development with React."
        ),
        "company": "BrightStart Talent",
        "location": {"city": "Vancouver", "state": "BC", "country": "Canada"},
        "salary": {"value": 20000, "currency": "CAD"},
        "employment_type": "Internship",
        "posting_date": "2023-10-06",
        "company_type": "Staffing Firm",
        "language": "English",
        "remote": False,
    },
    {
        "title": "Machine Learning Engineer",
        "description": (
            "Rejoignez notre équipe pour développer des modèles de "
            "machine learning avancés."
        ),
        "company": "DeepData Labs",
        "location": {"city": "Paris", "state": "Île-de-France", "country": "France"},
        "salary": {"value": 70000, "currency": "EUR"},
        "employment_type": "Full-Time",
        "posting_date": "2023-10-11",
        "company_type": "Direct Employer",
        "language": "French",
        "remote": False,
    },
    {
        "title": "Agile Project Lead",
        "description": (
            "Drive cross-functional teams in a remote-first environment "
            "with agile principles."
        ),
        "company": "Orbit Global",
        "location": {"city": "Manchester", "state": "England", "country": "UK"},
        "salary": {"value": 85000, "currency": "GBP"},
        "employment_type": "Full-Time",
        "posting_date": "2023-10-13",
        "company_type": "Direct Employer",
        "language": "English",
        "remote": True,
    },
    {
        "title": "DevOps Consultant",
        "description": (
            "We are seeking a highly skilled DevOps Consultant to help scale "
            "our CI/CD infrastructure and cloud operations."
        ),
        "company": "CloudWorks Pro",
        "location": {"city": "Seattle", "state": "WA", "country": "USA"},
        "salary": {"value": 65, "currency": "USD", "unit": "hourly"},
        "employment_type": "Contract",
        "posting_date": "2023-10-14",
        "company_type": "Consulting Agency",
        "language": "English",
        "remote": True,
    },
]

# Test data 2 - Flat format
test_data_2 = [
    {
        "title": "Senior Software Engineer",
        "description": (
            "We are looking for a Senior Software Engineer with experience "
            "in Go and distributed systems."
        ),
        "company": "Tech Innovators Inc.",
        "location": "New York, NY, USA",
        "salary": 150000,
        "employment_type": "Full-Time",
        "posting_date": "2023-10-01",
        "company_type": "Direct Employer",
        "language": "English",
        "remote": False,
    },
    {
        "title": "Junior Developer",
        "description": "An excellent opportunity for a Junior Developer to join a dynamic team.",
        "company": "Staffing Solutions",
        "location": "Toronto, ON, Canada",
        "salary": 80000,
        "employment_type": "Full-Time",
        "posting_date": "2023-10-05",
        "company_type": "Staffing Firm",
        "language": "",
        "remote": False,
    },
    {
        "title": "Data Scientist",
        "description": "Nous recherchons un Data Scientist expérimenté.",
        "company": "Analytics Corp.",
        "location": "Montreal, QC, Canada",
        "salary": 62.5,
        "employment_type": "Full-Time",
        "posting_date": "2023-10-10",
        "company_type": "Direct Employer",
        "language": "French",
        "remote": False,
    },
    {
        "title": "Project Manager",
        "description": "Lead projects across various domains.",
        "company": "Global Enterprises",
        "location": "London, UK",
        "salary": 80000,
        "employment_type": "Full-Time",
        "posting_date": "2023-10-12",
        "company_type": "Direct Employer",
        "language": "English",
        "remote": True,
    },
]


def test_salary_approval() -> None:
    """Test salary approval logic with sample data."""
    mapper = JobDataMapper()

    print("=" * 80)
    print("SALARY APPROVAL TEST RESULTS")
    print("=" * 80)

    all_test_data = [
        ("Test Data 1 (Object Format)", test_data_1),
        ("Test Data 2 (Flat Format)", test_data_2),
    ]

    for dataset_name, test_data in all_test_data:
        print(f"\n{dataset_name}:")
        print("-" * 50)

        for i, job_data in enumerate(test_data, 1):
            print(f"\n{i}. {job_data['title']} at {job_data.get('company', 'Unknown')}")

            # Map the job data
            mapped_data = mapper.map_job_data(job_data)

            # Extract relevant salary info for display
            salary_min = mapped_data.get("salary_min")
            salary_currency = mapped_data.get("salary_currency", "USD")
            salary_unit = mapped_data.get("salary_unit", "annual")

            print(f"   Salary: {salary_min} {salary_currency} ({salary_unit})")

            # Test approval
            approved, reason = salary_meets_requirements(mapped_data)

            if approved:
                print("   ✅ APPROVED")
            else:
                print(f"   ❌ REJECTED: {reason}")


if __name__ == "__main__":
    test_salary_approval()
