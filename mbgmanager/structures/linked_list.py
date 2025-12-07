class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListKode:
    def __init__(self):
        self.head = None

    def tambah_di_akhir(self, data):
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = node

    def cari_by_kode(self, kode):
        cur = self.head
        while cur is not None:
            if hasattr(cur.data, "kode") and cur.data.kode == kode:
                return cur
            cur = cur.next
        return None

    def hapus_by_kode(self, kode):
        cur = self.head
        prev = None
        while cur is not None:
            if hasattr(cur.data, "kode") and cur.data.kode == kode:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return cur.data
            prev = cur
            cur = cur.next
        return None

    def to_list(self):
        result = []
        cur = self.head
        while cur is not None:
            result.append(cur.data)
            cur = cur.next
        return result
