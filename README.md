# mimelink

This is just a Python command-line/module to generate and install MIME types on some GNU/Linux distributions following the (Shared MIME-info specification)[https://specifications.freedesktop.org/shared-mime-info-spec] XML format

### Install

```bash
$ git clone https://github.com/redraw/mimelink
$ cd mimelink
$ sudo chmod +x mimelink.py
$ sudo ln -s $(readlink -f mimelink.py) /usr/local/bin/mimelink
```

### Example

On command-line

```bash
$ mimelink processing-app text/x-processing *.pde *.PDE

<?xml version="1.0" encoding="utf-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
	<mime-type type="text/x-processing">
		<comment/>
		<glob-deleteall/>
		<glob-pattern>*.pde</glob-pattern>
		<glob-pattern>*.PDE</glob-pattern>
	</mime-type>
</mime-info>

saving in /home/redraw/.local/share/mime/packages/processing-app.xml
running update-mime-database...
```

or as a Python module,

```python
from mimelink import MimeLink

m = MimeLink(name="processing-app", mimetype="text/x-processing", patterns=["*.pde", "*.PDE"])
m.link()
```

### Author notes

Beerware (?)
