from parkir import Parkir
from utils import clear, pause

def menu():
    print("=== SISTEM PARKIR KENDARAAN ===")
    print("1. Kendaraan Masuk")
    print("2. Kendaraan Keluar")
    print("3. Lihat Parkir")
    print("4. Keluar")

parkir = Parkir()
clear()

while True:
    menu()
    pilihan = input("Pilihan : ")

    if pilihan == "1":
        plat = input("Plat  : ")
        jenis = input("Jenis : ")
        merk = input("Merk  : ")

        if parkir.masuk(plat, jenis, merk):
            print("Kendaraan berhasil ditambahkan")
        else:
            print("Plat kendaraan sudah terdaftar")

        pause()

    elif pilihan == "2":

        if not parkir.semua():
            print("Parkir kosong")
            pause()
            continue

        plat = input("Plat kendaraan keluar: ")
        data = parkir.keluar(plat)

        if data:
            print(f"Keluar: {data['plat']}3")
        else:
            print("Kendaraan tidak ditemukan")

        pause()

    elif pilihan == "3":
        data = parkir.semua()
        if not data:
            print("Parkir kosong")
        else:
            print("\nDaftar Kendaraan Parkir:")
            for i, k in enumerate(data, start=1):
                print(f"{i}. {k['plat']} ")

        pause()

    elif pilihan == "4":
        print("Terima kasih ")
        break

    else:
        print("Pilihan tidak valid")
        pause()
