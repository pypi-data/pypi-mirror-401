"""Blendflare Python SDK - Official client for the Blendflare API.

This SDK provides a simple and powerful interface to search and download
3D assets from the Blendflare library.

Example usage:
    >>> from blendflare import BlendflareClient, Category, Feature, SortBy
    >>> 
    >>> # Initialize the client
    >>> client = BlendflareClient(api_key="sk_live_your_api_key")
    >>> 
    >>> # Search for projects
    >>> results = client.search_projects(
    ...     q="sports car",
    ...     category=Category.TRANSPORT,
    ...     features=[Feature.RIGGED, Feature.ANIMATED],
    ...     sort_by=SortBy.POPULAR,
    ...     limit=20
    ... )
    >>> 
    >>> # Display results
    >>> for project in results.items:
    ...     print(f"{project.project_info.title} by {project.author.nickname}")
    ...     print(f"Downloads: {project.stats.downloads_count}")
    >>> 
    >>> # Download a project
    >>> download = client.download_project(
    ...     project_slug=results.items[0].slug,
    ...     nickname=results.items[0].author.nickname
    ... )
    >>> print(f"Download URL: {download.data.download_url}")
"""

__version__ = "1.0.3"
__author__ = "Blendflare"
__email__ = "support@blendflare.com"

# Main client
from .client import BlendflareClient

# Models
from .models import (
    Author,
    BlenderVersion,
    DownloadData,
    DownloadResponse,
    FileInfo,
    LegalInfo,
    Pagination,
    Project,
    ProjectInfo,
    ProjectStats,
    SearchMetadata,
    SearchResponse,
    TechnicalSpecs,
)

# Types and enums
from .types import (
    CATEGORY_SUBCATEGORIES,
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
    get_subcategories,
    get_subcategory_names,
    join_enum_values,
    parse_tags,
)

# Exceptions
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

__all__ = [
    # Version
    "__version__",
    "__author__",
    "__email__",
    # Main client
    "BlendflareClient",
    # Models
    "Author",
    "BlenderVersion",
    "DownloadData",
    "DownloadResponse",
    "FileInfo",
    "LegalInfo",
    "Pagination",
    "Project",
    "ProjectInfo",
    "ProjectStats",
    "SearchMetadata",
    "SearchResponse",
    "TechnicalSpecs",
    # Types
    "CATEGORY_SUBCATEGORIES",
    "Category",
    "Feature",
    "GameEngine",
    "LegalFlag",
    "LicenseType",
    "MaterialType",
    "NodeGroupType",
    "Physics",
    "RenderEngine",
    "Simulation",
    "SortBy",
    "SortOrder",
    "Style",
    "Subcategory",
    "UVMapping",
    "get_subcategories",
    "get_subcategory_names",
    "join_enum_values",
    "parse_tags",
    # Exceptions
    "APIError",
    "AuthenticationError",
    "AuthorizationError",
    "BadRequestError",
    "BlendflareError",
    "ConnectionError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "ValidationError",
]