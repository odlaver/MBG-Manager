class HashTableKode:
    def __init__(self, size=101):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, kode):
        return sum(ord(c) for c in kode) % self.size

    def insert(self, obj):
        if not hasattr(obj, "kode"):
            raise ValueError("Objek harus punya atribut 'kode'")
        idx = self._hash(obj.kode)
        bucket = self.table[idx]
        for i, existing in enumerate(bucket):
            if existing.kode == obj.kode:
                bucket[i] = obj
                return
        bucket.append(obj)

    def get(self, kode):
        idx = self._hash(kode)
        for obj in self.table[idx]:
            if obj.kode == kode:
                return obj
        return None

    def delete(self, kode):
        idx = self._hash(kode)
        bucket = self.table[idx]
        for i, obj in enumerate(bucket):
            if obj.kode == kode:
                return bucket.pop(i)
        return None
