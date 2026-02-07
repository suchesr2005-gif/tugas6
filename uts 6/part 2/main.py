import os
from utils import nilai_ke_label, label_ke_bobot
biodata = {}
list_sks = []
list_nilai = []
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk lanjut...")
def tampilkan_menu():
    print("===== MENU =====")
    print("1. Biodata")
    print("2. SKS")
    print("3. Input Nilai")
    print("4. Lihat Nilai")
    print("5. Lihat IP")
    print("6. Keluar")
def menu_biodata():
    while True:
        clear()
        print("=== BIODATA ===")
        print("1. Input Biodata")
        print("2. Lihat Biodata")
        print("3. Kembali")

        s = input("Pilihan: ")

        if s == "1":
            biodata["nama"] = input("Nama  : ")
            biodata["nim"] = input("NIM   : ")
            biodata["prodi"] = input("Prodi : ")
            print("\nBiodata tersimpan")
            pause()

        elif s == "2":
            if not biodata:
                print("\nBiodata belum diinput")
            else:
                print("\nNama  :", biodata["nama"])
                print("NIM   :", biodata["nim"])
                print("Prodi :", biodata["prodi"])
            pause()

        elif s == "3":
            break
        else:
            print("Pilihan tidak valid")
            pause()
def menu_sks():
    list_sks.clear()
    jumlah = int(input("Jumlah Mata Kuliah: "))

    for i in range(jumlah):
        list_sks.append(int(input(f"SKS {i+1}: ")))

    print("\nData SKS tersimpan")
    pause()
def menu_input_nilai():
    list_nilai.clear()
    jumlah = int(input("Jumlah Mata Kuliah: "))

    for i in range(jumlah):
        list_nilai.append(float(input(f"Nilai {i+1}: ")))

    print("\nData nilai tersimpan")
    pause()
def menu_lihat_nilai():
    if not list_sks:
        print("\nSKS belum diinput")
        pause()
        return

    if not list_nilai:
        print("\nNilai belum diinput")
        pause()
        return

    if len(list_sks) != len(list_nilai):
        print("\nJumlah SKS dan nilai tidak sama")
        pause()
        return

    print("\nSKS | Nilai | Label | Bobot")
    print("----------------------------")

    for i in range(len(list_nilai)):
        label = nilai_ke_label(list_nilai[i])
        bobot = label_ke_bobot(label)
        print(f"{list_sks[i]:<3} | {list_nilai[i]:<5} | {label:<5} | {bobot}")

    pause()
def menu_lihat_ip():
    if not list_sks or not list_nilai:
        print("\nData belum lengkap")
        pause()
        return

    if len(list_sks) != len(list_nilai):
        print("\nJumlah SKS dan nilai tidak sama")
        pause()
        return

    total_sks = sum(list_sks)
    total_nilai = 0

    for i in range(len(list_nilai)):
        label = nilai_ke_label(list_nilai[i])
        total_nilai += label_ke_bobot(label) * list_sks[i]

    ips = total_nilai / total_sks
    print("\nIPS :", round(ips, 2))
    pause()
def run_program():
    clear()
    while True:
        tampilkan_menu()
        pilihan = input("Pilihan: ")

        if pilihan == "1":
            menu_biodata()
        elif pilihan == "2":
            menu_sks()
        elif pilihan == "3":
            menu_input_nilai()
        elif pilihan == "4":
            menu_lihat_nilai()
        elif pilihan == "5":
            menu_lihat_ip()
        elif pilihan == "6":
            print("\nProgram selesai")
            break
        else:
            print("\nPilihan tidak valid")
            pause()

        clear()