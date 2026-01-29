import argparse

DEFAULT_LINE_SPACING = 20
DEFAULT_LINE_OPACITY = 0.25
DEFAULT_ENHANCE_BOTTOM_LINES = 3

def create_parser():
    parser = argparse.ArgumentParser(
        description='Add equally spaced horizontal lines to PDF files for handwriting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf
  %(prog)s input.pdf -o output.pdf
  %(prog)s input.pdf -o output.pdf -s 25 -a 0.2
  %(prog)s input.pdf --line-spacing 30 --opacity 0.4

Tips:
  - For regular writing: Use spacing of 20-30 points
  - For large handwriting: Use spacing of 35-45 points
  - For subtle lines: Use opacity of 0.2-0.3
  - For more visible lines: Use opacity of 0.4-0.6
        """
    )
    
    parser.add_argument(
        'input_pdf',
        help='Path to the input PDF file'
    )
    
    parser.add_argument(
        '-p', '--padding',
        dest='padding',
        action='store_true',
        help='Adds a white page with lines after each page.'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_pdf',
        type=str,
        default=None,
        help='Path to the output PDF file (default: input_lined.pdf)'
    )
    
    parser.add_argument(
        '-s', '--line-spacing',
        dest='line_spacing',
        type=float,
        default=DEFAULT_LINE_SPACING,
        help=f'Space between lines in points (default: {DEFAULT_LINE_SPACING})'
    )
    
    parser.add_argument(
        '-a', '--opacity',
        dest='opacity',
        type=float,
        default=DEFAULT_LINE_OPACITY,
        help=f'Line opacity from 0.0 (invisible) to 1.0 (solid) (default: {DEFAULT_LINE_OPACITY})'
    )
    
    parser.add_argument(
        '-e', '--enhance-bottom-lines',
        dest='enhance_bottom_lines',
        type=int,
        default=DEFAULT_ENHANCE_BOTTOM_LINES,
        help=f'Number of bottom lines to enhance (thicker/darker) to prevent printer fade (default: {DEFAULT_ENHANCE_BOTTOM_LINES}, 0 to disable)'
    )
    
    return parser

def parse_args():
    parser = create_parser()
    args = parser.parse_args()
    
    if not 0.0 <= args.opacity <= 1.0:
        parser.error(f'Opacity must be between 0.0 and 1.0, got: {args.opacity}')
    
    if args.line_spacing <= 0:
        parser.error(f'Line spacing must be positive, got: {args.line_spacing}')
    
    if args.enhance_bottom_lines < 0:
        parser.error(f'Enhance bottom lines must be non-negative, got: {args.enhance_bottom_lines}')
    
    if args.output_pdf is None:
        args.output_pdf = args.input_pdf.rsplit('.', 1)[0] + '_lined.pdf'
    
    return args
