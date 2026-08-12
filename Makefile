PLUGIN_NAME := geolens_qgis
QGIS_PLUGIN_DIR ?= $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins

.PHONY: test install package clean

test:
	python -m pytest tests -v
	python -m compileall -q $(PLUGIN_NAME)

install:
	python install.py --plugin-dir "$(QGIS_PLUGIN_DIR)"

package: clean
	python package_plugin.py --output "dist/$(PLUGIN_NAME).zip"

clean:
	rm -rf dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
