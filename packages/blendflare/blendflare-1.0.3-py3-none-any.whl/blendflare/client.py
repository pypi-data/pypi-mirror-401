"""Main client for the Blendflare API."""

import time
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import requests

from .exceptions import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    BlendflareError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from .models import DownloadResponse, SearchResponse
from .types import (
    Category,
    Feature,
    GameEngine,
    LegalFlag,
    LicenseType,
    MaterialType,
    NodeGroupType,
    Physics,
    RenderEngine,
    Simulation,
    SortBy,
    SortOrder,
    Style,
    Subcategory,
    UVMapping,
    join_enum_values,
    parse_tags,
)


class BlendflareClient:
    """Client for interacting with the Blendflare API.
    
    Example:
        >>> from blendflare import BlendflareClient, Category, SortBy
        >>> 
        >>> client = BlendflareClient(api_key="sk_live_your_api_key")
        >>> 
        >>> # Search for projects
        >>> results = client.search_projects(
        ...     q="sports car",
        ...     category=Category.TRANSPORT,
        ...     sort_by=SortBy.POPULAR,
        ...     limit=20
        ... )
        >>> 
        >>> # Download a project
        >>> download = client.download_project(
        ...     project_slug="sign-decal-pack",
        ...     nickname="example_nickname"
        ... )
        >>> print(download.data.download_url)
    """
    
    BASE_URL = "https://api.blendflare.com/v1"
    DEFAULT_TIMEOUT = 30
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> None:
        """Initialize the Blendflare client.
        
        Args:
            api_key: Your Blendflare API key (format: "sk_live_...")
            base_url: Optional custom base URL for the API
            timeout: Request timeout in seconds (default: 30)
        """
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"ApiKey {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "blendflare-python/1.0.3",
        })
        self._consecutive_403_count = 0
        self._last_request_time = 0
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data
        
        Returns:
            Response data as dictionary
        
        Raises:
            BlendflareError: For API errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            
            # Handle different status codes
            if response.status_code == 200:
                self._consecutive_403_count = 0  # Reset on success
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                raise BadRequestError(error_data.get("message", "Bad request"))
            elif response.status_code == 401:
                raise AuthenticationError()
            elif response.status_code == 403:
                error_data = response.json()
                message = error_data.get("Message", error_data.get("message", "Access forbidden"))
                
                # Track consecutive 403s - if we get multiple in short succession, 
                # it's likely rate limiting rather than invalid API key
                import time
                current_time = time.time()
                
                # If less than 5 seconds since last request and we got another 403
                if current_time - self._last_request_time < 5:
                    self._consecutive_403_count += 1
                else:
                    self._consecutive_403_count = 1
                
                self._last_request_time = current_time
                
                # If we've had 3+ consecutive 403s in quick succession, it's rate limiting
                if self._consecutive_403_count >= 3:
                    raise RateLimitError(message)
                
                # Otherwise, it's an authorization error (invalid API key)
                raise AuthorizationError(message)
            elif response.status_code == 404:
                error_data = response.json()
                raise NotFoundError(error_data.get("message", "Resource not found"))
            elif response.status_code == 422:
                error_data = response.json()
                details = None
                if "error" in error_data and "details" in error_data["error"]:
                    details = error_data["error"]["details"]
                raise ValidationError(
                    error_data.get("message", "Validation error"),
                    details=details
                )
            elif response.status_code >= 500:
                raise ServerError()
            else:
                raise APIError(
                    f"Unexpected status code: {response.status_code}",
                    status_code=response.status_code
                )
        
        except requests.exceptions.Timeout:
            raise TimeoutError()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
    
    def search_projects(
        self,
        # Basic Search
        q: Optional[str] = None,
        category: Optional[Union[Category, str]] = None,
        subcategory: Optional[Union[Subcategory, str]] = None,
        style: Optional[Union[Style, str]] = None,
        is_kit: Optional[bool] = None,
        tags: Optional[Union[List[str], str]] = None,
        # Technical Specifications
        render_engine: Optional[Union[RenderEngine, str]] = None,
        blender_version: Optional[str] = None,
        materials: Optional[Union[MaterialType, str]] = None,
        uv_mapping: Optional[Union[UVMapping, str]] = None,
        # Features
        features: Optional[Union[List[Feature], str]] = None,
        simulations: Optional[Union[List[Simulation], str]] = None,
        node_groups: Optional[Union[List[NodeGroupType], str]] = None,
        physics: Optional[Union[List[Physics], str]] = None,
        game_engines: Optional[Union[List[GameEngine], str]] = None,
        # Counts and Size
        min_poly_count: Optional[int] = None,
        max_poly_count: Optional[int] = None,
        min_vertex_count: Optional[int] = None,
        max_vertex_count: Optional[int] = None,
        min_file_size: Optional[int] = None,
        max_file_size: Optional[int] = None,
        # Stats Filters
        min_downloads: Optional[int] = None,
        min_likes: Optional[int] = None,
        min_views: Optional[int] = None,
        min_bookmarks: Optional[int] = None,
        # Author and Licensing
        author: Optional[str] = None,
        license_type: Optional[Union[LicenseType, str]] = None,
        legal: Optional[Union[List[LegalFlag], str]] = None,
        # Sorting
        sort_by: Optional[Union[SortBy, str]] = None,
        sort_order: Optional[Union[SortOrder, str]] = None,
        # Pagination
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> SearchResponse:
        """Search for projects in the Blendflare library.
        
        Args:
            q: Search query keywords
            category: Main category filter
            subcategory: Subcategory filter (specific to category)
            style: Visual style of the asset
            is_kit: Filter for asset kits/collections
            tags: Tags filter (list or + separated string)
            render_engine: Blender render engine
            blender_version: Blender version compatibility (e.g., "4.4")
            materials: Material type
            uv_mapping: UV mapping type
            features: Asset features (list or + separated string)
            simulations: Physics simulations (list or + separated string)
            node_groups: Node group types (list or + separated string)
            physics: Physics features (list or + separated string)
            game_engines: Game engine compatibility (list or + separated string)
            min_poly_count: Minimum polygon count
            max_poly_count: Maximum polygon count
            min_vertex_count: Minimum vertex count
            max_vertex_count: Maximum vertex count
            min_file_size: Minimum file size in bytes
            max_file_size: Maximum file size in bytes
            min_downloads: Minimum download count
            min_likes: Minimum likes count
            min_views: Minimum views count
            min_bookmarks: Minimum bookmarks count
            author: Filter by creator username
            license_type: License type
            legal: Legal flags (list or + separated string)
            sort_by: Sort field
            sort_order: Sort direction
            page: Page number (default: 1)
            limit: Results per page, max 100 (default: 10)
        
        Returns:
            SearchResponse containing search results and metadata
        
        Example:
            >>> from blendflare import BlendflareClient, Category, Feature, SortBy
            >>> 
            >>> client = BlendflareClient(api_key="your_api_key")
            >>> results = client.search_projects(
            ...     q="car",
            ...     category=Category.TRANSPORT,
            ...     features=[Feature.RIGGED, Feature.ANIMATED],
            ...     sort_by=SortBy.POPULAR,
            ...     limit=20
            ... )
            >>> 
            >>> for project in results.items:
            ...     print(f"{project.project_info.title} by {project.author.nickname}")
        """
        params: Dict[str, Any] = {}
        
        # Basic Search
        if q is not None:
            params["q"] = q
        if category is not None:
            params["category"] = category.value if isinstance(category, Category) else category
        if subcategory is not None:
            params["subcategory"] = subcategory.value if isinstance(subcategory, Subcategory) else subcategory
        if style is not None:
            params["style"] = style.value if isinstance(style, Style) else style
        if is_kit is not None:
            params["is_kit"] = is_kit
        if tags is not None:
            params["tags"] = parse_tags(tags) if isinstance(tags, list) else tags
        
        # Technical Specifications
        if render_engine is not None:
            params["render_engine"] = render_engine.value if isinstance(render_engine, RenderEngine) else render_engine
        if blender_version is not None:
            params["blender_version"] = blender_version
        if materials is not None:
            params["materials"] = materials.value if isinstance(materials, MaterialType) else materials
        if uv_mapping is not None:
            params["uv_mapping"] = uv_mapping.value if isinstance(uv_mapping, UVMapping) else uv_mapping
        
        # Features
        if features is not None:
            params["features"] = join_enum_values(features) if isinstance(features, list) else features
        if simulations is not None:
            params["simulations"] = join_enum_values(simulations) if isinstance(simulations, list) else simulations
        if node_groups is not None:
            params["node_groups"] = join_enum_values(node_groups) if isinstance(node_groups, list) else node_groups
        if physics is not None:
            params["physics"] = join_enum_values(physics) if isinstance(physics, list) else physics
        if game_engines is not None:
            params["game_engines"] = join_enum_values(game_engines) if isinstance(game_engines, list) else game_engines
        
        # Counts and Size
        if min_poly_count is not None:
            params["min_poly_count"] = min_poly_count
        if max_poly_count is not None:
            params["max_poly_count"] = max_poly_count
        if min_vertex_count is not None:
            params["min_vertex_count"] = min_vertex_count
        if max_vertex_count is not None:
            params["max_vertex_count"] = max_vertex_count
        if min_file_size is not None:
            params["min_file_size"] = min_file_size
        if max_file_size is not None:
            params["max_file_size"] = max_file_size
        
        # Stats Filters
        if min_downloads is not None:
            params["min_downloads"] = min_downloads
        if min_likes is not None:
            params["min_likes"] = min_likes
        if min_views is not None:
            params["min_views"] = min_views
        if min_bookmarks is not None:
            params["min_bookmarks"] = min_bookmarks
        
        # Author and Licensing
        if author is not None:
            params["author"] = author
        if license_type is not None:
            params["license_type"] = license_type.value if isinstance(license_type, LicenseType) else license_type
        if legal is not None:
            params["legal"] = join_enum_values(legal) if isinstance(legal, list) else legal
        
        # Sorting
        if sort_by is not None:
            params["sort_by"] = sort_by.value if isinstance(sort_by, SortBy) else sort_by
        if sort_order is not None:
            params["sort_order"] = sort_order.value if isinstance(sort_order, SortOrder) else sort_order
        
        # Pagination
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        
        response_data = self._request("GET", "/search/projects", params=params)
        return SearchResponse.from_dict(response_data)
    
    def download_project(
        self,
        project_slug: str,
        nickname: str,
    ) -> DownloadResponse:
        """Generate a download URL for a project.
        
        Args:
            project_slug: The project slug identifier
            nickname: The author's nickname
        
        Returns:
            DownloadResponse containing download URL and file information
        
        Example:
            >>> client = BlendflareClient(api_key="your_api_key")
            >>> download = client.download_project(
            ...     project_slug="sign-decal-pack",
            ...     nickname="example_nickname"
            ... )
            >>> print(f"Download: {download.data.download_url}")
            >>> print(f"File size: {download.data.file_size_mb:.2f} MB")
            >>> print(f"Expires in: {download.data.expires_in} seconds")
        """
        params = {
            "project_slug": project_slug,
            "nickname": nickname,
        }
        
        response_data = self._request("GET", "/download-project", params=params)
        return DownloadResponse.from_dict(response_data)
    
    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()
    
    def __enter__(self) -> "BlendflareClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()