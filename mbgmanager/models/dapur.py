class Dapur:
    def __init__(self, kode, nama, daerah):
        self.kode = kode
        self.nama = nama
        self.daerah = daerah
        self.menu_harian = {}

    def __str__(self):
        return f"[{self.kode}] {self.nama} - {self.daerah}"
