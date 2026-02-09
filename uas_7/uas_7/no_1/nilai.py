daftar_nilai = [69, 78, 68, 65, 61, 21, 78, 24, 94, 6]

def hitung_nilai_diatas(threshold=0, daftar_nilai=None):
    if daftar_nilai is None:
        return 0

    hasil = 0
    for nilai in daftar_nilai:
        if nilai > threshold:
            hasil += 1
    return hasil

angka = hitung_nilai_diatas(threshold=50, daftar_nilai=daftar_nilai)
print(angka)
