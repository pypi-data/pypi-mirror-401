#!/usr/bin/env python3
"""Generate PDF with QR codes for travel show samples."""

import qrcode
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import tempfile
import os

samples = [
    {"emoji": "🦁", "name": "Kenya Safari", "category": "Africa", "hash": "VZXkaQVofGTHR2l8q8Xdfn40YUNglijawBA4tGqn"},
    {"emoji": "🍝", "name": "Morocco Food Tour", "category": "Middle East", "hash": "jqjQML3fW7SzkcpzUaLy1LqMDV5tSnY0jpn79keN"},
    {"emoji": "🦜", "name": "Costa Rica Adventure", "category": "Latin America", "hash": "0ygNwmIDpX7fw4VSmszHGOId2akdxCCenbIKkxBy"},
    {"emoji": "🚢", "name": "Alaska Cruise", "category": "Cruise", "hash": "JUFaMLJM1D2ovXOmMDO0e0kLJtM69FoHaQuaGJHA"},
    {"emoji": "🤿", "name": "Thailand Scuba", "category": "Dive/Watersports", "hash": "hWCH1mOnmPRvC6Pl3jxDLvNr6xxNgljkwaQMNwzM"},
    {"emoji": "🍷", "name": "Tuscany Wine", "category": "Europe", "hash": "5z402OCqJ24cnAmleexZelCkmAbZV225RTZ2K9A4"},
    {"emoji": "🧘", "name": "Bali Wellness", "category": "Wellness", "hash": "rzmM414ErZTJAFJRmf0Yel8aVxp9Sh6CVGX6VEsA"},
    {"emoji": "💑", "name": "St. Lucia Honeymoon", "category": "Caribbean", "hash": "Kzipi1mVET5otdg6HfZDXeeWBmuiegeNf8KFm6ET"},
    {"emoji": "🏔️", "name": "Kilimanjaro Summit", "category": "Africa", "hash": "ueEbTWp5qOWRU7BPxUttFG6M3Qdgrgmlsph4iE84"},
    {"emoji": "💬", "name": "Sample Prompts", "category": "How It Works", "hash": "3YePoRPGH5xNiLKmivBvl6mYLmWlPrmzrfNvNmDC"},
]

booking_url = "https://book.squareup.com/appointments/qka7rptzqt4njx/location/4CWG2VP15JSJS/services/3WJPJ5DIHYAY4MWINUKZUZV4"
register_url = "https://mcp.factumerit.app/beta-signup?code=TRAVEL-ADVENTURE-SEATTLE-2026"

def generate_qr(url: str, size: int = 400) -> Image.Image:
    """Generate QR code image."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").get_image().resize((size, size))

def main():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)

    # Add DejaVu font for emoji support (fallback to helvetica if not available)
    try:
        pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
        font_name = "DejaVu"
    except:
        font_name = "helvetica"

    temp_files = []

    # First page: Booking QR
    pdf.add_page()
    pdf.set_font(font_name, size=28)
    pdf.set_y(40)
    pdf.cell(0, 15, "Book a Setup Call", ln=True, align="C")
    pdf.set_font(font_name, size=20)
    pdf.set_text_color(100, 102, 241)  # Indigo
    pdf.cell(0, 12, "$99 Show Special", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    # Generate and add booking QR
    qr_img = generate_qr(booking_url, 300)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        qr_img.save(f.name)
        temp_files.append(f.name)
        pdf.image(f.name, x=55, y=80, w=100)

    pdf.set_y(200)
    pdf.set_font(font_name, size=12)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, "Factum Erit - AI Trip Planning Setup", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    # Registration page
    pdf.add_page()
    pdf.set_font(font_name, size=28)
    pdf.set_y(40)
    pdf.cell(0, 15, "Try It Free", ln=True, align="C")
    pdf.set_font(font_name, size=18)
    pdf.set_text_color(39, 174, 96)  # Green
    pdf.cell(0, 12, "Create Your Account", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    # Generate and add registration QR
    qr_img = generate_qr(register_url, 300)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        qr_img.save(f.name)
        temp_files.append(f.name)
        pdf.image(f.name, x=55, y=80, w=100)

    pdf.set_y(195)
    pdf.set_font(font_name, size=14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Code: TRAVEL-ADVENTURE-SEATTLE-2026", ln=True, align="C")
    pdf.set_y(210)
    pdf.set_font(font_name, size=11)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, "Scan to sign up and start planning", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    # Sample pages
    for sample in samples:
        pdf.add_page()

        # Title (name only, no emoji due to font issues)
        pdf.set_font(font_name, size=32)
        pdf.set_y(35)
        pdf.cell(0, 18, sample["name"], ln=True, align="C")

        # Category
        pdf.set_font(font_name, size=18)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 12, sample["category"], ln=True, align="C")
        pdf.set_text_color(0, 0, 0)

        # QR code
        url = f"https://vikunja.factumerit.app/share/{sample['hash']}/auth"
        qr_img = generate_qr(url, 350)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            qr_img.save(f.name)
            temp_files.append(f.name)
            pdf.image(f.name, x=45, y=75, w=120)

        # Footer with URL
        pdf.set_y(220)
        pdf.set_font(font_name, size=9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, "Scan to view sample trip plan", ln=True, align="C")
        pdf.set_text_color(0, 0, 0)

    # Save PDF
    output_path = "travel-show-qr-codes.pdf"
    pdf.output(output_path)
    print(f"Generated: {output_path}")

    # Cleanup temp files
    for f in temp_files:
        os.unlink(f)

if __name__ == "__main__":
    main()
