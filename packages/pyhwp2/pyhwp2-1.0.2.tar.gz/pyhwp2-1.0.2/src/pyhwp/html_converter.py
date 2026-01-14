# -*- coding: utf-8 -*-
"""
HWP to HTML Converter module.
"""
import os

from hwp5.hwp5html import HTMLTransform
from hwp5.xmlmodel import Hwp5File
from contextlib import closing

class HwpToHtmlConverter:
    def __init__(self, hwp_file):
        self.hwp_file = hwp_file

    def convert(self, output_path):
        """
        Convert the HWP file to HTML.
        :param output_path: Path to save the generated HTML file.
        """
        if not os.path.exists(self.hwp_file):
             raise FileNotFoundError(f"HWP file not found: {self.hwp_file}")

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Use HTMLTransform from hwp5 package
        # The existing transform_hwp5_to_xhtml takes a file path or file object
        # but transform_hwp5_to_xhtml in HTMLTransform returns a transform function
        # We need to instantiate HTMLTransform and use its methods correctly.
        
        # Looking at hwp5html.py:
        # transform = html_transform.transform_hwp5_to_xhtml
        # transform(hwp5file, dest) 
        
        transformer = HTMLTransform()
        output_dir = os.path.dirname(os.path.abspath(output_path))
        
        with closing(Hwp5File(self.hwp_file)) as hwp5file:
            with transformer.transformed_xhwp5_at_temp(hwp5file) as xhwp5path:
                # 1. Generage HTML
                with open(output_path, 'wb') as f:
                    transformer.transform_xhwp5_to_xhtml(xhwp5path, f)
                
                # 2. Generate CSS
                # The XSLT usually expects styles.css
                css_path = os.path.join(output_dir, 'styles.css')
                with open(css_path, 'wb') as f:
                    transformer.transform_xhwp5_to_css(xhwp5path, f)

            # 3. Extract BinData
            bindata_dir = os.path.join(output_dir, 'bindata')
            transformer.extract_bindata_dir(hwp5file, bindata_dir)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Convert HWP file to HTML with CSS and images.')
    parser.add_argument('input', help='Input HWP file')
    parser.add_argument('--output', '-o', help='Output HTML file path (default: input_filename.html)')

    args = parser.parse_args()

    input_file = args.input
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + '.html'

    try:
        converter = HwpToHtmlConverter(input_file)
        print(f"Converting '{input_file}' to '{output_file}'...")
        converter.convert(output_file)
        print("Conversion successful!")
        print(f"Generated files:")
        print(f" - HTML: {output_file}")
        print(f" - CSS:  {os.path.join(os.path.dirname(os.path.abspath(output_file)), 'styles.css')}")
        print(f" - Data: {os.path.join(os.path.dirname(os.path.abspath(output_file)), 'bindata')}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
