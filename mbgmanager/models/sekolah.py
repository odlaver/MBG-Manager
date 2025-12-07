class Sekolah:
    def __init__(self, kode, nama, jarak_km, kecamatan, kode_dapur, status="Belum dikirim"):
        self.kode = kode
        self.nama = nama
        self.jarak_km = jarak_km
        self.kecamatan = kecamatan
        self.kode_dapur = kode_dapur
        self.status = status

    def __str__(self):
        return (
            f"[{self.kode}] {self.nama} - {self.kecamatan} "
            f"({self.jarak_km} km, status: {self.status}, dapur: {self.kode_dapur})"
        )
