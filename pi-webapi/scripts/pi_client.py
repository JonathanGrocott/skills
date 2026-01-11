"""AVEVA PI Web API Client for historian data retrieval.

This client provides read-only access to PI System data through the PI Web API,
including current values, historical data, and Asset Framework navigation.
"""

import base64
import logging
from typing import Any
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)


class PIWebAPIClient:
    """Client for interacting with AVEVA PI Web API."""

    def __init__(
        self,
        base_url: str = "https://PI1AVDEVA.web.boeing.com/piwebapi",
        username: str | None = None,
        password: str | None = None,
        default_data_server: str = "PI1AVDEVA",
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ):
        """Initialize the PI Web API client.

        Args:
            base_url: Base URL for the PI Web API
            username: Username for basic authentication
            password: Password for basic authentication
            default_data_server: Default PI Data Archive server name
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip("/")
        self.default_data_server = default_data_server
        self.timeout = timeout

        # Setup authentication
        headers = {"Accept": "application/json"}
        if username and password:
            auth_string = f"{username}:{password}"
            auth_bytes = auth_string.encode("ascii")
            b64_auth = base64.b64encode(auth_bytes).decode("ascii")
            headers["Authorization"] = f"Basic {b64_auth}"

        self._client = httpx.Client(
            headers=headers,
            timeout=timeout,
            verify=verify_ssl,
        )

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request to the API.

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            ValueError: If request fails or returns error
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self._client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise ValueError(f"PI Web API request failed: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"Request error: {e}")
            raise ValueError(f"PI Web API request error: {e}")

    # Point operations

    def get_point_by_path(self, path: str) -> dict[str, Any]:
        """Get PI Point by path.

        Args:
            path: Point path (e.g., "\\\\PI1AVDEVA\\TAG001")

        Returns:
            Point object with WebId and metadata
        """
        return self._get("/points", params={"path": path})

    def get_point_by_webid(self, webid: str) -> dict[str, Any]:
        """Get PI Point by WebId.

        Args:
            webid: Point WebId

        Returns:
            Point object with metadata
        """
        return self._get(f"/points/{webid}")

    def search_points(
        self,
        name_filter: str | None = None,
        description_filter: str | None = None,
        max_count: int = 100,
    ) -> dict[str, Any]:
        """Search for PI Points in the default data server.

        Args:
            name_filter: Name filter (supports wildcards *)
            description_filter: Description filter
            max_count: Maximum number of results

        Returns:
            Dictionary with 'Items' list of matching points
        """
        # First, get the default data server WebId
        ds_response = self._get("/dataservers", params={"path": f"\\\\{self.default_data_server}"})
        ds_webid = ds_response["WebId"]

        params: dict[str, Any] = {"maxCount": max_count}
        if name_filter:
            params["nameFilter"] = name_filter
        if description_filter:
            params["descriptionFilter"] = description_filter

        return self._get(f"/dataservers/{ds_webid}/points", params=params)

    # Stream operations (data retrieval)

    def get_value_by_webid(self, webid: str) -> dict[str, Any]:
        """Get current value for a stream by WebId.

        Args:
            webid: Stream WebId (from point or attribute)

        Returns:
            Current value with timestamp and quality
        """
        return self._get(f"/streams/{webid}/value")

    def get_current_value_by_tag(self, tag_name: str, data_server: str | None = None) -> dict[str, Any]:
        """Get current value for a PI tag.

        Args:
            tag_name: Tag name (without server prefix)
            data_server: Data server name (uses default if None)

        Returns:
            Current value with timestamp and quality
        """
        server = data_server or self.default_data_server
        path = f"\\\\{server}\\{tag_name}"
        point = self.get_point_by_path(path)
        return self.get_value_by_webid(point["WebId"])

    def get_recorded_values_by_webid(
        self,
        webid: str,
        start_time: str = "*-1d",
        end_time: str = "*",
        max_count: int = 1000,
    ) -> dict[str, Any]:
        """Get recorded (archive) values for a stream.

        Args:
            webid: Stream WebId
            start_time: Start time expression (e.g., "*-24h", "2024-01-01T00:00:00Z")
            end_time: End time expression (e.g., "*", "2024-01-02T00:00:00Z")
            max_count: Maximum number of values

        Returns:
            Dictionary with 'Items' list of values
        """
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "maxCount": max_count,
        }
        return self._get(f"/streams/{webid}/recorded", params=params)

    def get_recorded_values_by_tag(
        self,
        tag_name: str,
        start_time: str = "*-1d",
        end_time: str = "*",
        max_count: int = 1000,
        data_server: str | None = None,
    ) -> dict[str, Any]:
        """Get recorded values for a PI tag.

        Args:
            tag_name: Tag name
            start_time: Start time expression
            end_time: End time expression
            max_count: Maximum number of values
            data_server: Data server name (uses default if None)

        Returns:
            Dictionary with 'Items' list of values
        """
        server = data_server or self.default_data_server
        path = f"\\\\{server}\\{tag_name}"
        point = self.get_point_by_path(path)
        return self.get_recorded_values_by_webid(
            point["WebId"],
            start_time=start_time,
            end_time=end_time,
            max_count=max_count,
        )

    def get_interpolated_values_by_webid(
        self,
        webid: str,
        start_time: str = "*-1d",
        end_time: str = "*",
        interval: str = "1h",
    ) -> dict[str, Any]:
        """Get interpolated values at regular intervals.

        Args:
            webid: Stream WebId
            start_time: Start time expression
            end_time: End time expression
            interval: Time interval (e.g., "1h", "15m", "1d")

        Returns:
            Dictionary with 'Items' list of interpolated values
        """
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "interval": interval,
        }
        return self._get(f"/streams/{webid}/interpolated", params=params)

    def get_interpolated_values_by_tag(
        self,
        tag_name: str,
        start_time: str = "*-1d",
        end_time: str = "*",
        interval: str = "1h",
        data_server: str | None = None,
    ) -> dict[str, Any]:
        """Get interpolated values for a PI tag.

        Args:
            tag_name: Tag name
            start_time: Start time expression
            end_time: End time expression
            interval: Time interval
            data_server: Data server name (uses default if None)

        Returns:
            Dictionary with 'Items' list of interpolated values
        """
        server = data_server or self.default_data_server
        path = f"\\\\{server}\\{tag_name}"
        point = self.get_point_by_path(path)
        return self.get_interpolated_values_by_webid(
            point["WebId"],
            start_time=start_time,
            end_time=end_time,
            interval=interval,
        )

    def get_summary_values_by_webid(
        self,
        webid: str,
        start_time: str = "*-1d",
        end_time: str = "*",
        summary_type: str = "Average",
        summary_duration: str = "1h",
    ) -> dict[str, Any]:
        """Get summary statistics for a stream.

        Args:
            webid: Stream WebId
            start_time: Start time expression
            end_time: End time expression
            summary_type: Summary type (Average, Total, Minimum, Maximum, etc.)
            summary_duration: Duration for each summary interval

        Returns:
            Dictionary with 'Items' list of summaries
        """
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "summaryType": summary_type,
            "summaryDuration": summary_duration,
        }
        return self._get(f"/streams/{webid}/summary", params=params)

    def get_summary_values_by_tag(
        self,
        tag_name: str,
        start_time: str = "*-1d",
        end_time: str = "*",
        summary_type: str = "Average",
        summary_duration: str = "1h",
        data_server: str | None = None,
    ) -> dict[str, Any]:
        """Get summary statistics for a PI tag.

        Args:
            tag_name: Tag name
            start_time: Start time expression
            end_time: End time expression
            summary_type: Summary type
            summary_duration: Duration for each summary interval
            data_server: Data server name (uses default if None)

        Returns:
            Dictionary with 'Items' list of summaries
        """
        server = data_server or self.default_data_server
        path = f"\\\\{server}\\{tag_name}"
        point = self.get_point_by_path(path)
        return self.get_summary_values_by_webid(
            point["WebId"],
            start_time=start_time,
            end_time=end_time,
            summary_type=summary_type,
            summary_duration=summary_duration,
        )

    # Asset Framework operations

    def get_asset_database_by_path(self, path: str) -> dict[str, Any]:
        """Get Asset Database by path.

        Args:
            path: Database path (e.g., "\\\\AF_SERVER\\DatabaseName")

        Returns:
            Database object with WebId and metadata
        """
        return self._get("/assetdatabases", params={"path": path})

    def get_elements(self, database_or_element_webid: str, max_count: int = 100) -> dict[str, Any]:
        """Get elements (children) under a database or element.

        Args:
            database_or_element_webid: Parent WebId
            max_count: Maximum number of elements

        Returns:
            Dictionary with 'Items' list of elements
        """
        # Try as database first
        try:
            return self._get(f"/assetdatabases/{database_or_element_webid}/elements", params={"maxCount": max_count})
        except ValueError:
            # Try as element
            return self._get(f"/elements/{database_or_element_webid}/elements", params={"maxCount": max_count})

    def get_element_by_path(self, path: str) -> dict[str, Any]:
        """Get Element by path.

        Args:
            path: Element path (e.g., "\\\\AF_SERVER\\DB\\Site\\Machine")

        Returns:
            Element object with WebId and metadata
        """
        return self._get("/elements", params={"path": path})

    def get_element_by_webid(self, webid: str) -> dict[str, Any]:
        """Get Element by WebId.

        Args:
            webid: Element WebId

        Returns:
            Element object with metadata
        """
        return self._get(f"/elements/{webid}")

    def get_child_elements(self, element_webid: str, max_count: int = 100) -> dict[str, Any]:
        """Get child elements.

        Args:
            element_webid: Parent element WebId
            max_count: Maximum number of children

        Returns:
            Dictionary with 'Items' list of child elements
        """
        return self._get(f"/elements/{element_webid}/elements", params={"maxCount": max_count})

    def get_element_attributes(
        self,
        element_webid: str,
        name_filter: str | None = None,
        max_count: int = 100,
    ) -> dict[str, Any]:
        """Get attributes for an element.

        Args:
            element_webid: Element WebId
            name_filter: Filter attributes by name (supports wildcards)
            max_count: Maximum number of attributes

        Returns:
            Dictionary with 'Items' list of attributes
        """
        params: dict[str, Any] = {"maxCount": max_count}
        if name_filter:
            params["nameFilter"] = name_filter

        return self._get(f"/elements/{element_webid}/attributes", params=params)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "PIWebAPIClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


if __name__ == "__main__":
    import os

    # Example usage
    username = os.environ.get("PI_USERNAME")
    password = os.environ.get("PI_PASSWORD")

    if not username or not password:
        print("Error: PI_USERNAME and PI_PASSWORD environment variables must be set")
        exit(1)

    client = PIWebAPIClient(
        username=username,
        password=password,
    )

    # Get current value
    try:
        value = client.get_current_value_by_tag("TAG001")
        print(f"Current value: {value['Value']} {value.get('UnitsAbbreviation', '')}")
        print(f"Timestamp: {value['Timestamp']}")
        print(f"Quality - Good: {value.get('Good', False)}")
    except ValueError as e:
        print(f"Error: {e}")
