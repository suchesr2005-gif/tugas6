class Parkir:
    def __init__(self):
        self.data = []

    def plat_ada(self, plat):
        for k in self.data:
            if k["plat"] == plat:
                return True
        return False

    def masuk(self, plat, jenis, merk):
        if self.plat_ada(plat):
            return False   # gagal karena duplikat

        self.data.append({
            "plat": plat,
            "jenis": jenis,
            "merk": merk
        })
        return True

    def keluar(self, plat):
        for k in self.data:
            if k["plat"] == plat:
                self.data.remove(k)
                return k   # kembalikan data kendaraan
        return None

    def semua(self):
        return self.data
