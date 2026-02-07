from utils import get_label, get_bobot, hitung_total_sks, hitung_total_nilai, hitung_ips
from cli import tampilkan_menu, bersihkan_layar, kembali_ke_menu

def main():
    data_kuliah = [] 

    while True:
        bersihkan_layar()
        tampilkan_menu()
        pilihan = input("\nPilihan: ")

        if pilihan == '1':
            n = float(input("Nilai Mahasiswa: "))
            print(f"Label: {get_label(n)}")
            kembali_ke_menu()

        elif pilihan == '2':
            l = input("Label Nilai Mahasiswa: ")
            print(f"Bobot: {get_bobot(l)}")
            kembali_ke_menu()

        elif pilihan == '3':
            total_sks = hitung_total_sks()
            kembali_ke_menu()

        elif pilihan == "4":
            jumlah = int(input("\nJumlah Data: "))
            sks_list = []
            nilai_list = []

            print("\n--------- input sks ----------")
            for i in range(jumlah):
                sks_list.append(int(input(f"SKS {i+1}: ")))

            print("\n--------- input Nilai Mahasiswa ----------")
            for i in range(jumlah):
                nilai_list.append(float(input(f"Nilai {i+1}: ")))

                total_nilai = hitung_total_nilai(sks_list, nilai_list)
            print("\nTotal Nilai:", total_nilai)
            kembali_ke_menu()

        elif pilihan == '5':
            jumlah = int(input("\nJumlah Data: "))
            sks_list = []
            nilai_list = []

            print("--------- input sks ---------")
            for i in range(1, jumlah + 1):
                sks_list.append(int(input(f"SKS {i}: ")))

            print("\n--------- input Nilai Mahasiswa ---------")
            for i in range(1, jumlah + 1):
                nilai_list.append(int(input(f"Nilai {i}: ")))

                total_nilai = hitung_total_nilai(sks_list, nilai_list)
                total_sks = sum(sks_list)

                ips = hitung_ips(total_nilai, total_sks)

            print("\nIPS:", round(ips, 2))
            kembali_ke_menu()
            
        elif pilihan == '6':
            print("Program Selesai.")
            break
        else:
            print("Pilihan tidak ada!")
            kembali_ke_menu()

if __name__ == "__main__":
    main()