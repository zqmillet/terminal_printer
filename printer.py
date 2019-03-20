import sys

from fpdf import FPDF

pdf = FPDF()
pdf.compress = False
pdf.add_page()
pdf.set_font('Courier', '', 14)
pdf.set_text_color(255, 0, 0)
pdf.set_fill_color(0, 255, 0)
pdf.cell(3, 6, 'h', 0, 0, fill = True, align = 'C')
pdf.cell(3, 6, 'h', 0, 0, fill = True, align = 'C')
pdf.cell(3, 6, ' ', 0, 0, fill = True, align = 'C')
pdf.cell(3, 6, 'h', 0, 0, fill = True, align = 'C')
pdf.cell(3, 6, 'h', 0, 0, fill = True, align = 'C')
pdf.output('py3k.pdf', 'F')
