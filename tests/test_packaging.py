from unittest.mock import MagicMock, patch
from src.app.utilities.mqtt_client import publish_message
from src.app.packaging import (
    perform_packaging,
    is_packaging_required,
    __zip_folder,
    __delete_folder,
)


@patch("src.app.packaging.is_packaging_required")
def test_perform_packaging_no_packaging_required(mock_is_packaging_required):
    config = MagicMock() @ patch("src.app.packaging.log")

    mock_is_packaging_required.return_value = False

    perform_packaging(config)

    mock_is_packaging_required.assert_called_once_with(
        f"{config.data.path}/{config.nsp.data.path}"
    )


@patch("src.app.packaging.publish_message")
@patch("src.app.packaging.is_packaging_required")
@patch("src.app.packaging.data_directory_contents")
@patch("src.app.packaging.__zip_folder")
@patch("src.app.packaging.__delete_folder")
def test_perform_packaging_with_packaging_required(
    mock_delete_folder,
    mock_zip_folder,
    mock_data_directory_contents,
    mock_is_packaging_required,
    mock_publish_message,
):
    config = MagicMock()
    mock_is_packaging_required.return_value = True
    mock_data_directory_contents.return_value = ["folder1"]

    perform_packaging(config)

    mock_is_packaging_required.assert_called_once_with(
        f"{config.data.path}/{config.nsp.data.path}"
    )
    mock_data_directory_contents.assert_called_once_with(config)
    mock_zip_folder.assert_called_once_with(
        "folder1", f"{config.data.path}/{config.nsp.data.path}", "folder1", "zip"
    )
    mock_delete_folder.assert_called_once_with("folder1")
    mock_publish_message.assert_called_once()


@patch("src.app.packaging.os.path.exists")
def test_is_packaging_required_with_non_existing_data_location(mock_exists):
    data_location = "/data/path"
    mock_exists.return_value = False

    result = is_packaging_required(data_location)

    assert result is False


@patch("src.app.packaging.shutil")
def test___zip_folder(mock_exists):
    source = "folder1"
    package_format = "zip"
    root = "/data/path/nsp/data/path"
    base = "folder1"

    __zip_folder(source, root, base, package_format)

    mock_exists.make_archive.assert_called_once_with(
        "folder1", "zip", "/data/path/nsp/data/path", "folder1"
    )


@patch("src.app.packaging.shutil.rmtree")
def test___delete_folder(mock_rmtree):
    path = "folder1"
    __delete_folder(path)
    mock_rmtree.assert_called_once_with("folder1")
