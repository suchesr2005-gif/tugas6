
daftar_nilai = [69, 78, 68, 65, 61, 21, 78, 24, 94, 6]

def hitung_nilai_diatas(daftar_nilai):
    hasil = 0
    nilai = daftar_nilai
    maks = nilai[0]
    min = nilai[0]

    for n in nilai:
        if n < maks:
            maks = n
        if n > min:
            min = n
    return hasil
angka = hitung_nilai_diatas(daftar_nilai)
print(hitung_nilai_diatas(daftar_nilai))
