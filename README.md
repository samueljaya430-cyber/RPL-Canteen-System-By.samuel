# 🏪 RPL Canteen Wow

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![Status](https://img.shields.io/badge/Status-Stable-green.svg)

Aplikasi kasir kantin berbasis Terminal (TUI) yang dikembangkan untuk mempermudah manajemen stok dan transaksi di kantin sekolah. Versi V17 ini adalah versi paling stabil dengan fitur perlindungan data otomatis.

---

## 📸 Screenshot Aplikasi

<details>
  <summary>Klik untuk melihat galeri foto aplikasi 📸</summary>
  
  ### 1. Menu Utama & Saldo Kas
  ![Menu Utama](Screenshot_2026-05-17-19-02-59-089_ru.iiec.pydroid3.jpg)
  
  ### 2. Form Identitas (Nama & Kelas)
  ![Form Identitas](Screenshot_2026-05-17-19-03-17-887_ru.iiec.pydroid3.jpg)
  
  ### 3. Pilihan Menu
  ![Pilihan Rasa](Screenshot_2026-05-17-19-03-48-811_ru.iiec.pydroid3.jpg)
  
  ### 4. Metode Pembayaran & Struk
  ![Transaksi](Screenshot_2026-05-17-19-04-43-435_ru.iiec.pydroid3.jpg)
  
</details>

---

## 🚀 Fitur Unggulan

- **🔐 Secured Entry**: Sistem wajib input Nama & Kelas sebelum transaksi untuk validasi data pembeli.
- **🥤 Smart Drink System**: Deteksi otomatis untuk menu minuman rasa-rasa (Pop Ice, Nutrisari, Teh Sisri).
- **💸 Triple Payment**: Mendukung pembayaran melalui **Tunai**, **QRIS**, dan **Transfer Bank**.
- **📈 Auto-Restock & Budgeting**: Mengurangi saldo kas kantin secara otomatis saat membeli stok baru (kulakan).
- **🛡️ Anti-Crash Database**: Menggunakan sistem sinkronisasi JSON yang mencegah error `KeyError`.
- **📜 Transaction Logging**: Riwayat 15 transaksi terakhir disimpan secara permanen di database.

---

## 🛠️ Cara Penggunaan

1. **Jalankan Aplikasi**: Buka file `rpl_canteen_elite_wow.py` di Pydroid 3 atau PC.
2. **Menu Penjualan**: Pilih [1], masukkan nama dan kelas, lalu pilih barang yang ingin dibeli.
3. **Menu Restock**: Pilih [2] jika ingin menambah stok barang menggunakan uang kas kantin.
4. **Cek Laporan**: Pilih [4] untuk melihat siapa saja yang sudah belanja hari ini.
5. **Simpan**: Selalu pilih menu [5] untuk keluar agar data tersimpan dengan aman ke file JSON.

---

## 🏗️ Struktur Proyek

- `rpl_canteen_elite_wow.py`: File utama aplikasi Python.
- `rpl_canteen_elite_db.json`: File database (dibuat otomatis oleh sistem).
- `README.md`: Dokumentasi proyek ini.

---
**Developed by Samuel (RPL Team) 🚀**
