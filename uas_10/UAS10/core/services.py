from .constants import dataMahasiswa

def proses_nilai(daftar_nilai, threshold=75):
    if len(daftar_nilai) != 5:
        raise ValueError("Nilai harus berjumlah 5")

    total = sum(daftar_nilai)
    rata_rata = total / len(daftar_nilai)

    status = "LULUS" if rata_rata >= threshold else "TIDAK LULUS"

    return {
        "nim": dataMahasiswa[0]["nim"],
        "nilai": daftar_nilai,
        "rata_rata": rata_rata,
        "threshold": threshold,
        "status": status
    }
