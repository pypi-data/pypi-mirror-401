"""Reusable AWS S3 provider helpers.

This module intentionally does NOT import `api.config` to avoid circular imports.
Instantiate an `S3Provider` in `api/config.py` and import that instance where needed.
"""

from __future__ import annotations

from typing import Optional, Tuple


class S3Provider:
    """Minimal S3 provider wrapper for upload + presigned download.

    Creates its own boto3 S3 client internally from bucket and region.
    """

    def __init__(
        self,
        bucket: str,
        region: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        """Initialize S3 provider with bucket, region, and AWS credentials.

        Args:
            bucket: S3 bucket name
            region: AWS region name
            aws_access_key_id: AWS access key ID
            aws_secret_access_key: AWS secret access key
        """
        try:
            import boto3
            from botocore.config import Config
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "boto3 is required for S3Provider. Install it with: pip install boto3"
            ) from e

        self.bucket = bucket
        self.region = region
        # Create boto3 S3 client (does not perform network calls)
        self.client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def parse_s3_url(self, s3_url: str) -> Tuple[str, str]:
        """Parse an S3 URL into (bucket, key).

        Supports:
        - s3://bucket/key
        - https://bucket.s3.amazonaws.com/key
        - http://bucket.s3.amazonaws.com/key

        Args:
            s3_url: The S3 URL to parse

        Returns:
            Tuple of (bucket, key)

        Raises:
            ValueError: If the URL format is unsupported
        """
        if s3_url.startswith("s3://"):
            remainder = s3_url.removeprefix("s3://")
            bucket, _, key = remainder.partition("/")
            return bucket, key

        if "s3.amazonaws.com" in s3_url:
            remainder = s3_url.removeprefix("https://").removeprefix("http://")
            host, _, key = remainder.partition("/")
            bucket = host.split(".", 1)[0]
            return bucket, key

        raise ValueError(f"Unsupported S3 URL format: {s3_url}")

    def upload_bytes(
        self,
        *,
        key: str,
        content: bytes,
        content_type: Optional[str] = None,
    ) -> str:
        """Upload bytes to S3 and return an s3:// URL."""
        params = {"Bucket": self.bucket, "Key": key, "Body": content}
        if content_type:
            params["ContentType"] = content_type
        self.client.put_object(**params)
        return f"s3://{self.bucket}/{key}"

    def upload_file(self, *, file_path: str, key: str) -> str:
        """Upload a local file to S3 and return an s3:// URL."""
        self.client.upload_file(file_path, self.bucket, key)
        return f"s3://{self.bucket}/{key}"

    def presign_get_url_from_s3_url(
        self, *, s3_url: str, expiration: int = 3600
    ) -> str:
        """Generate a presigned GET URL for a stored S3 URL."""
        bucket, key = self.parse_s3_url(s3_url)
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration,
        )

    def get_object_bytes(self, *, s3_url: str) -> bytes:
        """Download an object from S3 and return its content as bytes."""
        bucket, key = self.parse_s3_url(s3_url)
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()

    def get_filename_from_s3_url(
        self, *, s3_url: str, default: Optional[str] = None
    ) -> str:
        """Extract the filename from an S3 URL.

        Args:
            s3_url: The S3 URL to extract the filename from
            default: Optional default filename if extraction fails or filename is invalid

        Returns:
            The filename extracted from the S3 URL, or the default if provided
        """
        _, key = self.parse_s3_url(s3_url)
        # Get the filename from the key (last part after the last "/")
        filename = key.split("/")[-1] if "/" in key else key
        # Use default if filename is empty or doesn't have extension
        if not filename or "." not in filename:
            if default:
                return default
            return filename if filename else "file"
        return filename
