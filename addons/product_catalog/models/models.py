# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import logging
_logger = logging.getLogger(__name__)


class CatalogGenerator(models.TransientModel):
    _name = 'catalog.generator'
    _description = 'Product Catalog Generator'

    parent_id = fields.Many2one(
        'product.category',
        string="eCommerce Category",
        help="Select the eCommerce category to generate the catalog for."
    )
    catalog_file = fields.Binary("Catalog File", readonly=True)
    file_name = fields.Char("File Name", default='product_catalog.pdf', readonly=True)

    def generate_catalog(self):
        """Generates a PDF catalog."""

        if not self.parent_id:
            raise UserError("Please select a category to generate the catalog.")

        # Fetch products in the selected eCommerce category
        products = self.env['product.template'].search([
            ('public_categ_ids', 'in', self.parent_id.id)
        ])

        if not products:
            raise UserError("No products found in the selected category.")

        pdf_data = self._generate_pdf_data(products)
        self.catalog_file = base64.encodebytes(pdf_data)
        self.file_name = f"catalog_{self.parent_id.name.replace(' ', '_').lower()}.pdf"

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'catalog.generator',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def _generate_pdf_data(self, products):
        """Generate the PDF content using ReportLab."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']

        elements = []
        table_data = [['Name', 'Category', 'Price']]

        for product in products:
            table_data.append([
                Paragraph(product.name or '', normal_style),
                Paragraph(product.categ_id.name or "No Category", normal_style),
                Paragraph(f"{product.list_price:.2f}", normal_style)
            ])

        table = Table(table_data)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ])
        table.setStyle(table_style)
        elements.append(table)

        doc.build(elements)
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
