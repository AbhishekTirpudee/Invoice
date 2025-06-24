💼 PDF Invoice Generator
A powerful and user-friendly Flask-based web application to generate professional PDF invoices with dynamic items and charges. Built using Python, Flask, ReportLab, and Tailwind CSS.

✨ Features
🖥️ Clean, responsive web UI using Tailwind CSS

➕ Add multiple items, each with:

Quantity & Price

Custom charge types (e.g., Development, Hosting, Subscription)

Charge values per type

👤 Input client details (name, email, phone, address)

🧾 Apply tax rate and flat or percentage discount

📥 Generates downloadable PDF invoice instantly

🔒 All data processed locally – no external storage or DB

🖼️ Demo Screenshot
(Replace this with your actual app screenshot)



📦 Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/PDF-Invoice-Generator.git
cd PDF-Invoice-Generator
2. Create a Virtual Environment (optional but recommended)
bash
Copy code
python -m venv invoice_env
invoice_env\Scripts\activate  # For Windows
# OR
source invoice_env/bin/activate  # For macOS/Linux
3. Install Required Dependencies
bash
Copy code
pip install -r requirements.txt
Or manually:

bash
Copy code
pip install Flask reportlab
🚀 Usage
1. Run the App
bash
Copy code
python app.py
2. Open in Browser
Visit: http://127.0.0.1:5000/

3. Fill the Form
Add client info

Add items and charges

Apply tax and discount

Generate the invoice PDF

📁 Project Structure
php
Copy code
PDF-Invoice-Generator/
├── app.py               # Flask web server
├── main.py              # Invoice logic & PDF rendering
├── templates/
│   └── index.html       # Web frontend (Tailwind CSS UI)
├── .gitignore           # Git ignored files (PDFs, venv, etc.)
├── requirements.txt     # Python dependencies
├── Procfile             # For deployment on Render/Heroku
└── README.md            # This file
🌐 Free Hosting (Optional)
You can host this app for free using Render or Railway.

📚 Dependencies
Flask – Web server

ReportLab – PDF generation

Install all with:

bash
Copy code
pip install Flask reportlab
🙌 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

📬 Contact
GitHub Issues: Open an issue

Maintainer
