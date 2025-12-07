import tkinter as tk
from tkinter import simpledialog, messagebox


class DapurUI:
    def __init__(self, root, dapur_service, output_callback):
        self.root = root
        self.dapur_service = dapur_service
        self.output = output_callback

    def tambah_dapur_gui(self):
        win = tk.Toplevel(self.root)
        win.title("Tambah Dapur")
        win.configure(bg="#ffffff")

        tk.Label(win, text="Kode Dapur").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        kode = tk.Entry(win, width=30)
        kode.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(win, text="Nama Dapur").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        nama = tk.Entry(win, width=30)
        nama.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(win, text="Daerah").grid(row=2, column=0, sticky="w", padx=8, pady=4)
        daerah = tk.Entry(win, width=30)
        daerah.grid(row=2, column=1, padx=8, pady=4)

        def simpan():
            try:
                d = self.dapur_service.tambah_dapur(
                    kode.get().strip(),
                    nama.get().strip(),
                    daerah.get().strip()
                )
                self.output(f"Dapur ditambahkan: {d}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Simpan", command=simpan).grid(row=3, column=0, columnspan=2, pady=8)

    def hapus_dapur_gui(self):
        kode = simpledialog.askstring("Hapus Dapur", "Kode dapur:")
        if not kode:
            return
        try:
            d = self.dapur_service.hapus_dapur(kode)
            self.output(f"Dapur dihapus: {d}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_menu_gui(self):
        kode = simpledialog.askstring("Menu Dapur", "Kode dapur:")
        if not kode:
            return
        hari = simpledialog.askstring("Hari", "Nama hari:")
        if not hari:
            return
        menu = simpledialog.askstring("Menu", "Pisahkan dengan koma:")
        if not menu:
            return
        try:
            self.dapur_service.update_menu_harian(
                kode,
                hari,
                [m.strip() for m in menu.split(",") if m.strip()]
            )
            self.output(f"Menu {hari} diperbarui untuk dapur {kode}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tampilkan_dapur_gui(self):
        data = self.dapur_service.get_semua_dapur()
        if not data:
            self.output("Belum ada dapur.")
            return
        self.output("\n".join(str(d) for d in data))

    def daftar_menu_gui(self):
        kode = simpledialog.askstring("Menu Dapur", "Kode dapur:")
        if not kode:
            return
        dapur = self.dapur_service.get_dapur(kode)
        if dapur is None or not dapur.menu_harian:
            self.output("Menu belum tersedia.")
            return
        lines = [f"{kode} - {dapur.nama}"]
        for h, m in dapur.menu_harian.items():
            lines.append(f"{h}: {', '.join(m)}")
        self.output("\n".join(lines))
