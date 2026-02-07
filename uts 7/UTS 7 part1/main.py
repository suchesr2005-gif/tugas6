import os
from antrian import Antrian

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def tekan_enter():
    input("\nTekan ENTER untuk kembali...")
    bersihkan_layar()

def menu():
    print("=== SISTEM ANTRIAN ===")
    print("1. Tambah Antrian")
    print("2. Panggil Antrian")
    print("3. Lihat Antrian")
    print("4. Keluar")

antrian = Antrian()
bersihkan_layar()

while True:
    menu()
    pilihan = input("Pilihan : ")

    if pilihan == "1":
        nama = input("Nama: ")
        antrian.tambah(nama)
        tekan_enter()

    elif pilihan == "2":
        antrian.panggil()
        tekan_enter()

    elif pilihan == "3":
        antrian.lihat()
        tekan_enter()

    elif pilihan == "4":
        print("Program selesai.")
        break

    else:
        print("Pilihan tidak valid")
        tekan_enter()
