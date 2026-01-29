"""Job data models."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class JobStatus(str, Enum):
    """Job status values."""

    SUBMITTED = "submitted"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


@dataclass
class Job:
    """Represents a Nextflow job."""

    id: str
    pipeline_id: str
    status: JobStatus
    run_name: Optional[str] = None
    compute_profile: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    progress: Optional[float] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error: Optional[str] = None
    success: Optional[bool] = None
    complete: Optional[bool] = None

    @property
    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self.status in (JobStatus.SUBMITTED, JobStatus.PENDING, JobStatus.RUNNING)

    @property
    def is_complete(self) -> bool:
        """Check if job has finished (success or failure)."""
        return self.complete or self.status in (
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        )

    @property
    def is_success(self) -> bool:
        """Check if job completed successfully."""
        return self.success is True or self.status == JobStatus.COMPLETED

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> "Job":
        """Create Job from API response."""
        status_str = data.get("status", "unknown")
        try:
            status = JobStatus(status_str)
        except ValueError:
            status = JobStatus.UNKNOWN

        return cls(
            id=data.get("job_id", data.get("id", "")),
            pipeline_id=data.get("pipeline_id", ""),
            status=status,
            run_name=data.get("run_name"),
            compute_profile=data.get("compute_profile"),
            params=data.get("params"),
            progress=data.get("progress"),
            start_time=data.get("start"),
            end_time=data.get("complete_time"),
            error=data.get("error_message"),
            success=data.get("success"),
            complete=data.get("complete"),
        )

    def __repr__(self) -> str:
        return f"Job(id={self.id!r}, status={self.status.value!r}, pipeline={self.pipeline_id!r})"
