"""Keyword Insights MCP Server.

An MCP server that provides tools for interacting with the Keyword Insights API.
"""

import os
import json
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


BASE_URL = "https://api.keywordinsights.ai"


class KeywordInsightsClient:
    """HTTP client for the Keyword Insights API."""

    def __init__(self):
        self._token: str | None = None
        self._client = httpx.AsyncClient(base_url=BASE_URL, timeout=60.0)

    async def _ensure_authenticated(self) -> None:
        """Ensure we have a valid auth token."""
        if self._token:
            return

        email = os.environ.get("KEYWORD_INSIGHTS_EMAIL")
        password = os.environ.get("KEYWORD_INSIGHTS_PASSWORD")

        if not email or not password:
            raise ValueError(
                "KEYWORD_INSIGHTS_EMAIL and KEYWORD_INSIGHTS_PASSWORD environment variables must be set"
            )

        await self.login(email, password)

    async def login(self, email: str, password: str) -> dict[str, Any]:
        """Authenticate and get a bearer token."""
        response = await self._client.post(
            "/authentication/login/",
            json={"email": email, "password": password},
        )
        response.raise_for_status()
        data = response.json()
        # Token is nested in result object
        result = data.get("result", data)
        self._token = result.get("access_token")
        return data

    def _headers(self) -> dict[str, str]:
        """Get headers with authorization."""
        return {"Authorization": f"Bearer {self._token}"}

    async def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json_body: dict | None = None,
    ) -> Any:
        """Make an authenticated request."""
        await self._ensure_authenticated()

        response = await self._client.request(
            method,
            path,
            params=params,
            json=json_body,
            headers=self._headers(),
        )

        # Handle 401 by re-authenticating once
        if response.status_code == 401:
            self._token = None
            await self._ensure_authenticated()
            response = await self._client.request(
                method,
                path,
                params=params,
                json=json_body,
                headers=self._headers(),
            )

        response.raise_for_status()

        # Handle binary responses (xlsx)
        if "application/vnd" in response.headers.get("content-type", ""):
            return {"binary": True, "content": response.content}

        return response.json()

    # === User ===
    async def get_user(self) -> dict:
        """Get user data."""
        return await self._request("GET", "/api/user/")

    # === Keyword Ranking ===
    async def create_advanced_ranking_order(
        self,
        keyword: str,
        location: str,
        language: str,
        device: str = "desktop",
        domain: str | None = None,
        include_word_count: bool = False,
    ) -> dict:
        """Create an advanced ranking order for a single keyword."""
        body = {
            "keyword": keyword,
            "location": location,
            "language": language,
            "device": device,
            "include_word_count": include_word_count,
        }
        if domain:
            body["domain"] = domain
        return await self._request("POST", "/api/advanced-ranking/order/", json_body=body)

    async def get_advanced_ranking_order(self, order_id: str) -> dict:
        """Get advanced ranking order status/results."""
        return await self._request("GET", "/api/advanced-ranking/order/", params={"order_id": order_id})

    async def create_advanced_ranking_batch_order(
        self,
        keywords: list[str],
        location: str,
        language: str,
        device: str = "desktop",
        domain: str | None = None,
        include_word_count: bool = False,
    ) -> dict:
        """Create a batch advanced ranking order for multiple keywords."""
        body = {
            "keywords": keywords,
            "location": location,
            "language": language,
            "device": device,
            "include_word_count": include_word_count,
        }
        if domain:
            body["domain"] = domain
        return await self._request("POST", "/api/advanced-ranking/batch/order/", json_body=body)

    async def get_advanced_ranking_batch_order(self, order_id: str) -> dict:
        """Get batch advanced ranking order status/results."""
        return await self._request("GET", "/api/advanced-ranking/batch/order/", params={"order_id": order_id})

    # === Content Brief ===
    async def get_content_brief_languages(self) -> dict:
        """Get supported languages for content briefs."""
        return await self._request("GET", "/api/content-brief/languages/")

    async def create_content_brief(
        self,
        keyword: str,
        language: str,
        location: str,
    ) -> dict:
        """Create a content brief."""
        body = {
            "keyword": keyword,
            "language": language,
            "location": location,
        }
        return await self._request("POST", "/api/content-brief/order/", json_body=body)

    async def get_content_brief(self, brief_id: str) -> dict:
        """Get content brief results."""
        return await self._request("GET", "/api/content-brief/order/", params={"id": brief_id})

    async def list_content_briefs(self) -> dict:
        """List all content briefs."""
        return await self._request("GET", "/api/content-brief/orders/")

    # === Keyword Content ===
    async def create_keyword_content_order(
        self,
        keyword: str,
        language: str,
        location: str,
        content_insights: list[str],
        device: str = "desktop",
    ) -> dict:
        """Create a keyword content order."""
        body = {
            "keyword": keyword,
            "language": language,
            "location": location,
            "content_insights": content_insights,
            "device": device,
        }
        return await self._request("POST", "/api/keyword-content/order/", json_body=body)

    async def get_keyword_content_order(self, order_id: str) -> dict:
        """Get keyword content order status/results."""
        return await self._request("GET", "/api/keyword-content/order/", params={"order_id": order_id})

    # === Keyword Insights ===
    async def get_insights_languages(self) -> dict:
        """Get supported languages for insights."""
        return await self._request("GET", "/api/keywords-insights/languages/")

    async def get_insights_locations(self, limit: int = 20) -> dict:
        """Get available locations (limited to reduce context size). Use search_insights_locations for specific lookups."""
        result = await self._request("GET", "/api/keywords-insights/locations/")
        locations = result.get("result", result) if isinstance(result, dict) else result
        if isinstance(locations, list) and len(locations) > limit:
            return {
                "locations": locations[:limit],
                "total_count": len(locations),
                "truncated": True,
                "hint": f"Showing first {limit} of {len(locations)} locations. Use search_insights_locations to find specific locations by name.",
            }
        return result

    async def search_insights_locations(self, query: str) -> dict:
        """Search for locations by user input."""
        return await self._request("GET", f"/api/keywords-insights/locations-live/{query}/")

    async def create_insights_order(
        self,
        project_name: str,
        keywords: list[str],
        search_volumes: list[int],
        language: str,
        location: str,
        insights: list[str],
        clustering_method: str = "volume",
        grouping_accuracy: int = 3,
        hub_creation_method: str = "medium",
        device: str = "desktop",
        url: str | None = None,
        folder_id: str | None = None,
    ) -> dict:
        """Create a keyword insights order."""
        body = {
            "project_name": project_name,
            "keywords": keywords,
            "search_volumes": search_volumes,
            "language": language,
            "location": location,
            "insights": insights,
            "clustering_method": clustering_method,
            "grouping_accuracy": grouping_accuracy,
            "hub_creation_method": hub_creation_method,
            "device": device,
        }
        if url:
            body["url"] = url
        if folder_id:
            body["folder_id"] = folder_id
        return await self._request("POST", "/api/keywords-insights/order/", json_body=body)

    async def get_insights_order(self, order_id: str) -> dict:
        """Get insights order status/results."""
        return await self._request("GET", "/api/keywords-insights/order/", params={"order_id": order_id})

    async def get_insights_order_cost(self, n_keywords: int, insights: list[str]) -> dict:
        """Estimate the cost of an insights order."""
        params = {
            "n_keywords": n_keywords,
            "insights": insights,
        }
        return await self._request("GET", "/api/keywords-insights/order/cost/", params=params)

    async def get_insights_order_json(
        self,
        order_id: str,
        page_size: int = 50,
        page_number: int = 1,
        sort_by: str = "search_volume",
        ascending: bool = False,
    ) -> dict:
        """Get clustered keyword data for an order with pagination."""
        params = {
            "page_size": page_size,
            "page_number": page_number,
            "sort_by": sort_by,
            "ascending": ascending,
        }
        return await self._request("GET", f"/api/keywords-insights/order/json/{order_id}/", params=params)

    async def export_insights_order_xlsx(self, order_id: str) -> dict:
        """Export insights order to xlsx."""
        return await self._request("GET", f"/api/keywords-insights/order/xlsx/{order_id}/")

    async def list_insights_orders(self, n_orders: int | None = None, n_days: int | None = None) -> dict:
        """List insights orders. Must specify either n_orders or n_days."""
        params = {}
        if n_orders is not None:
            params["n_orders"] = n_orders
        if n_days is not None:
            params["n_days"] = n_days
        if not params:
            params["n_orders"] = 10  # Default to last 10 orders
        return await self._request("GET", "/api/keywords-insights/orders/", params=params)

    # === Writer Agent ===
    async def get_writer_agent_options(self) -> dict:
        """Get writer agent options."""
        return await self._request("GET", "/api/writer-agent/options/")

    async def create_writer_agent_order(
        self,
        keyword: str,
        language_code: str = "en",
        location_name: str = "United States",
        content_type: str = "article",
        point_of_view: str | None = None,
        folder_id: str | None = None,
        additional_insights: str | None = None,
    ) -> dict:
        """Create a writer agent order."""
        body = {
            "keyword": keyword,
            "language_code": language_code,
            "location_name": location_name,
            "content_type": content_type,
        }
        if point_of_view:
            body["point_of_view"] = point_of_view
        if folder_id:
            body["folder_id"] = folder_id
        if additional_insights:
            body["additional_insights"] = additional_insights
        return await self._request("POST", "/api/writer-agent/order/", json_body=body)

    async def get_writer_agent_order(self, order_id: str) -> dict:
        """Get writer agent order results."""
        return await self._request("GET", "/api/writer-agent/order/", params={"id": order_id})

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()


# Create global client instance
client = KeywordInsightsClient()

# Create MCP server
server = Server("keyword-insights")


def _clean_value(value: Any) -> Any:
    """Recursively clean a value, removing empty/null entries."""
    if isinstance(value, dict):
        cleaned = {}
        for k, v in value.items():
            cleaned_v = _clean_value(v)
            # Keep the value if it's not empty/null
            if cleaned_v is not None and cleaned_v != "" and cleaned_v != [] and cleaned_v != {}:
                cleaned[k] = cleaned_v
        return cleaned if cleaned else None
    elif isinstance(value, list):
        cleaned = [_clean_value(item) for item in value]
        cleaned = [item for item in cleaned if item is not None and item != "" and item != [] and item != {}]
        return cleaned if cleaned else None
    else:
        return value


def _json_response(data: Any, clean: bool = True) -> list[TextContent]:
    """Format a JSON response, optionally cleaning empty values."""
    if clean:
        data = _clean_value(data)
    # No indent to save space
    return [TextContent(type="text", text=json.dumps(data, separators=(",", ":")))]


def _error_response(error: Exception) -> list[TextContent]:
    """Format an error response."""
    return [TextContent(type="text", text=f"Error: {str(error)}")]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        # User
        Tool(
            name="get_user",
            description="Get the current user's account data and subscription information",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        # Keyword Ranking
        Tool(
            name="create_advanced_ranking_order",
            description="Create an advanced ranking report for a single keyword. Returns top ranking URLs and optionally word counts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "The keyword to analyze"},
                    "location": {"type": "string", "description": "Target location (e.g., 'United States')"},
                    "language": {"type": "string", "description": "Target language (e.g., 'en')"},
                    "device": {"type": "string", "enum": ["desktop", "mobile"], "default": "desktop"},
                    "domain": {"type": "string", "description": "Optional domain to track"},
                    "include_word_count": {"type": "boolean", "default": False},
                },
                "required": ["keyword", "location", "language"],
            },
        ),
        Tool(
            name="get_advanced_ranking_order",
            description="Check the status of an advanced ranking order and get results when ready",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID to check"},
                },
                "required": ["order_id"],
            },
        ),
        Tool(
            name="create_advanced_ranking_batch_order",
            description="Create a batch advanced ranking report for multiple keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "List of keywords to analyze"},
                    "location": {"type": "string", "description": "Target location"},
                    "language": {"type": "string", "description": "Target language"},
                    "device": {"type": "string", "enum": ["desktop", "mobile"], "default": "desktop"},
                    "domain": {"type": "string", "description": "Optional domain to track"},
                    "include_word_count": {"type": "boolean", "default": False},
                },
                "required": ["keywords", "location", "language"],
            },
        ),
        Tool(
            name="get_advanced_ranking_batch_order",
            description="Check the status of a batch advanced ranking order and get results when ready",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The batch order ID to check"},
                },
                "required": ["order_id"],
            },
        ),
        # Content Brief
        Tool(
            name="get_content_brief_languages",
            description="Get the list of languages supported for content briefs",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="create_content_brief",
            description="Create a content brief for a topic. Analyzes top SERP results to provide content structure recommendations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "The topic/keyword to create a brief for"},
                    "language": {"type": "string", "description": "Language code (e.g., 'en')"},
                    "location": {"type": "string", "description": "Target location (e.g., 'United States')"},
                },
                "required": ["keyword", "language", "location"],
            },
        ),
        Tool(
            name="get_content_brief",
            description="Get the results of a content brief order",
            inputSchema={
                "type": "object",
                "properties": {
                    "brief_id": {"type": "string", "description": "The content brief ID (returned from create_content_brief)"},
                },
                "required": ["brief_id"],
            },
        ),
        Tool(
            name="list_content_briefs",
            description="List all content briefs for your account",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        # Keyword Content
        Tool(
            name="create_keyword_content_order",
            description="Extract content insights for a keyword (PAA questions, Reddit/Quora questions, meta titles/descriptions)",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "The keyword to analyze"},
                    "language": {"type": "string", "description": "Language code (e.g., 'en')"},
                    "location": {"type": "string", "description": "Target location (e.g., 'United States')"},
                    "content_insights": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["paa", "reddit_questions", "quora_questions", "meta_titles", "meta_descriptions"]},
                        "description": "Types of content to extract. Costs: paa/reddit/quora=50 credits, meta_titles/descriptions=200 credits each",
                    },
                    "device": {"type": "string", "enum": ["desktop", "mobile"], "description": "Device type (default: desktop)", "default": "desktop"},
                },
                "required": ["keyword", "language", "location", "content_insights"],
            },
        ),
        Tool(
            name="get_keyword_content_order",
            description="Get the status/results of a keyword content order",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The keyword content order ID"},
                },
                "required": ["order_id"],
            },
        ),
        # Keyword Insights
        Tool(
            name="get_insights_languages",
            description="Get the list of languages supported for keyword insights",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="get_insights_locations",
            description="Get available locations for keyword insights orders (returns first 20 by default). Use search_insights_locations to find specific locations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Max locations to return (default: 20)", "default": 20},
                },
                "required": [],
            },
        ),
        Tool(
            name="search_insights_locations",
            description="Search for locations by name (useful for dynamic UI)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Location search query"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="create_insights_order",
            description="Create a keyword insights/clustering order. Groups keywords by search intent and topic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Name for this project/order"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "List of keywords to cluster"},
                    "search_volumes": {"type": "array", "items": {"type": "integer"}, "description": "Search volumes for each keyword (same order as keywords)"},
                    "language": {"type": "string", "description": "Language code (e.g., 'en')"},
                    "location": {"type": "string", "description": "Target location (e.g., 'United States')"},
                    "insights": {"type": "array", "items": {"type": "string", "enum": ["cluster", "context", "rank", "title_ai"]}, "description": "Analysis types to run"},
                    "clustering_method": {"type": "string", "enum": ["volume", "agglomerative"], "description": "Clustering algorithm (default: volume)", "default": "volume"},
                    "grouping_accuracy": {"type": "integer", "minimum": 1, "maximum": 7, "description": "SERP overlap threshold 1-7 (default: 3)", "default": 3},
                    "hub_creation_method": {"type": "string", "enum": ["soft", "medium", "hard"], "description": "Hub similarity level (default: medium)", "default": "medium"},
                    "device": {"type": "string", "enum": ["desktop", "tablet", "mobile"], "description": "Device type (default: desktop)", "default": "desktop"},
                    "url": {"type": "string", "description": "Domain URL (required if 'rank' insight selected)"},
                    "folder_id": {"type": "string", "description": "Optional folder ID for organization"},
                },
                "required": ["project_name", "keywords", "search_volumes", "language", "location", "insights"],
            },
        ),
        Tool(
            name="get_insights_order",
            description="Check the status of a keyword insights order and get results when ready",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The insights order ID"},
                },
                "required": ["order_id"],
            },
        ),
        Tool(
            name="get_insights_order_cost",
            description="Estimate the credit cost of a keyword insights order before creating it",
            inputSchema={
                "type": "object",
                "properties": {
                    "n_keywords": {"type": "integer", "description": "Number of keywords to process"},
                    "insights": {"type": "array", "items": {"type": "string", "enum": ["cluster", "context", "rank", "title_ai"]}, "description": "Analysis types to run"},
                },
                "required": ["n_keywords", "insights"],
            },
        ),
        Tool(
            name="get_insights_order_json",
            description="Get the clustered keyword data for an insights order as JSON with pagination. Returns clusters sorted by search volume by default.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The insights order ID"},
                    "page_size": {"type": "integer", "description": "Results per page (default: 50, max: 1000)", "default": 50},
                    "page_number": {"type": "integer", "description": "Page number (default: 1)", "default": 1},
                    "sort_by": {"type": "string", "description": "Sort field (default: search_volume)", "default": "search_volume"},
                    "ascending": {"type": "boolean", "description": "Sort ascending (default: false)", "default": False},
                },
                "required": ["order_id"],
            },
        ),
        Tool(
            name="export_insights_order_xlsx",
            description="Export an insights order to an Excel file",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The insights order ID"},
                    "output_path": {"type": "string", "description": "Path to save the xlsx file"},
                },
                "required": ["order_id", "output_path"],
            },
        ),
        Tool(
            name="list_insights_orders",
            description="List keyword insights orders for your account. Specify n_orders OR n_days.",
            inputSchema={
                "type": "object",
                "properties": {
                    "n_orders": {"type": "integer", "description": "Number of recent orders to return (default: 10)"},
                    "n_days": {"type": "integer", "description": "Return orders from the last N days"},
                },
                "required": [],
            },
        ),
        # Writer Agent
        Tool(
            name="get_writer_agent_options",
            description="Get available options for the writer agent",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="create_writer_agent_order",
            description="Create a writer agent order to generate AI content (article outline, plan, and full article)",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "The topic/keyword to write about"},
                    "language_code": {"type": "string", "description": "ISO 639-1 language code (default: 'en')", "default": "en"},
                    "location_name": {"type": "string", "description": "Target location (default: 'United States')", "default": "United States"},
                    "content_type": {"type": "string", "enum": ["article", "landing_page"], "description": "Type of content (default: article)", "default": "article"},
                    "point_of_view": {"type": "string", "enum": ["First person", "Second Person", "Third Person"], "description": "Narrative perspective"},
                    "folder_id": {"type": "string", "description": "Optional folder ID for organization"},
                    "additional_insights": {"type": "string", "description": "Custom instructions or context for the writer"},
                },
                "required": ["keyword"],
            },
        ),
        Tool(
            name="get_writer_agent_order",
            description="Get the results of a writer agent order",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The writer agent order ID"},
                },
                "required": ["order_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        # User
        if name == "get_user":
            result = await client.get_user()
            return _json_response(result)

        # Keyword Ranking
        elif name == "create_advanced_ranking_order":
            result = await client.create_advanced_ranking_order(
                keyword=arguments["keyword"],
                location=arguments["location"],
                language=arguments["language"],
                device=arguments.get("device", "desktop"),
                domain=arguments.get("domain"),
                include_word_count=arguments.get("include_word_count", False),
            )
            return _json_response(result)

        elif name == "get_advanced_ranking_order":
            result = await client.get_advanced_ranking_order(arguments["order_id"])
            return _json_response(result)

        elif name == "create_advanced_ranking_batch_order":
            result = await client.create_advanced_ranking_batch_order(
                keywords=arguments["keywords"],
                location=arguments["location"],
                language=arguments["language"],
                device=arguments.get("device", "desktop"),
                domain=arguments.get("domain"),
                include_word_count=arguments.get("include_word_count", False),
            )
            return _json_response(result)

        elif name == "get_advanced_ranking_batch_order":
            result = await client.get_advanced_ranking_batch_order(arguments["order_id"])
            return _json_response(result)

        # Content Brief
        elif name == "get_content_brief_languages":
            result = await client.get_content_brief_languages()
            return _json_response(result)

        elif name == "create_content_brief":
            result = await client.create_content_brief(
                keyword=arguments["keyword"],
                language=arguments["language"],
                location=arguments["location"],
            )
            return _json_response(result)

        elif name == "get_content_brief":
            result = await client.get_content_brief(arguments["brief_id"])
            return _json_response(result)

        elif name == "list_content_briefs":
            result = await client.list_content_briefs()
            return _json_response(result)

        # Keyword Content
        elif name == "create_keyword_content_order":
            result = await client.create_keyword_content_order(
                keyword=arguments["keyword"],
                language=arguments["language"],
                location=arguments["location"],
                content_insights=arguments["content_insights"],
                device=arguments.get("device", "desktop"),
            )
            return _json_response(result)

        elif name == "get_keyword_content_order":
            result = await client.get_keyword_content_order(arguments["order_id"])
            return _json_response(result)

        # Keyword Insights
        elif name == "get_insights_languages":
            result = await client.get_insights_languages()
            return _json_response(result)

        elif name == "get_insights_locations":
            result = await client.get_insights_locations(limit=arguments.get("limit", 20))
            return _json_response(result)

        elif name == "search_insights_locations":
            result = await client.search_insights_locations(arguments["query"])
            return _json_response(result)

        elif name == "create_insights_order":
            result = await client.create_insights_order(
                project_name=arguments["project_name"],
                keywords=arguments["keywords"],
                search_volumes=arguments["search_volumes"],
                language=arguments["language"],
                location=arguments["location"],
                insights=arguments["insights"],
                clustering_method=arguments.get("clustering_method", "volume"),
                grouping_accuracy=arguments.get("grouping_accuracy", 3),
                hub_creation_method=arguments.get("hub_creation_method", "medium"),
                device=arguments.get("device", "desktop"),
                url=arguments.get("url"),
                folder_id=arguments.get("folder_id"),
            )
            return _json_response(result)

        elif name == "get_insights_order":
            result = await client.get_insights_order(arguments["order_id"])
            return _json_response(result)

        elif name == "get_insights_order_cost":
            result = await client.get_insights_order_cost(
                n_keywords=arguments["n_keywords"],
                insights=arguments["insights"],
            )
            return _json_response(result)

        elif name == "get_insights_order_json":
            result = await client.get_insights_order_json(
                order_id=arguments["order_id"],
                page_size=arguments.get("page_size", 50),
                page_number=arguments.get("page_number", 1),
                sort_by=arguments.get("sort_by", "search_volume"),
                ascending=arguments.get("ascending", False),
            )
            return _json_response(result)

        elif name == "export_insights_order_xlsx":
            result = await client.export_insights_order_xlsx(arguments["order_id"])
            if result.get("binary"):
                output_path = arguments["output_path"]
                with open(output_path, "wb") as f:
                    f.write(result["content"])
                return _json_response({"success": True, "path": output_path})
            return _json_response(result)

        elif name == "list_insights_orders":
            result = await client.list_insights_orders(
                n_orders=arguments.get("n_orders"),
                n_days=arguments.get("n_days"),
            )
            return _json_response(result)

        # Writer Agent
        elif name == "get_writer_agent_options":
            result = await client.get_writer_agent_options()
            return _json_response(result)

        elif name == "create_writer_agent_order":
            result = await client.create_writer_agent_order(
                keyword=arguments["keyword"],
                language_code=arguments.get("language_code", "en"),
                location_name=arguments.get("location_name", "United States"),
                content_type=arguments.get("content_type", "article"),
                point_of_view=arguments.get("point_of_view"),
                folder_id=arguments.get("folder_id"),
                additional_insights=arguments.get("additional_insights"),
            )
            return _json_response(result)

        elif name == "get_writer_agent_order":
            result = await client.get_writer_agent_order(arguments["order_id"])
            return _json_response(result)

        else:
            return _error_response(ValueError(f"Unknown tool: {name}"))

    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if e.response else str(e)
        return _error_response(Exception(f"HTTP {e.response.status_code}: {error_detail}"))
    except Exception as e:
        return _error_response(e)


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Entry point."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
