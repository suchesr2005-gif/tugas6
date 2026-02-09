from datetime import datetime
from collections import defaultdict
from constants import parkir_aktif, riwayat_parkir, TARIF
from utils.waktu import hitung_durasi_menit, hitung_biaya


# ================= RIWAYAT =================
def init_riwayat():
    for record in riwayat_parkir:
        if record.get("menit") is None or record.get("biaya") is None:
            durasi_menit = hitung_durasi_menit(record["masuk"], record["keluar"])
            biaya = hitung_biaya(record["jenis"], durasi_menit)

            record["menit"] = durasi_menit
            record["biaya"] = biaya


# ================= LAPORAN =================
def buat_struktur_kosong():
    return {
        "mobil": {"jml": 0, "biaya": 0},
        "motor": {"jml": 0, "biaya": 0},
        "total_jml": 0,
        "total_biaya": 0
    }


def proses_analisis(format_waktu):
    init_riwayat()
    hasil_analisis = defaultdict(buat_struktur_kosong)

    for record in riwayat_parkir:
        waktu_keluar = datetime.strptime(
            record["keluar"], "%Y-%m-%d %H:%M:%S"
        )
        key = waktu_keluar.strftime(format_waktu)
        jenis_kendaraan = record["jenis"].lower()
        biaya = record["biaya"]

        if jenis_kendaraan == "mobil":
            hasil_analisis[key]["mobil"]["jml"] += 1
            hasil_analisis[key]["mobil"]["biaya"] += biaya

        elif jenis_kendaraan == "motor":
            hasil_analisis[key]["motor"]["jml"] += 1
            hasil_analisis[key]["motor"]["biaya"] += biaya

        hasil_analisis[key]["total_jml"] += 1
        hasil_analisis[key]["total_biaya"] += biaya

    return hasil_analisis


def laporan_harian():
    return proses_analisis("%d-%m-%Y")


def laporan_mingguan():
    return proses_analisis("Minggu %U %Y")


def laporan_bulanan():
    return proses_analisis("%B %Y")


def laporan_tahunan():
    return proses_analisis("%Y")


def total_laporan():
    init_riwayat()
    jumlah_mobil = sum(
        1 for record in riwayat_parkir if record["jenis"] == "mobil"
    )
    jumlah_motor = sum(
        1 for record in riwayat_parkir if record["jenis"] == "motor"
    )
    total_biaya = sum(record["biaya"] for record in riwayat_parkir)

    return len(riwayat_parkir), total_biaya, jumlah_mobil, jumlah_motor


# ================= PARKIR AKTIF =================
def kendaraan_masuk(plat, jenis, merk):
    if any(kendaraan["plat"] == plat for kendaraan in parkir_aktif):
        return False

    parkir_aktif.append({
        "plat": plat,
        "jenis": jenis.lower(),
        "merk": merk,
        "masuk": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True


def kendaraan_keluar(plat):
    for index, kendaraan in enumerate(parkir_aktif):
        if kendaraan["plat"] == plat:
            waktu_keluar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            durasi_menit = hitung_durasi_menit(
                kendaraan["masuk"], waktu_keluar
            )
            biaya = hitung_biaya(kendaraan["jenis"], durasi_menit)

            data_keluar = {
                "plat": kendaraan["plat"],
                "jenis": kendaraan["jenis"],
                "merk": kendaraan["merk"],
                "masuk": kendaraan["masuk"],
                "keluar": waktu_keluar,
                "menit": durasi_menit,
                "biaya": biaya
            }

            parkir_aktif.pop(index)
            riwayat_parkir.append(data_keluar)
            return data_keluar

    return None


def daftar_parkir():
    return parkir_aktif


def reset_data():
    parkir_aktif.clear()
    riwayat_parkir.clear()
