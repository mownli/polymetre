TARGET = polymetre.pyz
INSTALLDIR = ~/.local/bin
PYTHON = /usr/bin/env python3
SRCDIR = polymetre
BUILDDIR = build

pyz: $(SRCDIR)
	mkdir -p "$(BUILDDIR)"
	cp -r "$(SRCDIR)"/* -t "$(BUILDDIR)"
	find "$(BUILDDIR)" -type f -print0 | xargs -0 sed -i "s/import polymetre\./import /g"
	find "$(BUILDDIR)" -type f -print0 | xargs -0 sed -i "s/from polymetre\./from /g"
	find "$(BUILDDIR)" -type f -print0 | xargs -0 sed -i "s/from polymetre //g"
	find "$(BUILDDIR)" -type d -name "__pycache__" -print0 | xargs -0 rm -rf
	cd "$(BUILDDIR)"; zip -rq tmp.zip *
	echo "#!$(PYTHON)" > "$(BUILDDIR)/$(TARGET)"
	cat "$(BUILDDIR)/tmp.zip" >> "$(BUILDDIR)/$(TARGET)"
	chmod u+x "$(BUILDDIR)/$(TARGET)"

install: $(BUILDDIR)/$(TARGET)
	install $^ $(INSTALLDIR)/$(TARGET)

clean:
	rm -rf build
	rm -rf dist
	rm -rf polymetre.egg-info

wheel: $(SRCDIR)
	python setup.py bdist_wheel
