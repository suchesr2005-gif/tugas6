import os

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("")

def tampilkan_menu():
    print("------------- MENU -------------")
    print("")
    print("1. Konversi Nilai ke Label")
    print("2. Konversi Label ke Bobot")
    print("3. Hitung Total SKS yang Diambil")
    print("4. Hitung Total Nilai")
    print("5. Hitung IPS")
    print("6. Exit -->")

def kembali_ke_menu():
    input("\nKlik Enter untuk kembali ke menu...")