"""Unified Acuity Scheduling API client.

Handles all API interactions with consistent error handling,
rate limiting, and retry logic.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from .config import API_BASE_URL, Config

logger = logging.getLogger(__name__)

# HTTP timeout in seconds
REQUEST_TIMEOUT = 10

# Rate limit retry settings
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # Exponential backoff multiplier


class AcuityAPIError(Exception):
    """Acuity API error with code and details."""

    def __init__(self, code: str, message: str, details: dict | None = None) -> None:
        """Initialize API error.

        Args:
            code: Error code (e.g., AUTH_FAILED, NOT_FOUND)
            message: Human-readable error message
            details: Optional additional error details

        """
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(f"{code}: {message}")


class AcuityClient:
    """Client for Acuity Scheduling API."""

    def __init__(self, config: Config) -> None:
        """Initialize client with config.

        Args:
            config: Configuration with credentials

        """
        config.validate()
        self.config = config
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(config.user_id, config.api_key)
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        """Make an API request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., /appointment-types)
            params: Query parameters
            json_data: JSON body for POST/PUT

        Returns:
            Parsed JSON response

        Raises:
            AcuityAPIError: On API errors

        """
        url = f"{API_BASE_URL}{endpoint}"

        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    timeout=REQUEST_TIMEOUT,
                )

                # Handle rate limiting
                if response.status_code == 429:
                    wait_time = RETRY_BACKOFF**attempt
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                # Handle auth errors
                if response.status_code == 401:
                    raise AcuityAPIError(
                        "AUTH_FAILED",
                        "Authentication failed - check credentials",
                    )

                # Handle not found
                if response.status_code == 404:
                    raise AcuityAPIError(
                        "NOT_FOUND",
                        f"Resource not found: {endpoint}",
                    )

                # Handle server errors with retry
                if response.status_code >= 500:
                    if attempt < MAX_RETRIES - 1:
                        wait_time = RETRY_BACKOFF**attempt
                        logger.warning(f"Server error, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    raise AcuityAPIError(
                        "SERVER_ERROR",
                        f"Server error: {response.status_code}",
                    )

                # Handle other client errors
                if response.status_code >= 400:
                    error_data = response.json() if response.text else {}
                    raise AcuityAPIError(
                        "API_ERROR",
                        error_data.get("message", f"Error {response.status_code}"),
                        error_data,
                    )

                # Success
                return response.json() if response.text else {}

            except requests.exceptions.Timeout:
                if attempt < MAX_RETRIES - 1:
                    logger.warning("Request timeout, retrying...")
                    continue
                raise AcuityAPIError("TIMEOUT", "Request timed out")

            except requests.exceptions.ConnectionError:
                raise AcuityAPIError("CONNECTION_ERROR", "Failed to connect to API")

        raise AcuityAPIError("MAX_RETRIES", "Max retries exceeded")

    # =========================================================================
    # Appointment Types
    # =========================================================================

    def list_appointment_types(self) -> list[dict]:
        """List all appointment types.

        Returns:
            List of appointment type objects with id, name, duration, calendarIDs

        """
        return self._request("GET", "/appointment-types")

    # =========================================================================
    # Calendars
    # =========================================================================

    def list_calendars(self) -> list[dict]:
        """List all calendars (team members).

        Returns:
            List of calendar objects with id, name, email, etc.

        """
        return self._request("GET", "/calendars")

    # =========================================================================
    # Availability
    # =========================================================================

    def get_available_dates(
        self,
        appointment_type_id: int,
        month: str,
        calendar_id: int | None = None,
    ) -> list[dict]:
        """Get dates with availability in a month.

        Args:
            appointment_type_id: Appointment type ID (required)
            month: Month in YYYY-MM format
            calendar_id: Optional calendar filter

        Returns:
            List of date objects with available dates

        """
        params: dict[str, str | int] = {
            "appointmentTypeID": appointment_type_id,
            "month": month,
        }
        if calendar_id:
            params["calendarID"] = calendar_id

        return self._request("GET", "/availability/dates", params=params)

    def get_available_times(
        self,
        appointment_type_id: int,
        date: str,
        calendar_id: int | None = None,
    ) -> list[dict]:
        """Get available time slots for a specific date.

        Args:
            appointment_type_id: Appointment type ID (required)
            date: Date in YYYY-MM-DD format
            calendar_id: Optional calendar filter

        Returns:
            List of time slot objects with ISO-8601 times

        """
        params: dict[str, str | int] = {
            "appointmentTypeID": appointment_type_id,
            "date": date,
        }
        if calendar_id:
            params["calendarID"] = calendar_id

        return self._request("GET", "/availability/times", params=params)

    def check_time_slot(
        self,
        appointment_type_id: int,
        datetime_str: str,
        calendar_id: int | None = None,
    ) -> dict:
        """Validate a specific time slot before booking.

        Args:
            appointment_type_id: Appointment type ID (required)
            datetime_str: ISO-8601 datetime string
            calendar_id: Optional calendar filter

        Returns:
            Validation result with valid boolean and details

        """
        data: dict[str, str | int] = {
            "datetime": datetime_str,
            "appointmentTypeID": appointment_type_id,
        }
        if calendar_id:
            data["calendarID"] = calendar_id

        try:
            result = self._request("POST", "/availability/check-times", json_data=data)
            return {"valid": True, "datetime": datetime_str, "result": result}
        except AcuityAPIError as e:
            return {
                "valid": False,
                "datetime": datetime_str,
                "reason": e.message,
            }

    # =========================================================================
    # Clients
    # =========================================================================

    def search_clients(self, search: str) -> list[dict]:
        """Search clients by name, email, or phone.

        Args:
            search: Partial match search string

        Returns:
            List of matching client objects

        """
        return self._request("GET", "/clients", params={"search": search})

    def create_client(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
        notes: str | None = None,
    ) -> dict:
        """Create a new client profile.

        Args:
            first_name: Client first name
            last_name: Client last name
            email: Client email address
            phone: Optional phone number
            notes: Optional internal notes

        Returns:
            Created client object

        Raises:
            AcuityAPIError: If client already exists (code: CLIENT_EXISTS)

        """
        data: dict[str, str] = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
        if phone:
            data["phone"] = phone
        if notes:
            data["notes"] = notes

        try:
            return self._request("POST", "/clients", json_data=data)
        except AcuityAPIError as e:
            if "already exists" in e.message.lower():
                raise AcuityAPIError(
                    "CLIENT_EXISTS",
                    f"Client with email {email} already exists",
                    e.details,
                )
            raise

    # =========================================================================
    # Appointments
    # =========================================================================

    def list_appointments(
        self,
        min_date: str | None = None,
        max_date: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> list[dict]:
        """List appointments with optional filters.

        Args:
            min_date: Start date filter (YYYY-MM-DD)
            max_date: End date filter (YYYY-MM-DD)
            first_name: Filter by client first name
            last_name: Filter by client last name
            email: Filter by client email

        Returns:
            List of appointment objects

        """
        params: dict[str, str] = {}
        if min_date:
            params["minDate"] = min_date
        if max_date:
            params["maxDate"] = max_date
        if first_name:
            params["firstName"] = first_name
        if last_name:
            params["lastName"] = last_name
        if email:
            params["email"] = email

        return self._request("GET", "/appointments", params=params)

    def get_appointment(self, appointment_id: int) -> dict:
        """Get details of a specific appointment.

        Args:
            appointment_id: Appointment ID

        Returns:
            Appointment object with full details

        """
        return self._request("GET", f"/appointments/{appointment_id}")

    def create_appointment(
        self,
        appointment_type_id: int,
        datetime_str: str,
        first_name: str,
        last_name: str,
        email: str,
        calendar_id: int | None = None,
        phone: str | None = None,
        notes: str | None = None,
    ) -> dict:
        """Create a new appointment.

        Args:
            appointment_type_id: Appointment type ID (required)
            datetime_str: ISO-8601 datetime string (required)
            first_name: Client first name (required)
            last_name: Client last name (required)
            email: Client email (required)
            calendar_id: Optional specific calendar
            phone: Optional client phone
            notes: Optional appointment notes

        Returns:
            Created appointment object

        """
        data: dict[str, str | int] = {
            "appointmentTypeID": appointment_type_id,
            "datetime": datetime_str,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
        if calendar_id:
            data["calendarID"] = calendar_id
        if phone:
            data["phone"] = phone
        if notes:
            data["notes"] = notes

        return self._request("POST", "/appointments", json_data=data)

    def reschedule_appointment(
        self,
        appointment_id: int,
        datetime_str: str,
        calendar_id: int | None = None,
    ) -> dict:
        """Reschedule an existing appointment.

        Args:
            appointment_id: Appointment ID to reschedule
            datetime_str: New ISO-8601 datetime string
            calendar_id: Optional new calendar (auto-finds if omitted)

        Returns:
            Updated appointment object

        """
        data: dict[str, str | int] = {"datetime": datetime_str}
        if calendar_id:
            data["calendarID"] = calendar_id

        return self._request(
            "PUT",
            f"/appointments/{appointment_id}/reschedule",
            json_data=data,
        )

    def cancel_appointment(self, appointment_id: int) -> dict:
        """Cancel an appointment.

        Args:
            appointment_id: Appointment ID to cancel

        Returns:
            Cancelled appointment object

        """
        return self._request("PUT", f"/appointments/{appointment_id}/cancel")
