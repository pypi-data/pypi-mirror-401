from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from sxd_master.build import BuildEngine


@pytest.fixture
def build_engine():
    with patch("sxd_master.build.docker_from_env") as mock_from_env:
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        engine = BuildEngine(registry_url="localhost:5000")
        yield engine


@pytest.mark.asyncio
async def test_build_engine_docker_build_command(build_engine):
    # Setup mock images
    mock_images = build_engine.docker_client.images
    mock_images.build.return_value = (MagicMock(), [])
    mock_images.push.return_value = '{"status": "Pushing..."}'

    # Create dummy Dockerfile
    dockerfile = Path("Dockerfile")
    dockerfile.write_text("FROM ghcr.io/sentient-x/sxd-base:latest")

    # Test building a sample pipeline
    image_tag = await build_engine.build_pipeline(
        name="test-pipeline",
        dockerfile_path=Path("Dockerfile"),
        context_path=Path("."),
        tag="v1.0.0",
    )
    await build_engine.push_pipeline(image_tag)

    # Verify docker build was called
    from unittest.mock import ANY

    mock_images.build.assert_called_once_with(
        path=".",
        dockerfile="Dockerfile",
        tag="localhost:5000/test-pipeline:v1.0.0",
        buildargs=None,
        rm=True,
    )

    # Verify docker push was called
    mock_images.push.assert_called_once_with(
        "localhost:5000/test-pipeline:v1.0.0", stream=True, decode=True
    )
