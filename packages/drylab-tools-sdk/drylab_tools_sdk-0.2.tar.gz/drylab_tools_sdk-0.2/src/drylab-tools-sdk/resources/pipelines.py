"""Pipeline registry operations."""

from typing import Optional, List, Dict, Any

from drylab_tools_sdk.resources.base import BaseResource
from drylab_tools_sdk.models.pipeline import Pipeline, PipelineSchema, SchemaField


class PipelinesResource(BaseResource):
    """
    Pipeline registry operations.

    List available pipelines, get parameter schemas, and register custom pipelines.

    Example:
        # List available pipelines
        pipelines = client.pipelines.list()
        for p in pipelines:
            print(f"{p.name}: {p.description}")

        # Get schema to understand required parameters
        schema = client.pipelines.get_schema("rnaseq")
        for field in schema.fields:
            if field.required:
                print(f"Required: {field.name} ({field.type})")
    """

    def list(
        self,
        include_public: bool = True,
        include_user: bool = True,
        project_id: Optional[str] = None,
    ) -> List[Pipeline]:
        """
        List available pipelines.

        Args:
            include_public: Include public nf-core pipelines
            include_user: Include user-uploaded pipelines
            project_id: Filter user pipelines by project

        Returns:
            List of Pipeline objects

        Example:
            pipelines = client.pipelines.list()
            for p in pipelines:
                print(f"{p.id}: {p.name} ({p.source})")
        """
        response = self._http.post(
            "/api/v1/ai/nextflow/pipelines/list",
            json={
                "include_public": include_public,
                "include_user": include_user,
                "project_id": project_id,
            },
        )

        return [Pipeline.from_response(p) for p in response]

    def get(self, pipeline_id: str) -> Pipeline:
        """
        Get details for a specific pipeline.

        Args:
            pipeline_id: Pipeline ID (e.g., "rnaseq" or "user-{uuid}")

        Returns:
            Pipeline object

        Example:
            pipeline = client.pipelines.get("rnaseq")
            print(f"Name: {pipeline.name}")
            print(f"Description: {pipeline.description}")
        """
        response = self._http.post(
            f"/api/v1/ai/nextflow/pipelines/{pipeline_id}/get",
            json={},
        )

        return Pipeline.from_response(response)

    def get_schema(
        self,
        pipeline_id: str,
        version: Optional[str] = None,
    ) -> PipelineSchema:
        """
        Get the parameter schema for a pipeline.

        The schema describes all available parameters, their types,
        whether they're required, and which ones are file paths.

        Args:
            pipeline_id: Pipeline ID
            version: Pipeline version (optional)

        Returns:
            PipelineSchema with field definitions

        Example:
            schema = client.pipelines.get_schema("rnaseq")

            # Find required parameters
            required = [f for f in schema.fields if f.required]
            print("Required parameters:")
            for f in required:
                print(f"  {f.name}: {f.type} - {f.description}")

            # Find path parameters (need vault paths)
            path_params = schema.path_fields
            print(f"Path parameters: {path_params}")
        """
        response = self._http.post(
            f"/api/v1/ai/nextflow/pipelines/{pipeline_id}/schema",
            json={"version": version},
        )

        return PipelineSchema(
            pipeline_id=response.get("pipeline_id", pipeline_id),
            fields=[
                SchemaField(
                    name=f["name"],
                    type=f["type"],
                    is_path=f.get("is_path", False),
                    required=f.get("required", False),
                    description=f.get("description", ""),
                    default=f.get("default"),
                )
                for f in response.get("fields", [])
            ],
            path_fields=response.get("path_fields", []),
        )

    def register(
        self,
        name: str,
        pipeline_zip_path: str,
        schema: Dict[str, Any],
        description: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Pipeline:
        """
        Register a custom Nextflow pipeline.

        The pipeline zip should contain:
        - main.nf: Main Nextflow script
        - nextflow.config: Pipeline configuration
        - Any additional modules/scripts

        Args:
            name: Name for the pipeline
            pipeline_zip_path: Vault path to pipeline zip
            schema: Parameter schema - minimal format with just path_fields, or full format
            description: Pipeline description
            project_id: Associate with project

        Returns:
            Registered Pipeline object

        Example (minimal schema - recommended):
            pipeline = client.pipelines.register(
                name="my-custom-analysis",
                pipeline_zip_path="/MyProject/pipelines/analysis.zip",
                schema={
                    "path_fields": ["input_file", "outdir", "reference"]
                },
                description="Custom analysis pipeline"
            )

        Example (full schema - optional):
            pipeline = client.pipelines.register(
                name="my-custom-analysis",
                pipeline_zip_path="/MyProject/pipelines/analysis.zip",
                schema={
                    "path_fields": ["input_file", "outdir"],
                    "fields": [
                        {"name": "input_file", "type": "path", "required": True},
                        {"name": "outdir", "type": "path", "required": True},
                        {"name": "threads", "type": "integer", "default": 4}
                    ]
                },
                description="Custom analysis pipeline"
            )
        """
        response = self._http.post(
            "/api/v1/ai/nextflow/pipelines/register",
            json={
                "pipeline_name": name,
                "pipeline_zip_vault_path": pipeline_zip_path,
                "schema_json": schema,
                "description": description,
                "project_id": project_id,
            },
        )

        return Pipeline.from_response(response)

    def delete(self, pipeline_id: str) -> bool:
        """
        Delete a user-uploaded pipeline.

        Only user pipelines (prefixed with "user-") can be deleted.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            True if deleted

        Example:
            client.pipelines.delete("user-550e8400-e29b-41d4-a716-446655440000")
        """
        self._http.post(
            f"/api/v1/ai/nextflow/pipelines/{pipeline_id}/delete",
            json={},
        )
        return True
