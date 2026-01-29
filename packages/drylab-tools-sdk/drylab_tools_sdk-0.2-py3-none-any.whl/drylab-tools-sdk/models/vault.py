"""Vault data models."""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class VaultFile:
    """Represents a file in the vault."""

    file_id: str
    filename: str
    size: Optional[int] = None
    mime_type: Optional[str] = None
    status: str = "available"
    s3_key: Optional[str] = None
    created_at: Optional[str] = None

    def __repr__(self) -> str:
        size_str = f"{self.size} bytes" if self.size else "unknown size"
        return f"VaultFile({self.filename!r}, {size_str})"


@dataclass
class VaultFolder:
    """Represents a folder in the vault."""

    folder_id: str
    folder_name: str
    description: Optional[str] = None

    def __repr__(self) -> str:
        return f"VaultFolder({self.folder_name!r})"


@dataclass
class UploadResult:
    """Result of an upload request."""

    presigned_url: str
    file_id: str
    s3_key: str

    def __repr__(self) -> str:
        return f"UploadResult(file_id={self.file_id!r})"


@dataclass
class DownloadResult:
    """Result of a download request."""

    url: str
    filename: Optional[str] = None
    file_id: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    file_count: Optional[int] = None  # For folder downloads

    def __repr__(self) -> str:
        return f"DownloadResult(filename={self.filename!r})"


@dataclass
class ListFilesResult:
    """Result of listing files in a folder."""

    folder_id: str
    folder_name: str
    vault_path: str
    files: List[VaultFile]
    subfolders: List[VaultFolder]

    def __repr__(self) -> str:
        lines = [f"{self.vault_path}/"]
        
        # Combine subfolders and files for tree display
        all_items = [(True, sf.folder_name) for sf in self.subfolders] + \
                    [(False, f.filename) for f in self.files]
        
        for i, (is_folder, name) in enumerate(all_items):
            is_last = (i == len(all_items) - 1)
            prefix = "`-- " if is_last else "|-- "
            suffix = "/" if is_folder else ""
            lines.append(f"{prefix}{name}{suffix}")
        
        if not all_items:
            lines.append("    (empty)")
        
        return "\n".join(lines)
