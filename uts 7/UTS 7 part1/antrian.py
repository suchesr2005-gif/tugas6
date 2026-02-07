class Antrian:
    def __init__(self):
        self.data = []

    def tambah(self, nama):
        if nama in self.data:
            print("Nama sudah ada dalam antrian")
            return

        self.data.append(nama)
        print("Antrian berhasil ditambahkan")


    def panggil(self):
        if not self.data:
            print("Tidak ada antrian")
        else:
            nama = self.data.pop(0)
            print(f"Memanggil {nama}")

    def lihat(self):
        if not self.data:
            print("Antrian kosong")
        else:
            print("Daftar Antrian:")
            for i, nama in enumerate(self.data, start=1):
                print(f"{i}. {nama}")
