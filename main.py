from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

@dataclass
class Client:
    name: str
    email: str
    address: str
    contact: Optional[int] = None

@dataclass
class Item:
    name: str
    qty: float
    price: float
    charge_types: List[str] = None
    charge_amounts: List[float] = None

    def price_cal(self):
        base = self.qty * self.price
        extras = sum(self.charge_amounts or [])
        return base + extras

class Invoice:
    def __init__(self, client):
        self.client = client
        self.items = []
        self.invoice_date = datetime.now()
        self.invoice_number = f"INV-{id(self)}"
        self.tax_rate: float = 0.0
        self.discount = 0.0
        self.discount_type = 'flat'

    def add_item(self, item):
        self.items.append(item)

    def set_tax_rate(self, rate):
        self.tax_rate = rate

    def set_discount(self, amount, discount_type):
        self.discount = amount
        self.discount_type = discount_type

def calculate_subtotal(items):
    return sum(item.price_cal() for item in items)

def apply_discount(subtotal, discount, discount_type):
    return subtotal * (1 - discount) if discount_type == 'percentage' else subtotal - discount

def apply_tax(amount, tax_rate):
    return amount * (1 + tax_rate)

def format_currency(amount):
    return f"${amount:.2f}"  # USD


def generate_pdf(invoice, filename=None):
    if filename is None:
        filename = f"invoice_{invoice.invoice_number}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("INVOICE", ParagraphStyle('title', parent=styles['Heading1'], fontSize=24, spaceAfter=20)))
    elements.append(Paragraph(f"Invoice Number: {invoice.invoice_number}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {invoice.invoice_date.strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Client Information:", styles["Heading2"]))
    elements.append(Paragraph(f"Name: {invoice.client.name}", styles["Normal"]))
    elements.append(Paragraph(f"Email: {invoice.client.email}", styles["Normal"]))
    elements.append(Paragraph(f"Address: {invoice.client.address}", styles["Normal"]))
    if invoice.client.contact:
        elements.append(Paragraph(f"Phone: {invoice.client.contact}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Items:", styles["Heading2"]))

    data = [["Item Name", "Qty", "Price", "Charges", "Total"]]
    for item in invoice.items:
        charge_lines = []
        if item.charge_types and item.charge_amounts:
            for ct, ca in zip(item.charge_types, item.charge_amounts):
                charge_lines.append(f"{ct}: {format_currency(ca)}")
        charge_str = "<br />".join(charge_lines) if charge_lines else "-"

        data.append([
            item.name,
            str(item.qty),
            format_currency(item.price),
            Paragraph(charge_str, styles["Normal"]),
            format_currency(item.price_cal())
        ])

    table = Table(data, colWidths=[2*inch, 0.75*inch, 1*inch, 2.75*inch, 1.25*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    subtotal = calculate_subtotal(invoice.items)
    discounted = apply_discount(subtotal, invoice.discount, invoice.discount_type)
    total = apply_tax(discounted, invoice.tax_rate)

    elements.append(Paragraph(f"Subtotal: {format_currency(subtotal)}", styles["Normal"]))
    elements.append(Paragraph(f"Discount: {format_currency(invoice.discount)}", styles["Normal"]))
    elements.append(Paragraph(f"Tax ({invoice.tax_rate*100:.1f}%): {format_currency(subtotal * invoice.tax_rate)}", styles["Normal"]))
    elements.append(Paragraph(f"Total: {format_currency(total)}", styles["Heading2"]))

    doc.build(elements)
    return filename

