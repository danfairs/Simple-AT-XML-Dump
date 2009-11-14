# Simple Zope instance script to dump out SimpleBlog entries with their
# comments to an XML format
import optparse
import sys

def run(app):
    options, args = parse_args()
    blog = app.unrestrictedTraverse(options.blog_path)


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-b', '--blog-path', dest='blog_path',
        help='Path to the SimpleBlog instance eg. /path/to/blog')
    options, args = parser.parse_args()
    
    if not options.blog_path:
        parser.error('Please provide a blog path')

    return options, args

if __name__ == '__main__':
    run(app)