from models.sekolah import Sekolah
from structures.linked_list import LinkedListKode
from structures.hash_table import HashTableKode
from structures.stack import Stack
from structures.queue import Queue
from structures.tree import TreeNode, hitung_node_tree
from structures.graph import Graph


class SekolahService:
    def __init__(self):
        self.daftar_sekolah = LinkedListKode()
        self.hash_sekolah = HashTableKode()
        self.stack_undo = Stack()
        self.antrean_pengiriman = Queue()
        self.graph_distribusi = Graph()

    def tambah_sekolah(self, kode, nama, jarak_km, kecamatan, kode_dapur):
        if self.hash_sekolah.get(kode) is not None:
            raise ValueError("Kode sekolah sudah terdaftar.")
        sekolah = Sekolah(kode, nama, jarak_km, kecamatan, kode_dapur)
        self.daftar_sekolah.tambah_di_akhir(sekolah)
        self.hash_sekolah.insert(sekolah)
        self.stack_undo.push(("CREATE", sekolah))
        return sekolah

    def hapus_sekolah(self, kode):
        data = self.daftar_sekolah.hapus_by_kode(kode)
        if data is None:
            raise ValueError("Sekolah tidak ditemukan.")
        self.hash_sekolah.delete(kode)
        self.stack_undo.push(("DELETE", data))
        return data

    def update_status(self, kode, status_baru):
        node = self.daftar_sekolah.cari_by_kode(kode)
        if node is None:
            raise ValueError("Sekolah tidak ditemukan.")
        lama = Sekolah(
            node.data.kode,
            node.data.nama,
            node.data.jarak_km,
            node.data.kecamatan,
            node.data.kode_dapur,
            node.data.status
        )
        node.data.status = status_baru
        self.hash_sekolah.insert(node.data)
        self.stack_undo.push(("UPDATE_STATUS", lama))
        return node.data

    def get_semua_sekolah(self):
        return self.daftar_sekolah.to_list()

    def get_urut_jarak(self, ascending=True):
        data = self.daftar_sekolah.to_list()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if ascending:
                    kondisi = data[j].jarak_km > data[j + 1].jarak_km
                else:
                    kondisi = data[j].jarak_km < data[j + 1].jarak_km
                if kondisi:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

    def undo(self):
        if self.stack_undo.is_empty():
            return "Tidak ada aksi yang bisa di-undo."
        aksi, data = self.stack_undo.pop()
        if aksi == "CREATE":
            self.daftar_sekolah.hapus_by_kode(data.kode)
            self.hash_sekolah.delete(data.kode)
            return "Undo: penambahan sekolah dibatalkan."
        if aksi == "DELETE":
            self.daftar_sekolah.tambah_di_akhir(data)
            self.hash_sekolah.insert(data)
            return "Undo: penghapusan sekolah dibatalkan."
        if aksi == "UPDATE_STATUS":
            node = self.daftar_sekolah.cari_by_kode(data.kode)
            if node:
                node.data.status = data.status
                self.hash_sekolah.insert(node.data)
            return "Undo: status pengiriman dikembalikan."
        return "Undo gagal."

    def tambah_antrean(self, kode):
        if self.hash_sekolah.get(kode) is None:
            raise ValueError("Sekolah tidak ditemukan.")
        self.antrean_pengiriman.enqueue(kode)

    def proses_antrean(self):
        kode = self.antrean_pengiriman.dequeue()
        if kode is None:
            return None, "Antrean pengiriman kosong."
        sekolah = self.hash_sekolah.get(kode)
        if sekolah is None:
            return None, f"Sekolah {kode} tidak ditemukan."
        sekolah.status = "Sedang dikirim"
        self.hash_sekolah.insert(sekolah)
        return sekolah, f"Pengiriman sedang diproses untuk {sekolah.nama}."

    def get_antrean_str(self):
        return str(self.antrean_pengiriman)

    def build_tree_lokasi(self, dapur_list):
        root = TreeNode("Provinsi Lampung")
        daerah_map = {}

        for dapur in dapur_list:
            key = dapur.daerah.lower().strip()
            if key not in daerah_map:
                node_daerah = TreeNode(dapur.daerah.title())
                daerah_map[key] = node_daerah
                root.tambah_child(node_daerah)

            node_dapur = TreeNode(f"Dapur {dapur.kode} - {dapur.nama}")
            daerah_map[key].tambah_child(node_dapur)

            for s in self.get_semua_sekolah():
                if s.kode_dapur == dapur.kode:
                    node_dapur.tambah_child(TreeNode(f"{s.kode} - {s.nama}"))

        return root, hitung_node_tree(root)

    def build_graph_distribusi(self, dapur_list):
        g = Graph()
        gudang = "Gudang Pusat"

        for dapur in dapur_list:
            g.tambah_edge(gudang, dapur.kode)
            for s in self.get_semua_sekolah():
                if s.kode_dapur == dapur.kode:
                    g.tambah_edge(dapur.kode, s.kode)

        self.graph_distribusi = g
        return g
