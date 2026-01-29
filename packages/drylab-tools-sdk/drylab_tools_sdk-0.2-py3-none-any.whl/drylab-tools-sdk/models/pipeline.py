"""Pipeline data models."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class SchemaField:
    """A field in a pipeline parameter schema."""

    name: str
    type: str
    is_path: bool = False
    required: bool = False
    description: str = ""
    default: Any = None

    def __repr__(self) -> str:
        req = " (required)" if self.required else ""
        path = " [path]" if self.is_path else ""
        return f"SchemaField({self.name}: {self.type}{req}{path})"


@dataclass
class PipelineSchema:
    """Parameter schema for a pipeline."""

    pipeline_id: str
    fields: List[SchemaField]
    path_fields: List[str] = field(default_factory=list)

    @property
    def required_fields(self) -> List[SchemaField]:
        """Get required fields."""
        return [f for f in self.fields if f.required]

    @property
    def optional_fields(self) -> List[SchemaField]:
        """Get optional fields."""
        return [f for f in self.fields if not f.required]

    def __repr__(self) -> str:
        return f"PipelineSchema({self.pipeline_id!r}, {len(self.fields)} fields)"


@dataclass
class Pipeline:
    """Represents a Nextflow pipeline."""

    id: str
    name: str
    description: str = ""
    source: str = "registry"  # "registry" or "user-upload"
    path: str = ""
    default_version: str = "main"

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> "Pipeline":
        """Create Pipeline from API response."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", data.get("pipeline_name", "")),
            description=data.get("description", ""),
            source=data.get("source", "registry"),
            path=data.get("path", data.get("pipeline_zip_s3_path", "")),
            default_version=data.get("default_version", "main"),
        )

    def __repr__(self) -> str:
        return f"Pipeline(id={self.id!r}, name={self.name!r})"
