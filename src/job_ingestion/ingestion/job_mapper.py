"""
Job data mapper for extracting and mapping job properties to database columns.

This module handles the complex task of mapping incoming job data (which can vary
in structure) to the standardized database schema with comprehensive job properties.
"""

from datetime import datetime
from typing import Any

from dateutil import parser as date_parser  # type: ignore[import-untyped]

from job_ingestion.utils.logging import get_logger

logger = get_logger("ingestion.job_mapper")


class JobDataMapper:
    """Maps raw job data to standardized database fields."""

    def map_job_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """
        Map raw job data to database fields.

        Args:
            raw_data: Raw job data from external source

        Returns:
            Dictionary with mapped fields for database insertion
        """
        mapped = {}

        # Basic job information
        mapped.update(self._map_basic_info(raw_data))

        # Salary information
        mapped.update(self._map_salary_info(raw_data))

        # Company information
        mapped.update(self._map_company_info(raw_data))

        # Location information
        mapped.update(self._map_location_info(raw_data))

        # Experience and job type
        mapped.update(self._map_experience_info(raw_data))

        # Dates
        mapped.update(self._map_dates(raw_data))

        # URLs and links
        mapped.update(self._map_urls(raw_data))

        # Flags and metadata
        mapped.update(self._map_flags(raw_data))

        # Complex JSON data
        mapped.update(self._map_json_data(raw_data))

        return mapped

    def _map_basic_info(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map basic job information."""
        return {
            "external_id": self._get_external_id(raw),
            "title": self._get_title(raw),
            "short_description": self._safe_get_string(
                raw, ["shortDescription", "summary", "short_desc"]
            ),
            "full_description": self._safe_get_string(
                raw, ["fullDescription", "description", "details", "full_desc"]
            ),
        }

    def _map_salary_info(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map salary and compensation information."""
        return {
            "salary_min": self._safe_get_numeric(
                raw, ["lowerBand", "compensationMin", "salary_min", "min_salary"]
            ),
            "salary_max": self._safe_get_numeric(
                raw, ["upperBand", "compensationMax", "salary_max", "max_salary"]
            ),
            "estimated_salary_min": self._safe_get_numeric(
                raw, ["estimatedLowerBand", "estimated_min"]
            ),
            "estimated_salary_max": self._safe_get_numeric(
                raw, ["estimatedUpperBand", "estimated_max"]
            ),
            "base_salary": self._safe_get_string(
                raw, ["baseSalary", "base_salary", "salary_range"]
            ),
            "is_salary_estimate": self._safe_get_bool(raw, ["isLaddersEstimate", "is_estimate"]),
            "is_salary_confidential": self._safe_get_bool(
                raw, ["salaryIsConfidential", "salary_confidential"]
            ),
        }

    def _map_company_info(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map company information."""
        return {
            "company_name": self._safe_get_string(
                raw, ["companyName", "company", "employer", "organization"]
            ),
            "is_company_confidential": self._safe_get_bool(
                raw, ["companyIsConfidential", "company_confidential"]
            ),
        }

    def _map_location_info(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map location information."""
        # Extract primary location from various possible sources
        primary_location = None
        latitude = None
        longitude = None

        # Try to get location from the location field
        if "location" in raw and isinstance(raw["location"], str):
            primary_location = raw["location"]

        # Try to get from locations array
        elif "locations" in raw and isinstance(raw["locations"], list) and raw["locations"]:
            first_location = raw["locations"][0]
            if isinstance(first_location, dict):
                primary_location = first_location.get("text")
                coords = first_location.get("coords", {})
                if isinstance(coords, dict):
                    latitude = coords.get("latitude")
                    longitude = coords.get("longitude")

        # Try coordinates from top level
        if not latitude or not longitude:
            coords = raw.get("coordinates", {})
            if isinstance(coords, dict):
                latitude = coords.get("latitude")
                longitude = coords.get("longitude")

        return {
            "primary_location": primary_location,
            "zipcode": self._safe_get_string(raw, ["zipcode", "zip", "postal_code"]),
            "county": self._safe_get_string(raw, ["county", "region"]),
            "latitude": latitude,
            "longitude": longitude,
        }

    def _map_experience_info(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map experience and job type information."""
        return {
            "years_experience": self._safe_get_string(
                raw, ["yearsExperience", "experience", "experience_level"]
            ),
            "years_experience_id": self._safe_get_int(raw, ["yearsExperienceId", "experience_id"]),
            "industry_name": self._safe_get_string(raw, ["industryName", "industry", "sector"]),
            "industry_id": self._safe_get_int(raw, ["industryId", "industry_id"]),
            "job_type_id": self._safe_get_int(raw, ["jobTypeId", "job_type_id", "type_id"]),
            "remote_flag": self._safe_get_string(raw, ["remoteFlag", "remote", "work_type"]),
        }

    def _map_dates(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map date fields."""
        return {
            "posting_date": self._parse_date(raw.get("postingDate")),
            "entry_date": self._parse_date(raw.get("entryDate")),
            "update_date": self._parse_date(raw.get("updateTime")),
        }

    def _map_urls(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map URL and link fields."""
        return {
            "external_application_url": self._safe_get_string(
                raw, ["externalApplicationUrl", "apply_url", "application_url"]
            ),
            "seo_job_link": self._safe_get_string(raw, ["seoJobLink", "job_url", "permalink"]),
            "seo_location": self._safe_get_string(raw, ["seoLocation", "location_slug"]),
        }

    def _map_flags(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map boolean flags and metadata."""
        return {
            "is_active": self._safe_get_bool(raw, ["active", "is_active"], default=True),
            "allows_external_apply": self._safe_get_bool(
                raw, ["allowExternalApply", "external_apply"], default=True
            ),
            "is_promoted": self._safe_get_bool(raw, ["promoted", "is_promoted"], default=False),
            "is_featured": self._safe_get_bool(
                raw, ["currentlyFeatured", "featured", "is_featured"], default=False
            ),
            "is_marketing": self._safe_get_bool(raw, ["marketing", "is_marketing"], default=False),
            "recruiter_anonymous": self._safe_get_bool(
                raw, ["recruiterAnonymous", "anonymous"], default=False
            ),
            "score": self._safe_get_float(raw, ["score", "relevance_score"]),
        }

    def _map_json_data(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map complex data that should be stored as JSON."""
        json_data = {}

        # Store locations array as JSON
        if "locations" in raw:
            json_data["locations_data"] = raw["locations"]

        # Store classifications
        if "classifications" in raw:
            json_data["classifications_data"] = raw["classifications"]
        elif "classification" in raw:
            json_data["classifications_data"] = raw["classification"]

        # Store posted dates array
        if "postedDates" in raw:
            json_data["posted_dates"] = raw["postedDates"]

        # Store other arrays
        if "candidateResidency" in raw:
            json_data["candidate_residency"] = raw["candidateResidency"]

        if "questions" in raw:
            json_data["questions"] = raw["questions"]

        if "featured" in raw:
            json_data["featured_data"] = raw["featured"]

        # Store additional metadata that doesn't fit elsewhere
        additional_metadata = {}
        metadata_fields = [
            "jobLocationId",
            "collapseKey",
            "promotedLabelVisible",
            "otherLocations",
            "marketing",
            "jobStatus",
        ]

        for field in metadata_fields:
            if field in raw:
                additional_metadata[field] = raw[field]

        if additional_metadata:
            json_data["additional_metadata"] = additional_metadata

        # Store collapse key separately for indexing
        json_data["collapse_key"] = self._safe_get_string(raw, ["collapseKey", "collapse_key"])

        return json_data

    # Helper methods
    def _get_external_id(self, raw: dict[str, Any]) -> str:
        """Extract external ID with fallbacks."""
        ext_id = raw.get("jobId") or raw.get("id") or raw.get("external_id")
        if ext_id:
            return str(ext_id)
        # Generate a unique ID based on available data
        title = self._get_title(raw)
        company = raw.get("companyName", "unknown")
        return f"{company}_{title}".replace(" ", "_").lower()[:100]

    def _get_title(self, raw: dict[str, Any]) -> str:
        """Extract job title with fallbacks."""
        title = raw.get("title") or raw.get("job_title") or raw.get("position")
        if isinstance(title, str) and title.strip():
            return title.strip()
        return "(untitled)"

    def _safe_get_string(
        self, raw: dict[str, Any], keys: list[str], default: str | None = None
    ) -> str | None:
        """Safely get string value from multiple possible keys."""
        for key in keys:
            value = raw.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return default

    def _safe_get_numeric(self, raw: dict[str, Any], keys: list[str]) -> float | None:
        """Safely get numeric value from multiple possible keys."""
        for key in keys:
            value = raw.get(key)
            if isinstance(value, int | float):
                return float(value)
            elif isinstance(value, str) and value.strip():
                try:
                    # Handle string numbers like "90000"
                    return float(value.replace(",", ""))
                except (ValueError, TypeError):
                    continue
        return None

    def _safe_get_int(self, raw: dict[str, Any], keys: list[str]) -> int | None:
        """Safely get integer value from multiple possible keys."""
        numeric = self._safe_get_numeric(raw, keys)
        return int(numeric) if numeric is not None else None

    def _safe_get_float(self, raw: dict[str, Any], keys: list[str]) -> float | None:
        """Safely get float value from multiple possible keys."""
        return self._safe_get_numeric(raw, keys)

    def _safe_get_bool(
        self, raw: dict[str, Any], keys: list[str], default: bool | None = None
    ) -> bool | None:
        """Safely get boolean value from multiple possible keys."""
        for key in keys:
            value = raw.get(key)
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                lower_val = value.lower()
                if lower_val in ("true", "1", "yes", "on"):
                    return True
                elif lower_val in ("false", "0", "no", "off"):
                    return False
        return default

    def _parse_date(self, date_value: Any) -> datetime | None:
        """Parse date from various formats."""
        if not date_value:
            return None

        if isinstance(date_value, datetime):
            return date_value

        if isinstance(date_value, str):
            try:
                # Handle common date formats
                parsed_date: datetime = date_parser.parse(date_value)
                return parsed_date
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not parse date '{date_value}': {e}")
                return None

        return None
