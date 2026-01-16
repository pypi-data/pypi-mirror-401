"""Tests for S3Provider"""

import sys
import tempfile
from pathlib import Path

import pytest
from moto import mock_aws


class TestS3ProviderParseS3URL:
    """Tests for parse_s3_url method"""

    def test_parse_s3_url_s3_protocol(self, s3_provider):
        """Test parsing s3:// URL"""
        bucket, key = s3_provider.parse_s3_url("s3://my-bucket/path/to/file.txt")
        assert bucket == "my-bucket"
        assert key == "path/to/file.txt"

    def test_parse_s3_url_https_protocol(self, s3_provider):
        """Test parsing https:// S3 URL"""
        bucket, key = s3_provider.parse_s3_url(
            "https://my-bucket.s3.amazonaws.com/path/to/file.txt"
        )
        assert bucket == "my-bucket"
        assert key == "path/to/file.txt"

    def test_parse_s3_url_http_protocol(self, s3_provider):
        """Test parsing http:// S3 URL"""
        bucket, key = s3_provider.parse_s3_url(
            "http://my-bucket.s3.amazonaws.com/path/to/file.txt"
        )
        assert bucket == "my-bucket"
        assert key == "path/to/file.txt"

    def test_parse_s3_url_root_key(self, s3_provider):
        """Test parsing URL with root key"""
        bucket, key = s3_provider.parse_s3_url("s3://my-bucket/file.txt")
        assert bucket == "my-bucket"
        assert key == "file.txt"

    def test_parse_s3_url_nested_path(self, s3_provider):
        """Test parsing URL with deeply nested path"""
        bucket, key = s3_provider.parse_s3_url(
            "s3://my-bucket/level1/level2/level3/file.txt"
        )
        assert bucket == "my-bucket"
        assert key == "level1/level2/level3/file.txt"

    def test_parse_s3_url_invalid_format_raises_error(self, s3_provider):
        """Test that invalid URL format raises ValueError"""
        with pytest.raises(ValueError, match="Unsupported S3 URL format"):
            s3_provider.parse_s3_url("invalid-url-format")


class TestS3ProviderUploadBytes:
    """Tests for upload_bytes method"""

    @mock_aws
    def test_upload_bytes_success(self, s3_provider):
        """Test successful upload of bytes"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        content = b"test file content"
        key = "test/path/file.txt"
        s3_url = s3_provider.upload_bytes(key=key, content=content)

        assert s3_url == f"s3://{s3_provider.bucket}/{key}"

        # Verify the object was uploaded
        response = s3_provider.client.get_object(Bucket=s3_provider.bucket, Key=key)
        assert response["Body"].read() == content

    @mock_aws
    def test_upload_bytes_with_content_type(self, s3_provider):
        """Test upload with content type"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        content = b'{"key": "value"}'
        key = "test/data.json"
        content_type = "application/json"
        s3_url = s3_provider.upload_bytes(
            key=key, content=content, content_type=content_type
        )

        assert s3_url == f"s3://{s3_provider.bucket}/{key}"

        # Verify the content type was set
        response = s3_provider.client.head_object(Bucket=s3_provider.bucket, Key=key)
        assert response["ContentType"] == content_type

    @mock_aws
    def test_upload_bytes_empty_content(self, s3_provider):
        """Test upload of empty bytes"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        content = b""
        key = "test/empty.txt"
        s3_url = s3_provider.upload_bytes(key=key, content=content)

        assert s3_url == f"s3://{s3_provider.bucket}/{key}"

        # Verify the object was uploaded
        response = s3_provider.client.get_object(Bucket=s3_provider.bucket, Key=key)
        assert response["Body"].read() == content


class TestS3ProviderUploadFile:
    """Tests for upload_file method"""

    @mock_aws
    def test_upload_file_success(self, s3_provider):
        """Test successful upload of file"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode="wb") as tmp_file:
            tmp_file.write(b"test file content")
            tmp_file_path = tmp_file.name

        try:
            key = "test/path/file.txt"
            s3_url = s3_provider.upload_file(file_path=tmp_file_path, key=key)

            assert s3_url == f"s3://{s3_provider.bucket}/{key}"

            # Verify the object was uploaded
            response = s3_provider.client.get_object(Bucket=s3_provider.bucket, Key=key)
            assert response["Body"].read() == b"test file content"
        finally:
            # Clean up temporary file
            Path(tmp_file_path).unlink()

    @mock_aws
    def test_upload_file_nonexistent_file_raises_error(self, s3_provider):
        """Test that uploading nonexistent file raises error"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        with pytest.raises(FileNotFoundError):
            s3_provider.upload_file(
                file_path="/nonexistent/path/file.txt", key="test/file.txt"
            )


class TestS3ProviderGetObjectBytes:
    """Tests for get_object_bytes method"""

    @mock_aws
    def test_get_object_bytes_success(self, s3_provider):
        """Test successful download of object as bytes"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        # Upload a test file
        test_key = "test/path/file.txt"
        test_content = b"test file content"
        s3_provider.client.put_object(
            Bucket=s3_provider.bucket, Key=test_key, Body=test_content
        )

        # Download using s3:// URL
        s3_url = f"s3://{s3_provider.bucket}/{test_key}"
        content = s3_provider.get_object_bytes(s3_url=s3_url)

        assert content == test_content

    @mock_aws
    def test_get_object_bytes_https_url(self, s3_provider):
        """Test download using https:// URL"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        # Upload a test file
        test_key = "test/path/file.txt"
        test_content = b"test file content"
        s3_provider.client.put_object(
            Bucket=s3_provider.bucket, Key=test_key, Body=test_content
        )

        # Download using https:// URL
        s3_url = f"https://{s3_provider.bucket}.s3.amazonaws.com/{test_key}"
        content = s3_provider.get_object_bytes(s3_url=s3_url)

        assert content == test_content

    @mock_aws
    def test_get_object_bytes_nonexistent_file_raises_error(self, s3_provider):
        """Test that downloading nonexistent file raises error"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        s3_url = f"s3://{s3_provider.bucket}/nonexistent/file.txt"
        with pytest.raises(Exception):  # boto3 raises ClientError
            s3_provider.get_object_bytes(s3_url=s3_url)


class TestS3ProviderPresignGetURL:
    """Tests for presign_get_url_from_s3_url method"""

    @mock_aws
    def test_presign_get_url_s3_protocol(self, s3_provider):
        """Test generating presigned URL from s3:// URL"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        # Upload a test file
        test_key = "test/path/file.txt"
        s3_provider.client.put_object(
            Bucket=s3_provider.bucket, Key=test_key, Body=b"test content"
        )

        s3_url = f"s3://{s3_provider.bucket}/{test_key}"
        presigned_url = s3_provider.presign_get_url_from_s3_url(s3_url=s3_url)

        assert presigned_url.startswith("https://")
        assert s3_provider.bucket in presigned_url
        assert test_key in presigned_url

    @mock_aws
    def test_presign_get_url_https_protocol(self, s3_provider):
        """Test generating presigned URL from https:// URL"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        # Upload a test file
        test_key = "test/path/file.txt"
        s3_provider.client.put_object(
            Bucket=s3_provider.bucket, Key=test_key, Body=b"test content"
        )

        s3_url = f"https://{s3_provider.bucket}.s3.amazonaws.com/{test_key}"
        presigned_url = s3_provider.presign_get_url_from_s3_url(s3_url=s3_url)

        assert presigned_url.startswith("https://")
        assert s3_provider.bucket in presigned_url
        assert test_key in presigned_url

    @mock_aws
    def test_presign_get_url_custom_expiration(self, s3_provider):
        """Test generating presigned URL with custom expiration"""
        s3_provider.client.create_bucket(Bucket=s3_provider.bucket)

        # Upload a test file
        test_key = "test/path/file.txt"
        s3_provider.client.put_object(
            Bucket=s3_provider.bucket, Key=test_key, Body=b"test content"
        )

        s3_url = f"s3://{s3_provider.bucket}/{test_key}"
        presigned_url = s3_provider.presign_get_url_from_s3_url(
            s3_url=s3_url, expiration=7200
        )

        assert presigned_url.startswith("https://")
        # The expiration parameter should be used (moto may not validate this, but it's passed)


class TestS3ProviderGetFilenameFromS3URL:
    """Tests for get_filename_from_s3_url method"""

    def test_get_filename_from_s3_url_simple(self, s3_provider):
        """Test extracting filename from simple S3 URL"""
        s3_url = "s3://bucket/path/to/file.txt"
        filename = s3_provider.get_filename_from_s3_url(s3_url=s3_url)
        assert filename == "file.txt"

    def test_get_filename_from_s3_url_nested(self, s3_provider):
        """Test extracting filename from nested path"""
        s3_url = "s3://bucket/level1/level2/level3/document.pdf"
        filename = s3_provider.get_filename_from_s3_url(s3_url=s3_url)
        assert filename == "document.pdf"

    def test_get_filename_from_s3_url_root(self, s3_provider):
        """Test extracting filename from root level"""
        s3_url = "s3://bucket/file.txt"
        filename = s3_provider.get_filename_from_s3_url(s3_url=s3_url)
        assert filename == "file.txt"

    def test_get_filename_from_s3_url_https(self, s3_provider):
        """Test extracting filename from https:// URL"""
        s3_url = "https://bucket.s3.amazonaws.com/path/to/file.txt"
        filename = s3_provider.get_filename_from_s3_url(s3_url=s3_url)
        assert filename == "file.txt"

    def test_get_filename_from_s3_url_no_extension(self, s3_provider):
        """Test extracting filename without extension"""
        s3_url = "s3://bucket/path/to/file"
        filename = s3_provider.get_filename_from_s3_url(s3_url=s3_url)
        assert filename == "file"

    def test_get_filename_from_s3_url_no_extension_with_default(self, s3_provider):
        """Test extracting filename without extension with default"""
        s3_url = "s3://bucket/path/to/file"
        filename = s3_provider.get_filename_from_s3_url(
            s3_url=s3_url, default="default.txt"
        )
        assert filename == "default.txt"

    def test_get_filename_from_s3_url_empty_key(self, s3_provider):
        """Test extracting filename from empty key"""
        s3_url = "s3://bucket/"
        filename = s3_provider.get_filename_from_s3_url(s3_url=s3_url)
        assert filename == "file"  # Default fallback

    def test_get_filename_from_s3_url_empty_key_with_default(self, s3_provider):
        """Test extracting filename from empty key with default"""
        s3_url = "s3://bucket/"
        filename = s3_provider.get_filename_from_s3_url(
            s3_url=s3_url, default="default.txt"
        )
        assert filename == "default.txt"
