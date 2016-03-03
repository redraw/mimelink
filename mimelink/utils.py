import xml.etree.ElementTree as ET
import xml.dom.minidom as md


class XML(object):
    def __init__(self, tag, text=None, **kwargs):
        self.elem = ET.Element(tag, **kwargs)
        self.elem.text = text

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        return self.prettify()

    @classmethod    
    def tag(cls, tag, text=None, **kwargs):
        e = ET.Element(tag, **kwargs)
        e.text = text
        return e

    def prettify(self, encoding="utf-8"):
        i = ET.tostring(self.elem)
        o = md.parseString(i).toprettyxml(encoding=encoding)
        return o

    def write(self, filepath, prettify=False, encoding="utf-8"):
        with open(filepath, 'w+') as f:
            if prettify:
                output = self.prettify(encoding=encoding)
            else:
                output = ET.tostring(encoding=encoding)
            f.write(output)
