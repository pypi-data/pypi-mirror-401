# -*- coding: utf-8 -*-
#

#   pyhwp : hwp file format parser in python
#   Copyright (C) 2010-2023 mete0r <https://github.com/mete0r>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from argparse import ArgumentParser
from contextlib import contextmanager
from contextlib import closing
from functools import partial
import gettext
import io
import logging
import os.path
import shutil
import shutil
import sys
import base64
import re
import tempfile
import mimetypes

from . import __version__ as version
from .cli import init_logger
from .transforms import BaseTransform
from .utils import cached_property


PY3 = sys.version_info.major == 3
logger = logging.getLogger(__name__)
locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
locale_dir = os.path.abspath(locale_dir)
t = gettext.translation('hwp5html', locale_dir, fallback=True)
_ = t.gettext


RESOURCE_PATH_XSL_CSS = 'xsl/hwp5css.xsl'
RESOURCE_PATH_XSL_XHTML = 'xsl/hwp5html.xsl'


class HTMLTransform(BaseTransform):

    @property
    def transform_hwp5_to_css(self):
        '''
        >>> T.transform_hwp5_to_css(hwp5file, 'styles.css')
        '''
        transform_xhwp5 = self.transform_xhwp5_to_css
        return self.make_transform_hwp5(transform_xhwp5)

    @property
    def transform_hwp5_to_xhtml(self):
        '''
        >>> T.transform_hwp5_to_xhtml(hwp5file, 'index.xhtml')
        '''
        transform_xhwp5 = self.transform_xhwp5_to_xhtml
        return self.make_transform_hwp5(transform_xhwp5)

    def transform_hwp5_to_dir(self, hwp5file, outdir):
        '''
        >>> T.transform_hwp5_to_dir(hwp5file, 'output')
        '''
        with self.transformed_xhwp5_at_temp(hwp5file) as xhwp5path:
            self.transform_xhwp5_to_dir(xhwp5path, outdir)

        bindata_dir = os.path.join(outdir, 'bindata')
        self.extract_bindata_dir(hwp5file, bindata_dir)

    @cached_property
    def transform_xhwp5_to_css(self):
        '''
        >>> T.transform_xhwp5_to_css('hwp5.xml', 'styles.css')
        '''
        resource_path = RESOURCE_PATH_XSL_CSS
        return self.make_xsl_transform(resource_path)

    @cached_property
    def transform_xhwp5_to_xhtml(self):
        '''
        >>> T.transform_xhwp5_to_xhtml('hwp5.xml', 'index.xhtml')
        '''
        resource_path = RESOURCE_PATH_XSL_XHTML
        return self.make_xsl_transform(resource_path)

    def transform_xhwp5_to_dir(self, xhwp5path, outdir):
        '''
        >>> T.transform_xhwp5_to_dir('hwp5.xml', 'output')
        '''
        html_path = os.path.join(outdir, 'index.xhtml')
        with io.open(html_path, 'wb') as f:
            self.transform_xhwp5_to_xhtml(xhwp5path, f)

        css_path = os.path.join(outdir, 'styles.css')
        with io.open(css_path, 'wb') as f:
            self.transform_xhwp5_to_css(xhwp5path, f)

    def transform_hwp5_to_single(self, hwp5file, outpath):
        """
        Convert HWP file to a single HTML file with embedded CSS and images.
        """
        # Create a temporary directory for intermediate conversion
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Perform standard conversion to temp dir
            self.transform_hwp5_to_dir(hwp5file, temp_dir)
            
            # Paths to generated files
            html_path = os.path.join(temp_dir, 'index.xhtml')
            css_path = os.path.join(temp_dir, 'styles.css')
            bindata_dir = os.path.join(temp_dir, 'bindata')
            
            # 2. Read HTML and CSS
            if os.path.exists(html_path):
                with io.open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            else:
                raise RuntimeError("HTML generation failed")
                
            css_content = ""
            if os.path.exists(css_path):
                with io.open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
            
            # 3. Embed CSS
            # Insert <style> tag before </head>
            if css_content:
                style_tag = f'<style>\n{css_content}\n</style>\n'
                html_content = html_content.replace('</head>', f'{style_tag}</head>')
                # Remove external link to css if present (optional, but good practice)
                # <link rel="stylesheet" type="text/css" href="styles.css" />
                html_content = re.sub(r'<link[^>]+href="styles.css"[^>]*/>', '', html_content)

            # 4. Embed Images
            if os.path.exists(bindata_dir):
                # Function to replace image src with base64 data
                def replace_image(match):
                    src = match.group(1)
                    if src.startswith('bindata/'):
                        image_filename = os.path.basename(src)
                        image_path = os.path.join(bindata_dir, image_filename)
                        if os.path.exists(image_path):
                            # Guess mime type
                            mime_type, _ = mimetypes.guess_type(image_path)
                            if not mime_type:
                                mime_type = 'image/png' # Default fallback
                                
                            with open(image_path, 'rb') as img_f:
                                img_data = img_f.read()
                                b64_data = base64.b64encode(img_data).decode('ascii')
                                return f'src="data:{mime_type};base64,{b64_data}"'
                    return match.group(0) # Return original if not matched/found
                
                # Replace src="bindata/..." with data URI
                # Regex looks for src="bindata/[^"]+"
                html_content = re.sub(r'src="(bindata/[^"]+)"', replace_image, html_content)
            
            # 5. Write final output
            with io.open(outpath, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def extract_bindata_dir(self, hwp5file, bindata_dir):
        if 'BinData' not in hwp5file:
            return
        bindata_stg = hwp5file['BinData']
        if not os.path.exists(bindata_dir):
            os.mkdir(bindata_dir)

        from hwp5.storage import unpack
        unpack(bindata_stg, bindata_dir)


def main():
    from .dataio import ParseError
    from .errors import InvalidHwp5FileError
    from .utils import make_open_dest_file
    from .xmlmodel import Hwp5File

    argparser = main_argparser()
    args = argparser.parse_args()
    init_logger(args)

    hwp5path = args.hwp5file

    html_transform = HTMLTransform()

    open_dest = make_open_dest_file(args.output)
    if args.css:
        transform = html_transform.transform_hwp5_to_css
        open_dest = wrap_for_css(open_dest)
    elif args.html:
        transform = html_transform.transform_hwp5_to_xhtml
        open_dest = wrap_for_xml(open_dest)
    elif args.embed_image:
        transform = html_transform.transform_hwp5_to_single
        # For single file, we need a file path, not a file object
        # transform_hwp5_to_single expects a path string
        if not args.output:
            args.output = os.path.splitext(os.path.basename(hwp5path))[0] + '.html'
        open_dest = lambda: contextmanager(lambda: (yield args.output))()
    else:
        transform = html_transform.transform_hwp5_to_dir
        dest_path = args.output
        if not dest_path:
            dest_path = os.path.splitext(os.path.basename(hwp5path))[0]
        open_dest = partial(open_dir, dest_path)

    print(f"DEBUG: Input file: {hwp5path}")
    print(f"DEBUG: Args: css={args.css}, html={args.html}, embed_image={getattr(args, 'embed_image', False)}")

    try:
        with closing(Hwp5File(hwp5path)) as hwp5file:
            with open_dest() as dest:
                print(f"DEBUG: Starting transformation using {transform}")
                transform(hwp5file, dest)
                print("DEBUG: Transformation finished")
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error('%s', e)
        sys.exit(1)


def main_argparser():
    parser = ArgumentParser(
        prog='hwp5html',
        description=_('HWPv5 to HTML converter'),
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(version)
    )
    parser.add_argument(
        '--loglevel',
        help=_('Set log level.'),
    )
    parser.add_argument(
        '--logfile',
        help=_('Set log file.'),
    )
    parser.add_argument(
        '--output',
        help=_('Output file'),
    )
    parser.add_argument(
        'hwp5file',
        metavar='<hwp5file>',
        help=_('.hwp file to convert'),
    )
    generator_group = parser.add_mutually_exclusive_group()
    generator_group.add_argument(
        '--css',
        action='store_true',
        help=_('Generate CSS'),
    )
    generator_group.add_argument(
        '--html',
        action='store_true',
        help=_('Generate HTML'),
    )
    generator_group.add_argument(
        '--embed-image',
        action='store_true',
        help=_('Embed images and CSS into a single HTML file'),
    )
    return parser


@contextmanager
def open_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    yield path


def wrap_for_css(open_dest):
    from .utils import wrap_open_dest_for_tty
    from .utils import pager
    from .utils import syntaxhighlight
    return wrap_open_dest_for_tty(open_dest, [
        pager(),
        syntaxhighlight('text/css'),
    ])


def wrap_for_xml(open_dest):
    from .utils import wrap_open_dest_for_tty
    from .utils import pager
    from .utils import syntaxhighlight
    from .utils import xmllint
    return wrap_open_dest_for_tty(open_dest, [
        pager(),
        syntaxhighlight('application/xml'),
        xmllint(format=True, nonet=True),
    ])


if __name__ == '__main__':
    main()
