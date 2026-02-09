from datetime import datetime, timedelta

parkir_aktif = []
riwayat_parkir = []

TARIF = {
    "mobil": 5000,
    "motor": 2000,
    "lain": 3000
}

# Tanggal mulai (16 Jan 2026)
start_date = datetime(2026, 1, 16)

# Kendaraan contoh
kendaraan_sample = [
    {"plat": "111", "jenis": "motor", "merk": "Vario"},
    {"plat": "101", "jenis": "motor", "merk": "Beat"},
    {"plat": "222", "jenis": "mobil", "merk": "Avanza"},
    {"plat": "201", "jenis": "mobil", "merk": "Pick Up"},
    {"plat": "102", "jenis": "motor", "merk": "Pick Up"},
    {"plat": "103", "jenis": "motor", "merk": "Supra"},
    {"plat": "202", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "208", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "209", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "210", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "211", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "212", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "213", "jenis": "mobil", "merk": "Suzuki"},
    {"plat": "113", "jenis": "motor", "merk": "Suzuki"},
]

# Generate riwayat dari 16 Jan sampai 10 Jan (mundur 7 hari)
for day_offset in range(0, 7):
    tanggal = start_date - timedelta(days=day_offset)  # mundur
    for idx, k in enumerate(kendaraan_sample):
        # Variasi jam agar tidak sama persis
        masuk_time = tanggal.replace(hour=9 + idx % 8, minute=0 + idx % 60, second=50)
        keluar_time = masuk_time + timedelta(hours=1)  # durasi 1 jam
        
        riwayat_parkir.append({
            "plat": k["plat"],
            "jenis": k["jenis"],
            "merk": k["merk"],
            "masuk": masuk_time.strftime("%Y-%m-%d %H:%M:%S"),
            "keluar": keluar_time.strftime("%Y-%m-%d %H:%M:%S"),
        })

# Contoh cek
for r in riwayat_parkir[:5]:
    print(r)
