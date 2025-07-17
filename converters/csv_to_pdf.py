#!/usr/bin/env python3
"""
CSV to Professional PDF Converter

This script converts CSV files into beautifully formatted PDF documents
with professional styling, headers, footers, and automatic table formatting.

Requirements:
pip install pandas reportlab

Usage:
python csv_to_pdf.py input.csv output.pdf
"""

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import sys
import os
from datetime import datetime

class NumberedCanvas(canvas.Canvas):
    """Custom canvas class to add page numbers and headers/footers"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.page_count = 0

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        self.page_count += 1

    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, state) in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, total_pages):
        """Draw page number at bottom of page"""
        self.setFont("Helvetica", 9)
        self.drawRightString(letter[0] - 0.75 * inch, 0.75 * inch, 
                           f"Page {page_num} of {total_pages}")
        
        # Add generation timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.drawString(0.75 * inch, 0.75 * inch, 
                       f"Generated: {timestamp}")

def create_professional_pdf(csv_file, output_file, title=None):
    """
    Convert CSV to professional PDF with beautiful formatting
    
    Args:
        csv_file (str): Path to input CSV file
        output_file (str): Path to output PDF file
        title (str): Optional title for the document
    """
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2C3E50')
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#34495E')
        )
        
        # Build document content
        story = []
        
        # Add title
        if title:
            story.append(Paragraph(title, title_style))
        else:
            file_name = os.path.splitext(os.path.basename(csv_file))[0]
            story.append(Paragraph(f"Data Report: {file_name.replace('_', ' ').title()}", title_style))
        
        # Add summary information
        summary_text = f"""
        <b>Summary Information:</b><br/>
        • Total Records: {len(df)}<br/>
        • Total Columns: {len(df.columns)}<br/>
        • Source File: {os.path.basename(csv_file)}<br/>
        • Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Prepare data for table
        data = []
        
        # Add headers
        headers = list(df.columns)
        data.append(headers)
        
        # Add data rows
        for _, row in df.iterrows():
            # Convert all values to strings and handle NaN values
            row_data = []
            for val in row:
                if pd.isna(val):
                    row_data.append("")
                else:
                    # Truncate long strings to prevent table overflow
                    str_val = str(val)
                    if len(str_val) > 50:
                        str_val = str_val[:47] + "..."
                    row_data.append(str_val)
            data.append(row_data)
        
        # Calculate column widths based on content
        col_widths = []
        available_width = 7 * inch  # Total available width
        
        for i, col in enumerate(headers):
            # Calculate max width needed for this column
            max_width = len(col)
            for row in data[1:]:  # Skip header row
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width)
        
        # Normalize column widths
        total_width = sum(col_widths)
        if total_width > 0:
            col_widths = [available_width * (w / total_width) for w in col_widths]
        else:
            col_widths = [available_width / len(headers)] * len(headers)
        
        # Create table
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Apply professional table style
        table_style = TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ])
        
        # Add alternating row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9FA'))
            else:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.white)
        
        table.setStyle(table_style)
        
        # Add table to story
        story.append(table)
        
        # Add data statistics if numeric columns exist
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Statistical Summary", subtitle_style))
            
            stats_text = "<b>Numeric Column Statistics:</b><br/><br/>"
            for col in numeric_cols:
                stats = df[col].describe()
                stats_text += f"<b>{col}:</b><br/>"
                stats_text += f"• Count: {stats['count']:.0f}<br/>"
                stats_text += f"• Mean: {stats['mean']:.2f}<br/>"
                stats_text += f"• Std: {stats['std']:.2f}<br/>"
                stats_text += f"• Min: {stats['min']:.2f}<br/>"
                stats_text += f"• Max: {stats['max']:.2f}<br/><br/>"
            
            story.append(Paragraph(stats_text, styles['Normal']))
        
        # Build PDF with custom canvas for page numbers
        doc.build(story, canvasmaker=NumberedCanvas)
        
        print(f"✅ Successfully converted {csv_file} to {output_file}")
        print(f"📊 Processed {len(df)} rows and {len(df.columns)} columns")
        
    except FileNotFoundError:
        print(f"❌ Error: CSV file '{csv_file}' not found.")
        return False
    except pd.errors.EmptyDataError:
        print(f"❌ Error: CSV file '{csv_file}' is empty.")
        return False
    except Exception as e:
        print(f"❌ Error converting CSV to PDF: {str(e)}")
        return False
    
    return True

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 3:
        print("Usage: python csv_to_pdf.py <input.csv> <output.pdf> [title]")
        print("Example: python csv_to_pdf.py data.csv report.pdf 'Monthly Sales Report'")
        return
    
    input_csv = sys.argv[1]
    output_pdf = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Check if input file exists
    if not os.path.exists(input_csv):
        print(f"❌ Error: Input file '{input_csv}' does not exist.")
        return
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_pdf)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert CSV to PDF
    success = create_professional_pdf(input_csv, output_pdf, title)
    
    if success:
        print(f"🎉 PDF successfully created: {output_pdf}")
        print(f"📄 You can now open the PDF file to view your professional report.")

if __name__ == "__main__":
    main()