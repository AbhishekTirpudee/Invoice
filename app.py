
from flask import Flask, render_template, request, jsonify, send_file
from main import Client, Item, Invoice, generate_pdf
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json

    # Create client
    client = Client(
        name=data['client']['name'],
        email=data['client']['email'],
        address=data['client']['address'],
        contact=data['client'].get('phone')
    )

    # Create invoice
    invoice = Invoice(client)

    # Add each item
    for item_data in data['items']:
        charge_types = item_data.get('charge_types', [])
        charge_amounts = item_data.get('charge_amounts', [])

        # Ensure both lists are the same length
        max_len = max(len(charge_types), len(charge_amounts))
        charge_types += [''] * (max_len - len(charge_types))
        charge_amounts += [0.0] * (max_len - len(charge_amounts))

        item = Item(
            name=item_data['name'],
            qty=int(item_data['quantity']),
            price=float(item_data['price']),
            charge_types=charge_types,
            charge_amounts=[float(a) for a in charge_amounts]
        )
        invoice.add_item(item)

    if 'tax_rate' in data:
        invoice.set_tax_rate(float(data['tax_rate']))
    if 'discount' in data:
        invoice.set_discount(float(data['discount']), data.get('discount_type', 'flat'))

    # Generate PDF and return download link
    pdf_filename = generate_pdf(invoice)

    return jsonify({
        'success': True,
        'invoice_number': invoice.invoice_number,
        'pdf_url': f'/download/{pdf_filename}'
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
