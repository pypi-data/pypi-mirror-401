"""Vault file operations."""

import os
from typing import Optional

import requests

from drylab_tools_sdk.resources.base import BaseResource
from drylab_tools_sdk.models.vault import (
    VaultFile,
    VaultFolder,
    UploadResult,
    DownloadResult,
    ListFilesResult,
)


class VaultResource(BaseResource):
    """
    Vault file storage operations.

    Provides methods to upload, download, and list files in the Drylab vault.
    Files are organized in a hierarchical structure: /ProjectName/Folder/SubFolder/file.txt

    Example:
        # List files in a folder
        result = client.vault.list("/MyProject/data")
        for file in result.files:
            print(file.filename)

        # Upload a file
        upload = client.vault.upload("/MyProject/output", "result.csv", size=1024)
        with open("result.csv", "rb") as f:
            requests.put(upload.presigned_url, data=f)

        # Download a file
        download = client.vault.download("/MyProject/data/input.fastq")
        response = requests.get(download.url)
    """

    def list(self, vault_path: str) -> ListFilesResult:
        """
        List files and subfolders at the given path.

        Args:
            vault_path: Path to folder, e.g., "/ProjectName/Folder"

        Returns:
            ListFilesResult with files and subfolders

        Example:
            result = client.vault.list("/MyProject/data")
            print(f"Found {len(result.files)} files")
            for file in result.files:
                print(f"  {file.filename} ({file.size} bytes)")
        """
        response = self._http.post("/api/v1/ai/vault/files/list", json={"vault_path": vault_path})

        return ListFilesResult(
            folder_id=response["folder_id"],
            folder_name=response["folder_name"],
            vault_path=response["vault_path"],
            files=[
                VaultFile(
                    file_id=f["file_id"],
                    filename=f["filename"],
                    size=f.get("file_size"),
                    mime_type=f.get("mime_type"),
                    status=f.get("status", "available"),
                    s3_key=f.get("s3_key"),
                    created_at=f.get("created_at"),
                )
                for f in response.get("files", [])
            ],
            subfolders=[
                VaultFolder(
                    folder_id=f["folder_id"],
                    folder_name=f["folder_name"],
                    description=f.get("description"),
                )
                for f in response.get("subfolders", [])
            ],
        )

    def upload(
        self,
        vault_path: str,
        filename: str,
        size: int,
    ) -> UploadResult:
        """
        Get a presigned URL to upload a file.

        The returned URL can be used with a PUT request to upload the file directly to S3.
        Folders in the path will be created automatically if they don't exist.

        Args:
            vault_path: Destination folder path, e.g., "/ProjectName/output"
            filename: Name for the uploaded file
            size: File size in bytes

        Returns:
            UploadResult with presigned_url, file_id, and s3_key

        Example:
            upload = client.vault.upload("/MyProject/output", "result.csv", size=1024)

            # Upload the file
            with open("result.csv", "rb") as f:
                response = requests.put(upload.presigned_url, data=f)

            print(f"Uploaded as file_id: {upload.file_id}")
        """
        response = self._http.post(
            "/api/v1/ai/vault/files/presigned-url",
            json={
                "vault_path": vault_path,
                "filename": filename,
                "file_size": size,
            },
        )

        return UploadResult(
            presigned_url=response["presigned_url"],
            file_id=response["file_id"],
            s3_key=response["key"],
        )

    def upload_file(
        self,
        vault_path: str,
        local_path: str,
        filename: Optional[str] = None,
    ) -> UploadResult:
        """
        Upload a local file to the vault (convenience method).

        This combines getting a presigned URL and uploading the file.

        Args:
            vault_path: Destination folder path, e.g., "/ProjectName/output"
            local_path: Path to the local file to upload
            filename: Optional name for the uploaded file (defaults to local filename)

        Returns:
            UploadResult with file_id

        Example:
            result = client.vault.upload_file(
                "/MyProject/output",
                "/tmp/analysis_result.csv"
            )
            print(f"Uploaded as: {result.file_id}")
        """
        if filename is None:
            filename = os.path.basename(local_path)

        file_size = os.path.getsize(local_path)

        # Get presigned URL
        upload = self.upload(vault_path, filename, file_size)

        # Upload the file
        with open(local_path, "rb") as f:
            response = requests.put(
                upload.presigned_url,
                data=f,
                headers={"Content-Type": "application/octet-stream"},
            )
            response.raise_for_status()

        return upload

    def download(
        self,
        vault_path: Optional[str] = None,
        file_id: Optional[str] = None,
    ) -> DownloadResult:
        """
        Get a presigned URL to download a file.

        Provide either vault_path OR file_id.

        Args:
            vault_path: Full path to file, e.g., "/ProjectName/data/file.txt"
            file_id: UUID of the file

        Returns:
            DownloadResult with url and metadata

        Example:
            download = client.vault.download("/MyProject/data/input.fastq")
            response = requests.get(download.url)
            with open("input.fastq", "wb") as f:
                f.write(response.content)
        """
        if not vault_path and not file_id:
            raise ValueError("Either vault_path or file_id is required")

        response = self._http.post(
            "/api/v1/ai/vault/files/download-url",
            json={
                "vault_path": vault_path,
                "file_id": file_id,
            },
        )

        return DownloadResult(
            url=response["download_url"],
            file_id=response["file_id"],
            filename=response["filename"],
            size=response.get("file_size"),
            mime_type=response.get("mime_type"),
        )

    def download_file(
        self,
        local_path: str,
        vault_path: Optional[str] = None,
        file_id: Optional[str] = None,
    ) -> str:
        """
        Download a file to local filesystem (convenience method).

        Args:
            local_path: Where to save the file locally
            vault_path: Full path to file in vault
            file_id: UUID of the file

        Returns:
            Local path where file was saved

        Example:
            path = client.vault.download_file(
                "/tmp/input.fastq",
                vault_path="/MyProject/data/input.fastq"
            )
        """
        download = self.download(vault_path=vault_path, file_id=file_id)

        response = requests.get(download.url, stream=True)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return local_path

    def download_folder(
        self,
        vault_path: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> DownloadResult:
        """
        Download a folder as a zip file.

        Args:
            vault_path: Path to folder, e.g., "/ProjectName/results"
            folder_id: UUID of the folder

        Returns:
            DownloadResult with URL to download the zip

        Example:
            download = client.vault.download_folder("/MyProject/results")
            response = requests.get(download.url)
            with open("results.zip", "wb") as f:
                f.write(response.content)
        """
        if not vault_path and not folder_id:
            raise ValueError("Either vault_path or folder_id is required")

        response = self._http.post(
            "/api/v1/ai/vault/folders/download-zip",
            json={
                "vault_path": vault_path,
                "folder_id": folder_id,
            },
        )

        return DownloadResult(
            url=response["download_url"],
            filename=response["filename"],
            file_count=response.get("file_count"),
            size=response.get("total_size"),
        )
