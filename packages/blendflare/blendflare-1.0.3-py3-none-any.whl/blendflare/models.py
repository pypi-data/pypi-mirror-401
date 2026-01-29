"""Data models for Blendflare API responses."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class BlenderVersion:
    """Blender version information."""
    
    major: int
    minor: int
    patch: int
    full_version: str


@dataclass
class Author:
    """Asset author information."""
    
    nickname: str
    avatar_url: str


@dataclass
class ProjectInfo:
    """Project metadata."""
    
    title: str
    tags: List[str]


@dataclass
class ProjectStats:
    """Project statistics."""
    
    downloads_count: int
    likes_count: int
    views_count: int
    bookmarks_count: int


@dataclass
class TechnicalSpecs:
    """Technical specifications of an asset."""
    
    blender_version: BlenderVersion
    render_engine: str


@dataclass
class FileInfo:
    """File information."""
    
    file_size: int
    poly_count: int
    file_name: str
    
    @property
    def file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size / (1024 * 1024)


@dataclass
class LegalInfo:
    """Legal and licensing information."""
    
    license_type: str
    contains_nsfw: bool
    no_ai_license: bool
    visibility: str


@dataclass
class Project:
    """Complete project/asset information."""
    
    slug: str
    last_updated: datetime
    category: str
    subcategory: str
    preview_image: str
    author: Author
    project_info: ProjectInfo
    stats: ProjectStats
    technical_specs: TechnicalSpecs
    file_info: FileInfo
    legal: LegalInfo
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create a Project instance from API response data."""
        return cls(
            slug=data["slug"],
            last_updated=datetime.fromisoformat(data["last_updated"].replace("Z", "+00:00")),
            category=data["category"],
            subcategory=data["subcategory"],
            preview_image=data["preview_image"],
            author=Author(**data["author"]),
            project_info=ProjectInfo(**data["project_info"]),
            stats=ProjectStats(**data["stats"]),
            technical_specs=TechnicalSpecs(
                blender_version=BlenderVersion(**data["technical_specs"]["blender_version"]),
                render_engine=data["technical_specs"]["render_engine"],
            ),
            file_info=FileInfo(**data["file_info"]),
            legal=LegalInfo(**data["legal"]),
        )


@dataclass
class SearchMetadata:
    """Metadata for search results."""
    
    aggregations: Dict[str, Any]
    query: str
    applied_filters: Dict[str, str]
    meta: Dict[str, Any]
    
    @property
    def search_time_ms(self) -> int:
        """Get search execution time in milliseconds."""
        return self.meta.get("search_time", 0)
    
    @property
    def has_results(self) -> bool:
        """Check if search returned any results."""
        return self.meta.get("has_results", False)
    
    @property
    def result_count(self) -> int:
        """Get number of results in current page."""
        return self.meta.get("result_count", 0)
    
    @property
    def total_filters_applied(self) -> int:
        """Get total number of filters applied."""
        return self.meta.get("total_filters_applied", 0)


@dataclass
class Pagination:
    """Pagination information."""
    
    count: int
    limit: int
    page: int
    total: int
    total_pages: int
    has_next_page: bool
    has_prev_page: bool


@dataclass
class SearchResponse:
    """Search results response."""
    
    message: str
    metadata: SearchMetadata
    items: List[Project]
    pagination: Pagination
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResponse":
        """Create a SearchResponse instance from API response data."""
        return cls(
            message=data["message"],
            metadata=SearchMetadata(**data["metadata"]),
            items=[Project.from_dict(item) for item in data["items"]],
            pagination=Pagination(**data["pagination"]),
        )


@dataclass
class DownloadData:
    """Download information for a project."""
    
    download_url: str
    file_name: str
    file_size: int
    expires_in: int
    is_owner: bool
    
    @property
    def file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size / (1024 * 1024)


@dataclass
class DownloadResponse:
    """Download URL response."""
    
    message: str
    data: DownloadData
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DownloadResponse":
        """Create a DownloadResponse instance from API response data."""
        return cls(
            message=data["message"],
            data=DownloadData(**data["data"]),
        )