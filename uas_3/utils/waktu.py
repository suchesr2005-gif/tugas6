from datetime import datetime
import math
from constants import TARIF


def hitung_durasi_menit(waktu_masuk, waktu_keluar):
    masuk = datetime.strptime(waktu_masuk, "%Y-%m-%d %H:%M:%S")
    keluar = datetime.strptime(waktu_keluar, "%Y-%m-%d %H:%M:%S")

    # Selisih waktu → menit (dibulatkan ke atas)
    durasi_menit = math.ceil(
        (keluar - masuk).total_seconds() / 60
    )

    return max(durasi_menit, 1)


def hitung_biaya(jenis_kendaraan, durasi_menit):
    tarif_per_menit = TARIF.get(jenis_kendaraan, TARIF["lain"])

    # biaya = menit × tarif
    return durasi_menit * tarif_per_menit
