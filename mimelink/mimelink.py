#!/usr/bin/env python
import os
import argparse
import subprocess

from utils import XML


HOME_PATH = os.path.expanduser('~')
MIME_PATH = os.path.join(HOME_PATH, ".local/share/mime")
MIME_PACKAGES_PATH = os.path.join(MIME_PATH, "packages")
XMLNS = "http://www.freedesktop.org/standards/shared-mime-info"


class MimeLink(object):
    """Helper to link MIME types in GNU/Linux"""

    def __init__(self, name, mimetype, patterns, comment=None):
        self.name = name
        self.mimetype = mimetype
        self.patterns = patterns
        self.comment = comment
        self.xml = None

    def make_xml(self):
        """Returns a utils' XML object"""

        with XML('mime-info', xmlns=XMLNS) as xml:

            mimetype = XML.tag('mime-type', type=self.mimetype)

            mimetype.extend([
                XML.tag('comment', self.comment or ""),
                XML.tag('glob-deleteall')
            ])

            mimetype.extend([
                XML.tag('glob-pattern', pattern) 
                for pattern in self.patterns
            ])

            xml.elem.append(mimetype)

        return xml

    def link(self, dry_run=False):
        """
        Writes the XML file into mime/packages, 
        and updates the database with `update-mime-database`
        """

        self.xml = self.make_xml()
        
        print str(self.xml)

        if dry_run: return

        if not os.path.exists(MIME_PACKAGES_PATH):
            os.makedirs(MIME_PACKAGES_PATH)

        name = self.name.split('-')
        
        if name > 1:
            vendor, app = (name[0], "".join(name[1:]))
        else:
            vendor, app = ('mimelink', self.name)

        filepath = os.path.join(MIME_PACKAGES_PATH, "%s-%s.xml" % (vendor, app))

        print "saving in %s" % filepath
        self.xml.write(filepath, prettify=True)

        print "running update-mime-database..."
        subprocess.call(['update-mime-database', MIME_PATH])


def main(args):
    """Main function."""

    mimelink = MimeLink(
        name=args.name, 
        mimetype=args.mimetype, 
        patterns=args.patterns,
        comment=args.comment
    )

    mimelink.link(dry_run=args.dry_run)


if __name__ == '__main__':
    """Run from command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="vendor-app name")
    parser.add_argument('mimetype', help="MIME type. ie. text/plain")
    parser.add_argument('patterns', nargs='+', help="Glob pattern. ie. *.jpg")
    parser.add_argument('--comment')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    main(args)