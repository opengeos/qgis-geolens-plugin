PLUGIN_NAME := geolens_qgis
QGIS_PLUGIN_DIR ?= $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins

.PHONY: test install package clean

test:
	python -m unittest discover -s tests -v
	python -m compileall -q $(PLUGIN_NAME)

install:
	mkdir -p "$(QGIS_PLUGIN_DIR)"
	ln -sfn "$(CURDIR)/$(PLUGIN_NAME)" "$(QGIS_PLUGIN_DIR)/$(PLUGIN_NAME)"

package: clean
	mkdir -p dist
	python -c 'import shutil; shutil.make_archive("dist/$(PLUGIN_NAME)", "zip", root_dir=".", base_dir="$(PLUGIN_NAME)")'

clean:
	rm -rf dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
