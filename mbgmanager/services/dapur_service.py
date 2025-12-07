from models.dapur import Dapur
from structures.linked_list import LinkedListKode
from structures.hash_table import HashTableKode


class DapurService:
    def __init__(self):
        self.daftar_dapur = LinkedListKode()
        self.hash_dapur = HashTableKode()

    def tambah_dapur(self, kode, nama, daerah):
        if self.hash_dapur.get(kode) is not None:
            raise ValueError("Kode dapur sudah terdaftar.")
        dapur = Dapur(kode, nama, daerah)
        self.daftar_dapur.tambah_di_akhir(dapur)
        self.hash_dapur.insert(dapur)
        return dapur

    def hapus_dapur(self, kode):
        dapur = self.daftar_dapur.hapus_by_kode(kode)
        if dapur is None:
            raise ValueError("Dapur tidak ditemukan.")
        self.hash_dapur.delete(kode)
        return dapur

    def get_dapur(self, kode):
        return self.hash_dapur.get(kode)

    def get_semua_dapur(self):
        return self.daftar_dapur.to_list()

    def update_menu_harian(self, kode_dapur, hari, menu_list):
        dapur = self.hash_dapur.get(kode_dapur)
        if dapur is None:
            raise ValueError("Dapur tidak ditemukan.")
        dapur.menu_harian[hari] = menu_list
        self.hash_dapur.insert(dapur)
        return dapur

    def get_menu_harian(self, kode_dapur, hari):
        dapur = self.hash_dapur.get(kode_dapur)
        if dapur is None:
            raise ValueError("Dapur tidak ditemukan.")
        return dapur.menu_harian.get(hari, [])
