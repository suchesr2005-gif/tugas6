from flask import Flask, render_template, send_file
import tempfile, os

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

app = Flask(__name__)

# ================= DATA =================
data = {
    "nama": "Suci Ramadani",
    "judul": "Mahasiswi Informatika",
    "tentang": [
        "Nama                  :Suci Ramadani",
        "Tempat/Tanggal Lahir  :Laburunci, 10 November 2005",
        "Alamat                :Pasarwajo, Kab. Buton, Sulawesi Tenggara",
        "Hobi :Main Game, Multimedia" 
    ],
    "email": "rsuci2010@gmail.com",
    "telepon": "082346414697",
    "facebook": "https://www.facebook.com/share/1C86WBbAtG/",
    "instagram": "https://www.instagram.com/suci._rmdn?igsh=YnVndXF2NjYwdDBv",

    "skills": ["Public Speaking", "Paper Craft", "Bikin Kue"],
    "pendidikan": [
        ["2011-2017", "SD NEGERI 68 Buton"],
        ["2017-2020", "SMP NEGERI 1 Buton"],
        ["2020-2023", "SMA NEGERI 1 Pasarwajo"],
        ["2024-Sekarang", "UNIVERSITAS DAYANU IKHSANUDIN PASARWAJO"]
    ],

    "pengalaman": [
        "Anggota Organisasi HMTI", 
        "Ikut lomba HACKATHON perwakilan team Pasarwajo",
    ]
}

# ================= ROUTES WEB =================
@app.route("/")
def home():
    return render_template("home.html", data=data)

@app.route("/tentang")
def tentang():
    return render_template("profile.html", data=data)

@app.route("/skills")
def skills():
    return render_template("skills.html", data=data)

@app.route("/education")
def education():
    return render_template("educations.html", data=data)

@app.route("/experience")
def experience():
    return render_template("experience.html", data=data)

@app.route("/contact")
def contact():
    return render_template("contact.html", data=data)

from reportlab.platypus import Table, TableStyle

from reportlab.platypus import Table, TableStyle

@app.route("/download")
def download():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    
    # Gunakan margin standar agar aman
    doc = SimpleDocTemplate(
        tmp.name,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1.2*cm,
        bottomMargin=1.2*cm
    )

    styles = getSampleStyleSheet()
    warna_utama = colors.HexColor("#22c55e")
    
    # ----- SETTING STYLE AGAR FULL -----
    # Nama dibuat sangat besar dan tegas
    style_name = ParagraphStyle("Name", fontSize=32, textColor=warna_utama, fontName="Helvetica-Bold", spaceAfter=15)
    style_sub = ParagraphStyle("Sub", fontSize=16, textColor=colors.grey, spaceAfter=40)
    
    # Section Heading dengan spasi besar
    style_section = ParagraphStyle(
        "Section", 
        fontSize=18, 
        textColor=warna_utama, 
        fontName="Helvetica-Bold", 
        spaceBefore=30, 
        spaceAfter=15
    )
    
    # Sidebar style
    style_side_title = ParagraphStyle("SideTitle", fontSize=15, textColor=colors.white, fontName="Helvetica-Bold", spaceAfter=15)
    style_side_text = ParagraphStyle("SideText", fontSize=12, textColor=colors.white, leading=22, spaceAfter=15)
    
    # Main Content style dengan leading (jarak baris) yang luas
    style_main_text = ParagraphStyle("MainText", fontSize=13, leading=22, spaceAfter=12)

    # ----- SIDEBAR CONTENT -----
    # ----- SIDEBAR CONTENT (Kiri) -----
    sidebar_elements = []
    img_path = os.path.join("static", "img", "image.png")
    if os.path.exists(img_path):
        img = Image(img_path, 4.5*cm, 4.5*cm)
        sidebar_elements.append(img)
        sidebar_elements.append(Spacer(1, 40))

    # KONTAK
    sidebar_elements.append(Paragraph("KONTAK", style_side_title))
    sidebar_elements.append(Paragraph(f"📧 {data['email']}", style_side_text))
    sidebar_elements.append(Paragraph(f"📞 {data['telepon']}", style_side_text))
    
    # SOSIAL MEDIA (Ditambahkan kembali)
    sidebar_elements.append(Spacer(1, 20))
    sidebar_elements.append(Paragraph("SOSIAL MEDIA", style_side_title))
    sidebar_elements.append(Paragraph(f"🌐 FB: Suci Ramadani", style_side_text))
    sidebar_elements.append(Paragraph(f"📷 IG: @suci._rmdn", style_side_text))
    
    # KEAHLIAN
    sidebar_elements.append(Spacer(1, 30))
    sidebar_elements.append(Paragraph("KEAHLIAN", style_side_title))
    for s in data["skills"]:
        sidebar_elements.append(Paragraph(f"• {s}", style_side_text))
    # ----- MAIN CONTENT -----
    main_elements = []
    main_elements.append(Paragraph(data["nama"].upper(), style_name))
    main_elements.append(Paragraph(data["judul"], style_sub))

    # Di dalam fungsi download() bagian TENTANG SAYA:
    main_elements.append(Paragraph("TENTANG SAYA", style_section))
    
    # Buat tabel mini untuk data diri agar titik dua sejajar
    tentang_data = []
    for t in data["tentang"]:
        if ":" in t:
            label, isi = t.split(":", 1)
            tentang_data.append([label.strip(), ":", isi.strip()])
    
    # Lebar kolom: Label 4cm, Titik dua 0.5cm, Isi 7cm
    tabel_tentang = Table(tentang_data, colWidths=[4*cm, 0.5*cm, 7*cm])
    tabel_tentang.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10), # Kasih jarak antar baris
        ('FONTNAME', (0,0), (0,-1), 'Helvetica'),
    ]))
    main_elements.append(tabel_tentang)

    # ===== PENDIDIKAN (Style Baru dengan Timeline) =====
    main_elements.append(Paragraph("PENDIDIKAN", style_section))
    
    edu_data = []
    for item in data["pendidikan"]:
        # Karena data berupa list [Tahun, Sekolah]
        tahun = item[0]
        sekolah = item[1]
        
        # Kolom kiri: Tahun, Kolom kanan: Detail Sekolah
        edu_data.append([
            Paragraph(tahun, style_main_text),
            Paragraph(f"{sekolah}<br/><font color='#666666' size='9'>Pendidikan Formal</font>", style_main_text)
        ])

    # Membuat tabel untuk pendidikan agar sejajar
    # Lebar kolom 1: 3.5cm (Tahun), Kolom 2: 8cm (Sekolah)
    edu_table = Table(edu_data, colWidths=[3.5*cm, 8*cm])
    
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5), # Jarak antar sekolah
        # Menambahkan garis vertikal hijau di antara tahun dan sekolah
        ('LINESTART', (1, 0), (1, -1), 2, warna_utama), 
        ('PADDINGLEFT', (1, 0), (1, -1), 12),
    ]))
    
    main_elements.append(edu_table)

    main_elements.append(Paragraph("PENGALAMAN", style_section))
    for e in data["pengalaman"]:
        main_elements.append(Paragraph(f"• {e}", style_main_text))

    # ----- LAYOUT TABEL (Aman & Full) -----
    table_data = [[sidebar_elements, main_elements]]
    
    # Tinggi baris dikurangi sedikit ke 26cm agar ada ruang untuk margin doc
    cv_table = Table(table_data, colWidths=[7.5*cm, 11.5*cm], rowHeights=[26.5*cm])
    
    cv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), warna_utama), 
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 25),
        ('RIGHTPADDING', (0, 0), (0, 0), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 35),
    ]))

    story = [cv_table]
    doc.build(story)

    return send_file(tmp.name, as_attachment=True, download_name=f"CV_{data['nama']}_Full.pdf")
# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
