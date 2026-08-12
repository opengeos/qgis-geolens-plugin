"""QGIS entry point for GeoLens."""


def classFactory(iface):
    from .plugin import GeoLensPlugin

    return GeoLensPlugin(iface)
