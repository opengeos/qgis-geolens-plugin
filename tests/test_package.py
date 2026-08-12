import zipfile

import pytest

from package_plugin import package_plugin


def test_package_has_qgis_layout(tmp_path):
    with pytest.raises(FileNotFoundError):
        package_plugin(tmp_path.parent / "missing", tmp_path / "bad.zip")


def test_real_package_has_required_files(tmp_path):
    from package_plugin import PLUGIN_DIR

    output = package_plugin(PLUGIN_DIR, tmp_path / "plugin.zip")
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
    assert "geolens_qgis/__init__.py" in names
    assert "geolens_qgis/metadata.txt" in names
    assert "geolens_qgis/LICENSE" in names
    assert not any("__pycache__" in name for name in names)


def test_package_skips_symlinks_to_external_files(tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    source = tmp_path / "plugin"
    source.mkdir()
    for required in ("__init__.py", "metadata.txt", "LICENSE"):
        (source / required).write_text("version=0.1.0\n", encoding="utf-8")
    (source / "leak.txt").symlink_to(outside)

    output = package_plugin(source, tmp_path / "plugin.zip")
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
    assert "plugin/leak.txt" not in names
    assert "geolens_qgis/leak.txt" not in names
    assert "geolens_qgis/metadata.txt" in names
