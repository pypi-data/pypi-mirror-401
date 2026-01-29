import io

import pdf_liner.constants as constants

from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfReader, PdfWriter

from pdf_liner.arg_parser import parse_args

def add_lines_to_pdf(
    input_pdf_path: str,
    output_pdf_path: str,
    line_spacing: float,
    line_opacity: float,
    padding: bool,
    enhance_bottom_lines: int
):
    """
    Add equally spaced horizontal lines to all pages of a PDF.
    
    Args:
        input_pdf_path: Path to the input PDF file
        output_pdf_path: Path to save the output PDF file
        line_spacing: Space between lines in points (default: 30)
        line_opacity: Opacity of lines from 0.0 to 1.0 (default: 0.3)
        padding: If True, adds a white page with lines after each page (default: False)
        enhance_bottom_lines: Number of bottom lines to make thicker/darker to prevent printer fade
    """
    
    print(f"[pdf](input): {input_pdf_path}")
    
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    print(f"[pdf](pages): {total_pages}")
    
    for page_num, page in enumerate(reader.pages, 1):
        # print(f"[pdf]({page_num}/{total_pages}): completed")
        
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        packet = io.BytesIO()
        canvas = Canvas(packet, pagesize=(page_width, page_height))
        
        canvas.setStrokeColorRGB(*constants.DEFAULT_LINE_STROKE_COLOR)
        canvas.setStrokeAlpha(line_opacity)
        canvas.setLineWidth(constants.DEFAULT_LINE_WIDTH)
        
        line_positions = []
        y_position = line_spacing
        while y_position < page_height:
            line_positions.append(y_position)
            y_position += line_spacing
        
        for i, y_pos in enumerate(line_positions):
            is_bottom_line = i < enhance_bottom_lines
            
            if is_bottom_line and enhance_bottom_lines > 0:
                enhancement_factor = 1.5 + (enhance_bottom_lines - i) * 0.3
                canvas.setLineWidth(constants.DEFAULT_LINE_WIDTH * enhancement_factor)
                canvas.setStrokeAlpha(min(1.0, line_opacity * enhancement_factor))
            else:
                canvas.setLineWidth(constants.DEFAULT_LINE_WIDTH)
                canvas.setStrokeAlpha(line_opacity)
            
            canvas.line(0, y_pos, page_width, y_pos)
        
        canvas.save()
        
        packet.seek(0)
        
        lines_pdf = PdfReader(packet)
        lines_page = lines_pdf.pages[0]
        
        page.merge_page(lines_page)
        
        writer.add_page(page)
        
        if padding:
            blank_packet = io.BytesIO()
            blank_canvas = Canvas(blank_packet, pagesize=(page_width, page_height))
            
            blank_canvas.setFillColorRGB(1, 1, 1)
            blank_canvas.rect(0, 0, page_width, page_height, fill=True, stroke=False)
            
            blank_canvas.setStrokeColorRGB(*constants.DEFAULT_LINE_STROKE_COLOR)
            blank_canvas.setStrokeAlpha(line_opacity)
            blank_canvas.setLineWidth(constants.DEFAULT_LINE_WIDTH)
            
            line_positions = []
            y_position = line_spacing
            while y_position < page_height:
                line_positions.append(y_position)
                y_position += line_spacing
            
            for i, y_pos in enumerate(line_positions):
                is_bottom_line = i < enhance_bottom_lines
                
                if is_bottom_line and enhance_bottom_lines > 0:
                    enhancement_factor = 1.5 + (enhance_bottom_lines - i) * 0.3
                    blank_canvas.setLineWidth(constants.DEFAULT_LINE_WIDTH * enhancement_factor)
                    blank_canvas.setStrokeAlpha(min(1.0, line_opacity * enhancement_factor))
                else:
                    blank_canvas.setLineWidth(constants.DEFAULT_LINE_WIDTH)
                    blank_canvas.setStrokeAlpha(line_opacity)
                
                blank_canvas.line(0, y_pos, page_width, y_pos)
            
            blank_canvas.save()
            
            blank_packet.seek(0)
            blank_pdf = PdfReader(blank_packet)
            blank_page = blank_pdf.pages[0]
            
            writer.add_page(blank_page)
    
    print(f"[pdf](output): {output_pdf_path}")
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)
    
    print("[pdf]: completed")

def main():
    args = parse_args()
    
    add_lines_to_pdf(
        input_pdf_path=args.input_pdf,
        output_pdf_path=args.output_pdf,
        line_spacing=args.line_spacing,
        line_opacity=args.opacity,
        padding=args.padding,
        enhance_bottom_lines=args.enhance_bottom_lines
    )

if __name__ == "__main__":
    main()
