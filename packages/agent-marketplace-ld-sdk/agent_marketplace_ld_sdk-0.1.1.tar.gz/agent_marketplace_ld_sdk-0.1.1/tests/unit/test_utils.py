"""Tests for utility modules."""

from pathlib import Path

import pytest

from agent_marketplace_sdk.exceptions import ValidationError
from agent_marketplace_sdk.utils import (
    create_agent_package,
    download_file,
    extract_zip,
    get_package_size,
    prepare_upload,
    validate_agent_name,
    validate_agent_structure,
    validate_version,
)


class TestDownloadUtils:
    """Tests for download utilities."""

    def test_download_file(self, tmp_path: Path):
        """Test downloading file."""
        content = b"test content"
        destination = tmp_path / "test.txt"

        result = download_file(content, destination)

        assert result == destination
        assert destination.exists()
        assert destination.read_bytes() == content

    def test_download_file_creates_parent(self, tmp_path: Path):
        """Test downloading file creates parent directories."""
        content = b"test content"
        destination = tmp_path / "subdir" / "test.txt"

        result = download_file(content, destination)

        assert result.exists()

    def test_extract_zip(self, tmp_path: Path, sample_zip_content: bytes):
        """Test extracting zip content."""
        destination = tmp_path / "extracted"

        result = extract_zip(sample_zip_content, destination)

        assert result == destination
        assert destination.exists()
        assert (destination / "agent.py").exists()
        assert (destination / "agent.yaml").exists()


class TestUploadUtils:
    """Tests for upload utilities."""

    def test_prepare_upload(self, sample_agent_dir: Path):
        """Test preparing upload."""
        result = prepare_upload(sample_agent_dir)

        assert result is not None
        content = result.read()
        assert len(content) > 0


class TestValidationUtils:
    """Tests for validation utilities."""

    def test_validate_agent_name_valid(self):
        """Test valid agent name."""
        assert validate_agent_name("test-agent") is True
        assert validate_agent_name("TestAgent") is True
        assert validate_agent_name("test123") is True

    def test_validate_agent_name_invalid_start(self):
        """Test agent name starting with number."""
        with pytest.raises(ValidationError):
            validate_agent_name("1test")

    def test_validate_agent_name_too_short(self):
        """Test agent name too short."""
        with pytest.raises(ValidationError):
            validate_agent_name("ab")

    def test_validate_agent_name_invalid_chars(self):
        """Test agent name with invalid characters."""
        with pytest.raises(ValidationError):
            validate_agent_name("test_agent")  # underscore not allowed

    def test_validate_version_valid(self):
        """Test valid version."""
        assert validate_version("1.0.0") is True
        assert validate_version("10.20.30") is True
        assert validate_version("0.0.1") is True

    def test_validate_version_invalid(self):
        """Test invalid version."""
        with pytest.raises(ValidationError):
            validate_version("1.0")

        with pytest.raises(ValidationError):
            validate_version("v1.0.0")

        with pytest.raises(ValidationError):
            validate_version("1.0.0-beta")

    def test_validate_agent_structure_valid(self, sample_agent_dir: Path):
        """Test valid agent structure."""
        assert validate_agent_structure(sample_agent_dir) is True

    def test_validate_agent_structure_not_directory(self, tmp_path: Path):
        """Test agent structure validation with file."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")

        with pytest.raises(ValidationError) as exc_info:
            validate_agent_structure(file_path)
        assert "not a directory" in str(exc_info.value)

    def test_validate_agent_structure_missing_files(self, tmp_path: Path):
        """Test agent structure validation with missing files."""
        agent_dir = tmp_path / "incomplete-agent"
        agent_dir.mkdir()
        (agent_dir / "README.md").write_text("# Agent")

        with pytest.raises(ValidationError) as exc_info:
            validate_agent_structure(agent_dir)
        assert "Missing required files" in str(exc_info.value)


class TestPackagingUtils:
    """Tests for packaging utilities."""

    def test_create_agent_package(self, sample_agent_dir: Path):
        """Test creating agent package."""
        result = create_agent_package(sample_agent_dir)

        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_create_agent_package_empty_dir(self, tmp_path: Path):
        """Test creating agent package from empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = create_agent_package(empty_dir)

        # Should still create a valid (empty) zip
        assert isinstance(result, bytes)

    def test_create_agent_package_with_subdirs(self, tmp_path: Path):
        """Test creating agent package with subdirectories."""
        agent_dir = tmp_path / "agent-with-subdirs"
        agent_dir.mkdir()
        (agent_dir / "subdir").mkdir()
        (agent_dir / "subdir" / "nested").mkdir()
        (agent_dir / "file.py").write_text("code")
        (agent_dir / "subdir" / "file2.py").write_text("code2")

        result = create_agent_package(agent_dir)

        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_get_package_size(self, sample_agent_dir: Path):
        """Test getting package size."""
        size = get_package_size(sample_agent_dir)

        assert isinstance(size, int)
        assert size > 0


class TestUploadUtilsEmpty:
    """Additional tests for upload utilities."""

    def test_prepare_upload_empty_dir(self, tmp_path: Path):
        """Test preparing upload from empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = prepare_upload(empty_dir)

        assert result is not None

    def test_prepare_upload_with_subdirs(self, tmp_path: Path):
        """Test preparing upload with subdirectories."""
        agent_dir = tmp_path / "agent-with-subdirs"
        agent_dir.mkdir()
        (agent_dir / "subdir").mkdir()
        (agent_dir / "file.py").write_text("code")

        result = prepare_upload(agent_dir)

        assert result is not None
        content = result.read()
        assert len(content) > 0
