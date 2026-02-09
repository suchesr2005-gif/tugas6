from flask import session
from service.parkir_service import *


# ================= UTIL =================
def log(teks):
    session.setdefault("log", []).append(teks)


def tampil_menu():
    log("1. Kendaraan Masuk")
    log("2. Kendaraan Keluar")
    log("3. Lihat Parkir")
    log("4. Analisis")
    log("5. Keluar")


def format_uang(nilai):
    return f"Rp {nilai:,}".replace(",", ".")


# ================= TABEL =================
def tabel(judul, data):
    log("")
    log(f"=== {judul} ===")
    log(f"{'Periode/Tanggal':<20} | {'Jumlah':<22} | {'Pendapatan':<20}")
    log("-" * 75)

    for periode, nilai in data.items():
        log(
            f"{periode:<20} | "
            f"Mobil: {nilai['mobil']['jml']} mobil{' ':<5} | "
            f"Mobil: {format_uang(nilai['mobil']['biaya'])}"
        )

        log(
            f"{'':<20} | "
            f"Motor: {nilai['motor']['jml']} motor{' ':<5} | "
            f"Motor: {format_uang(nilai['motor']['biaya'])}"
        )

        log(
            f"{'':<20} | "
            f"Total: {nilai['total_jml']} Kendaraan | "
            f"Jumlah: {format_uang(nilai['total_biaya'])}"
        )
        log("-" * 75)


# ================= PROSES =================
def proses(input_user):
    step = session.get("step", "menu")

    # ===== MENU =====
    if step == "menu":
        log(f"Pilihan : {input_user}")

        if input_user == "1":
            session["step"] = "plat"

        elif input_user == "2":
            if not daftar_parkir():
                log("Parkiran kosong")
                session["step"] = "pause"
            else:
                session["step"] = "keluar"

        elif input_user == "3":
            data_parkir = daftar_parkir()
            if not data_parkir:
                log("Parkiran kosong")
            else:
                for index, kendaraan in enumerate(data_parkir, 1):
                    log(f"{index}. {kendaraan['plat']}")
            session["step"] = "pause"

        # ===== ANALISIS =====
        elif input_user == "4":
            total_kendaraan, total_uang, jumlah_mobil, jumlah_motor = total_laporan()

            log(
                f"Total Kendaraan : {total_kendaraan} "
                f"({jumlah_mobil} mobil dan {jumlah_motor} motor)"
            )
            log(f"Total Pendapatan : {format_uang(total_uang)}")

            tabel("HARI INI", laporan_harian())
            tabel("MINGGU TERAKHIR", laporan_mingguan())
            tabel("BULAN TERAKHIR", laporan_bulanan())
            tabel("TAHUN TERAKHIR", laporan_tahunan())

            session["step"] = "pause"

        elif input_user == "5":
            reset_data()
            session.clear()
            return "reset"

    # ===== INPUT PLAT =====
    elif step == "plat":
        log(f"Plat : {input_user}")
        session["plat"] = input_user
        session["step"] = "jenis"

    # ===== INPUT JENIS =====
    elif step == "jenis":
        log(f"Jenis : {input_user}")
        session["jenis"] = input_user
        session["step"] = "merk"

    # ===== INPUT MERK =====
    elif step == "merk":
        log(f"Merk : {input_user}")

        berhasil = kendaraan_masuk(
            session["plat"],
            session["jenis"],
            input_user
        )

        if berhasil:
            log("Kendaraan berhasil masuk")
        else:
            log(
                f'Kendaraan dengan Plat "{session["plat"]}" '
                f'sudah ada di parkiran'
            )

        session["step"] = "pause"

    # ===== KENDARAAN KELUAR =====
    elif step == "keluar":
        log(f"Plat : {input_user}")
        hasil_keluar = kendaraan_keluar(input_user)

        if not hasil_keluar:
            log("Kendaraan tidak ditemukan")
        else:
            log(
                f"{hasil_keluar['plat']} "
                f"{hasil_keluar['jenis']} "
                f"{hasil_keluar['merk']}"
            )
            log(f"Masuk  : {hasil_keluar['masuk']}")
            log(f"Keluar : {hasil_keluar['keluar']}")
            log(f"Durasi : {hasil_keluar['menit']} menit")
            log(f"Biaya  : {format_uang(hasil_keluar['biaya'])}")

        session["step"] = "pause"

    # ===== PAUSE =====
    elif step == "pause":
        session["log"] = []
        tampil_menu()
        session["step"] = "menu"

    return "lanjut"
