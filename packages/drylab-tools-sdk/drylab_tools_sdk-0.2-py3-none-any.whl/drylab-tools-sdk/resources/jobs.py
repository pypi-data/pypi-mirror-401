"""Nextflow job operations."""

import time
from typing import Optional, Dict, Any, List

from drylab_tools_sdk.resources.base import BaseResource
from drylab_tools_sdk.models.job import Job, JobStatus


class JobsResource(BaseResource):
    """
    Nextflow job management operations.

    Submit, monitor, and manage Nextflow pipeline jobs.

    Example:
        # Submit a job
        job = client.jobs.submit(
            pipeline_id="rnaseq",
            params={
                "input": "/MyProject/data/samplesheet.csv",
                "outdir": "/MyProject/results",
                "genome": "GRCh38"
            },
            compute_profile="aws-batch"
        )

        # Check status
        job = client.jobs.get(job.id)
        print(f"Status: {job.status}, Progress: {job.progress}%")

        # Wait for completion
        while not job.is_complete:
            time.sleep(30)
            job = client.jobs.get(job.id)

        if job.is_success:
            print("Job completed successfully!")
    """

    def submit(
        self,
        pipeline_id: str,
        params: Dict[str, Any],
        compute_profile: str = "aws-batch",
        version: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Job:
        """
        Submit a new Nextflow pipeline job.

        Args:
            pipeline_id: Pipeline to run. Can be:
                - Public pipeline ID: "rnaseq", "sarek", "fetchngs"
                - User pipeline: "user-{uuid}"
            params: Pipeline parameters. Path parameters should use vault paths.
            compute_profile: Compute backend:
                - "local": Local execution
                - "aws-batch": AWS Batch (recommended)
                - "google-batch": Google Cloud Batch
            version: Pipeline version (optional, defaults to latest)
            project_id: Associate job with a project (optional)

        Returns:
            Job object with id and initial status

        Example:
            job = client.jobs.submit(
                pipeline_id="rnaseq",
                params={
                    "input": "/MyProject/data/samplesheet.csv",
                    "outdir": "/MyProject/results",
                    "genome": "GRCh38",
                    "aligner": "star_salmon"
                },
                compute_profile="aws-batch"
            )
            print(f"Submitted job: {job.id}")
        """
        response = self._http.post(
            "/api/v1/ai/nextflow/jobs/submit-job",
            json={
                "pipeline_id": pipeline_id,
                "params": params,
                "compute_profile": compute_profile,
                "version": version,
                "project_id": project_id,
            },
        )

        return Job.from_response(response)

    def submit_custom(
        self,
        pipeline_name: str,
        pipeline_zip_path: str,
        schema: Dict[str, Any],
        params: Dict[str, Any],
        compute_profile: str = "aws-batch",
        description: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Job:
        """
        Register a custom pipeline and submit a job in one call.

        Use this when you have a custom Nextflow pipeline zip file
        in the vault and want to run it.

        Args:
            pipeline_name: Name for the pipeline
            pipeline_zip_path: Vault path to pipeline zip file
            schema: Pipeline parameter schema (JSON object)
            params: Pipeline parameters
            compute_profile: Compute backend
            description: Pipeline description (optional)
            project_id: Associate with project (optional)

        Returns:
            Job object

        Example:
            job = client.jobs.submit_custom(
                pipeline_name="my-analysis",
                pipeline_zip_path="/MyProject/pipelines/my-pipeline.zip",
                schema={
                    "fields": [
                        {"name": "input", "type": "string", "is_path": True},
                        {"name": "outdir", "type": "string", "is_path": True}
                    ]
                },
                params={
                    "input": "/MyProject/data/input.csv",
                    "outdir": "/MyProject/results"
                }
            )
        """
        response = self._http.post(
            "/api/v1/ai/nextflow/jobs/submit-custom-job",
            json={
                "pipeline_name": pipeline_name,
                "pipeline_zip_vault_path": pipeline_zip_path,
                "schema_json": schema,
                "params": params,
                "compute_profile": compute_profile,
                "description": description,
                "project_id": project_id,
            },
        )

        return Job.from_response(response)

    def get(self, job_id: str) -> Job:
        """
        Get the current status of a job.

        Args:
            job_id: Job UUID

        Returns:
            Job object with current status

        Example:
            job = client.jobs.get("550e8400-e29b-41d4-a716-446655440000")
            print(f"Status: {job.status}")
            print(f"Progress: {job.progress}%")
            if job.error:
                print(f"Error: {job.error}")
        """
        response = self._http.post(f"/api/v1/ai/nextflow/jobs/{job_id}/get", json={})

        return Job.from_response(response)

    def list(
        self,
        status: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        limit: int = 20,
        ai_only: bool = True,
    ) -> List[Job]:
        """
        List jobs with optional filters.

        Args:
            status: Filter by status ("running", "completed", "failed")
            pipeline_id: Filter by pipeline
            limit: Maximum number of jobs (1-100)
            ai_only: Only show AI-submitted jobs (default: True)

        Returns:
            List of Job objects

        Example:
            # List running jobs
            running = client.jobs.list(status="running")

            # List all jobs for a pipeline
            jobs = client.jobs.list(pipeline_id="rnaseq", limit=50)
        """
        response = self._http.post(
            "/api/v1/ai/nextflow/jobs/list",
            json={
                "status": status,
                "pipeline_id": pipeline_id,
                "limit": limit,
                "ai_only": ai_only,
            },
        )

        return [Job.from_response(j) for j in response.get("jobs", [])]

    def cancel(self, job_id: str) -> bool:
        """
        Cancel a running job.

        Args:
            job_id: Job UUID

        Returns:
            True if cancellation was initiated

        Example:
            client.jobs.cancel(job.id)
        """
        self._http.post(f"/api/v1/ai/nextflow/jobs/{job_id}/cancel", json={})
        return True

    def delete(self, job_id: str) -> bool:
        """
        Delete a job record.

        Args:
            job_id: Job UUID

        Returns:
            True if deleted

        Example:
            client.jobs.delete(job.id)
        """
        self._http.post(f"/api/v1/ai/nextflow/jobs/{job_id}/delete", json={})
        return True

    def wait_for_completion(
        self,
        job_id: str,
        poll_interval: int = 30,
        timeout: Optional[int] = None,
    ) -> Job:
        """
        Wait for a job to complete.

        Args:
            job_id: Job UUID
            poll_interval: Seconds between status checks (default: 30)
            timeout: Maximum seconds to wait (optional)

        Returns:
            Job object with final status

        Raises:
            TimeoutError: If timeout is reached before completion

        Example:
            job = client.jobs.submit(...)
            final_job = client.jobs.wait_for_completion(job.id, timeout=3600)
            if final_job.is_success:
                print("Job completed!")
        """
        start_time = time.time()

        while True:
            job = self.get(job_id)

            if job.is_complete:
                return job

            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Job {job_id} did not complete within {timeout}s")

            time.sleep(poll_interval)
