import tkinter as tk
from services.sekolah_service import SekolahService
from services.dapur_service import DapurService
from ui.sekolah_ui import SekolahUI
from ui.dapur_ui import DapurUI
from tkinter import simpledialog


class MBGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Program Makan Bergizi Gratis")
        self.root.minsize(1150, 620)
        self.root.configure(bg="#edf1f7")

        self.sekolah_service = SekolahService()
        self.dapur_service = DapurService()

        self.sekolah_ui = SekolahUI(
            self.root,
            self.sekolah_service,
            self.dapur_service,
            self.set_output
        )

        self.dapur_ui = DapurUI(
            self.root,
            self.dapur_service,
            self.set_output
        )

        self._build_layout()

        self.set_output(
            "Selamat datang di Dashboard MBG.\n"
            "Gunakan menu di kiri untuk mengelola sekolah, dapur, antrean, dan visualisasi distribusi."
        )

    def _build_layout(self):
        header = tk.Frame(self.root, bg="#3366ff", pady=10, padx=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Dashboard MBG - Sekolah & Dapur",
            bg="#3366ff",
            fg="white",
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Manajemen sekolah, dapur, pengiriman, dan visualisasi distribusi",
            bg="#3366ff",
            fg="#e3f2ff",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        main = tk.Frame(self.root, bg="#edf1f7")
        main.pack(fill="both", expand=True)

        sidebar_container = tk.Frame(main, bg="#ffffff", width=260)
        sidebar_container.pack(side="left", fill="y")
        sidebar_container.pack_propagate(False)

        sidebar_canvas = tk.Canvas(
            sidebar_container,
            bg="#ffffff",
            width=260,
            highlightthickness=0
        )
        sidebar_canvas.pack(side="left", fill="y", expand=True)

        scrollbar = tk.Scrollbar(
            sidebar_container,
            orient="vertical",
            command=sidebar_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        sidebar_canvas.configure(yscrollcommand=scrollbar.set)

        sidebar = tk.Frame(sidebar_canvas, bg="#ffffff")
        sidebar_canvas.create_window((0, 0), window=sidebar, anchor="nw")

        sidebar.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(
                scrollregion=sidebar_canvas.bbox("all")
            )
        )

        sidebar_canvas.bind_all(
            "<MouseWheel>",
            lambda e: sidebar_canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            )
        )

        content = tk.Frame(main, bg="#edf1f7")
        content.pack(side="right", fill="both", expand=True, padx=12, pady=12)

        self._build_sidebar(sidebar)

        self.output_text = tk.Text(
            content,
            wrap="word",
            bg="#ffffff",
            fg="#222b45",
            font=("Consolas", 10),
            relief="flat",
            padx=10,
            pady=8
        )
        self.output_text.pack(fill="both", expand=True)

    def _build_sidebar(self, sidebar):
        btn_style = {
            "width": 26,
            "anchor": "w",
            "bg": "#ffffff",
            "activebackground": "#e4e9f2",
            "fg": "#2e3a59",
            "activeforeground": "#3366ff",
            "relief": "flat",
            "font": ("Segoe UI", 9),
            "bd": 0,
            "padx": 18,
            "pady": 5,
        }

        def add_btn(text, cmd):
            tk.Button(sidebar, text=text, command=cmd, **btn_style).pack(fill="x", pady=1)

        tk.Label(sidebar, text="MANAGE SEKOLAH", bg="#ffffff",
                 fg="#8f9bb3", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(18, 6))

        add_btn("Tambah Sekolah", self._safe(self.sekolah_ui.tambah_sekolah_gui))
        add_btn("Hapus Sekolah", self._safe(self.sekolah_ui.hapus_sekolah_gui))
        add_btn("Update Status Pengiriman", self._safe(self.sekolah_ui.update_status_gui))
        add_btn("Daftar Sekolah", self._safe(self.sekolah_ui.tampilkan_sekolah_gui))
        add_btn("Sekolah Terdekat", self._safe(self.sekolah_ui.tampilkan_terdekat_gui))
        add_btn("Sekolah Terjauh", self._safe(self.sekolah_ui.tampilkan_terjauh_gui))

        tk.Label(sidebar, bg="#ffffff").pack(pady=4)

        tk.Label(sidebar, text="MANAGE DAPUR", bg="#ffffff",
                 fg="#8f9bb3", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(6, 6))

        add_btn("Tambah Dapur", self._safe(self.dapur_ui.tambah_dapur_gui))
        add_btn("Hapus Dapur", self._safe(self.dapur_ui.hapus_dapur_gui))
        add_btn("Update Menu Dapur", self._safe(self.dapur_ui.update_menu_gui))
        add_btn("Daftar Dapur", self._safe(self.dapur_ui.tampilkan_dapur_gui))
        add_btn("Daftar Menu Dapur", self._safe(self.dapur_ui.daftar_menu_gui))

        tk.Label(sidebar, bg="#ffffff").pack(pady=4)

        tk.Label(sidebar, text="VISUALISASI", bg="#ffffff",
                 fg="#8f9bb3", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(6, 6))

        add_btn("Tree Lokasi", self._safe(self.tampilkan_tree_gui))
        add_btn("Graph + BFS", self._safe(self.tampilkan_graph_gui))

    def _safe(self, func):
        def wrapper():
            try:
                func()
            except Exception as e:
                self.set_output(str(e))
        return wrapper

    def set_output(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def tampilkan_tree_gui(self):
        dapurs = self.dapur_service.get_semua_dapur()
        root, total = self.sekolah_service.build_tree_lokasi(dapurs)
        self.set_output(f"Total node: {total}\n" + "\n".join(root.to_lines()))

    def tampilkan_graph_gui(self):
        dapurs = self.dapur_service.get_semua_dapur()
        g = self.sekolah_service.build_graph_distribusi(dapurs)
        start = simpledialog.askstring(
            "Graph BFS",
            "Masukkan node awal (Gudang Pusat / kode dapur / kode sekolah):"
        )
        if not start:
            return
        self.set_output(
            "Graph Distribusi:\n" +
            g.tampilkan_str() +
            "\n\n" +
            g.bfs_str(start)
        )
