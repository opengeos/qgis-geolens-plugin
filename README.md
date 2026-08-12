# GeoLens for QGIS

A QGIS plugin for browsing and using datasets from a self-hosted [GeoLens](https://getgeolens.com) server. It brings the GeoLens catalog workflow from [GeoLibre](https://github.com/opengeos/GeoLibre) into QGIS.

## Features

- Connect to any GeoLens server, with an optional API key for private data.
- Search the catalog and inspect dataset descriptions, types, and feature counts.
- Add vector datasets as signed Mapbox Vector Tile layers with automatic token renewal.
- Add public raster datasets as server-rendered XYZ tile layers.
- Load vector datasets through OGC API Features, optionally clipped to the current map extent.
- Open a dataset's GeoLens metadata page.
- Edit loaded feature layers in QGIS and synchronize creates, updates, and deletes back to GeoLens when the server permits editing.
- Use the public GeoLibre datasets and GeoLens demo servers from the built-in server picker.

## Install for development

Clone the repository and link its plugin directory into your active QGIS profile:

```bash
git clone https://github.com/opengeos/qgis-geolens-plugin.git
cd qgis-geolens-plugin
make install
```

Restart QGIS, enable **GeoLens** in **Plugins → Manage and Install Plugins**, then open it from **Web → GeoLens** or the toolbar.

The default Linux profile is `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`. Override it when needed:

```bash
make install QGIS_PLUGIN_DIR=/path/to/profile/python/plugins
```

## Usage

1. Enter a GeoLens server URL or choose a sample server.
2. Enter an API key if the catalog or datasets are private, then click **Connect**.
3. Search and select a dataset.
4. Choose **Add tiles** for scalable viewing, or **Add features** for attributes and editing.
5. For an editable feature layer, commit QGIS edits, select that layer, and click **Sync selected GeoLens layer edits**.

GeoLens writes are per-feature and are not transactional. The plugin reports partial failures and requires confirmation before deleting server features. API keys are stored only in the local QGIS profile settings and are never written to project layer properties.

Private raster tiles need a QGIS Authentication configuration capable of adding
an `X-Api-Key` request header. The initial release deliberately does not embed
API keys in raster layer source URLs, because QGIS serializes those URLs into
project files.

## Development

The HTTP client has no QGIS dependency, so its tests run with standard Python:

```bash
python -m unittest discover -s tests -v
python -m compileall -q geolens_qgis
make package
```

The generated `dist/geolens_qgis.zip` has the directory layout expected by the QGIS Plugin Manager.

## License

MIT
