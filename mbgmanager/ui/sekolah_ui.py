import tkinter as tk
from tkinter import simpledialog, messagebox


class SekolahUI:
    def __init__(self, root, sekolah_service, dapur_service, output_callback):
        self.root = root
        self.sekolah_service = sekolah_service
        self.dapur_service = dapur_service
        self.output = output_callback

    def tambah_sekolah_gui(self):
        dapurs = self.dapur_service.get_semua_dapur()
        if not dapurs:
            messagebox.showerror("Error", "Tambah dapur terlebih dahulu.")
            return

        win = tk.Toplevel(self.root)
        win.title("Tambah Sekolah")
        win.configure(bg="#ffffff")

        tk.Label(win, text="Kode Sekolah").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        kode = tk.Entry(win, width=30)
        kode.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(win, text="Nama Sekolah").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        nama = tk.Entry(win, width=30)
        nama.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(win, text="Kecamatan").grid(row=2, column=0, sticky="w", padx=8, pady=4)
        kec = tk.Entry(win, width=30)
        kec.grid(row=2, column=1, padx=8, pady=4)

        tk.Label(win, text="Jarak (km)").grid(row=3, column=0, sticky="w", padx=8, pady=4)
        jarak = tk.Entry(win, width=30)
        jarak.grid(row=3, column=1, padx=8, pady=4)

        tk.Label(win, text="Dapur").grid(row=4, column=0, sticky="w", padx=8, pady=4)
        dapur_var = tk.StringVar(win)
        dapur_codes = [d.kode for d in dapurs]
        dapur_var.set(dapur_codes[0])
        tk.OptionMenu(win, dapur_var, *dapur_codes).grid(row=4, column=1, sticky="w", padx=8, pady=4)

        def simpan():
            try:
                s = self.sekolah_service.tambah_sekolah(
                    kode.get().strip(),
                    nama.get().strip(),
                    float(jarak.get().strip()),
                    kec.get().strip(),
                    dapur_var.get()
                )
                self.output(f"Sekolah ditambahkan: {s}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Simpan", command=simpan).grid(row=5, column=0, columnspan=2, pady=8)

    def hapus_sekolah_gui(self):
        kode = simpledialog.askstring("Hapus Sekolah", "Kode sekolah:")
        if not kode:
            return
        try:
            s = self.sekolah_service.hapus_sekolah(kode)
            self.output(f"Sekolah dihapus: {s}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_status_gui(self):
        kode = simpledialog.askstring("Update Status", "Kode sekolah:")
        if not kode:
            return

        win = tk.Toplevel(self.root)
        win.title("Update Status Pengiriman")
        win.configure(bg="#ffffff")

        tk.Label(win, text="Status Baru").grid(row=0, column=0, sticky="w", padx=8, pady=6)

        status_var = tk.StringVar(value="Belum dikirim")
        opsi_status = ["Belum dikirim", "Sedang dikirim", "Terkirim"]

        tk.OptionMenu(win, status_var, *opsi_status).grid(
            row=0, column=1, sticky="w", padx=8, pady=6
        )

        def simpan():
            try:
                s = self.sekolah_service.update_status(kode, status_var.get())
                self.output(f"Status diperbarui: {s}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Simpan", command=simpan).grid(
            row=1, column=0, columnspan=2, pady=8
        )


    def tampilkan_sekolah_gui(self):
        data = self.sekolah_service.get_semua_sekolah()
        if not data:
            self.output("Belum ada sekolah.")
            return
        self.output("\n".join(str(s) for s in data))

    def tampilkan_terdekat_gui(self):
        data = self.sekolah_service.get_urut_jarak(True)
        self.output("\n".join(str(s) for s in data))

    def tampilkan_terjauh_gui(self):
        data = self.sekolah_service.get_urut_jarak(False)
        self.output("\n".join(str(s) for s in data))

    def undo_gui(self):
        self.output(self.sekolah_service.undo())

    def tambah_antrean_gui(self):
        kode = simpledialog.askstring("Antrean", "Kode sekolah:")
        if not kode:
            return
        try:
            self.sekolah_service.tambah_antrean(kode)
            self.output(f"{kode} masuk antrean.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def proses_antrean_gui(self):
        s, msg = self.sekolah_service.proses_antrean()
        self.output(msg)

    def lihat_antrean_gui(self):
        self.output(self.sekolah_service.get_antrean_str())
