# Simple Zope instance script to dump out SimpleBlog entries with their
# comments to an XML format
import logging
import optparse
import sys
import xml.sax.saxutils
from DateTime import DateTime
from ZODB.POSException import ConflictError

logger = logging.getLogger('simple-dumper')

# Borrowed from Django
class SimplerXMLGenerator(xml.sax.saxutils.XMLGenerator):
    def addQuickElement(self, name, contents=None, attrs=None):
        "Convenience method for adding an element with no children"
        if attrs is None: attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents)
        self.endElement(name)

def run(app):
    options, args = parse_args()
    ob = app.unrestrictedTraverse(options.item_path)

    if options.out_file:
        out = open(options.out_file, 'w')
    else:
        out = sys.stdout

    handler = SimplerXMLGenerator(out, 'utf-8')        
    export(handler, ob, out)

def export(handler, ob, out):
    handler.startElement(ob.meta_type, {})
    for field in ob.Schema().filterFields():
        try:
            value = field.get(ob)
        except ConflictError:
            raise
        except:
            logger.warn('Problem getting value for %s on %s' % (field.getName(), 
                '/'.join(ob.getPhysicalPath())))
            continue
            
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            for item in value:
                handler.addQuickElement('sequence-item', item)
            continue
        elif isinstance(value, DateTime):
            value = value.rfc822()

        if isinstance(value, str):
            value = value.decode('utf-8')
        if not isinstance(value, unicode):
            value = unicode(value ) # Hope for the best!
        handler.addQuickElement(field.getName(), unicode(value))

    if ob.isPrincipiaFolderish:
        for subob in ob.objectValues():
            export(handler, subob, out)
    handler.endElement(ob.meta_type)

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--item-path', dest='item_path',
        help='Path to the instance to export eg. /path/to/folder')
    parser.add_option('-o', '--out-file', dest='out_file',
        help='File to write output to, or stdout if missing')
    options, args = parser.parse_args()
    return options, args

if __name__ == '__main__':
    run(app)