import json
import os
from datetime import datetime

DB_FILE = 'rpl_canteen_elite_db.json'

def load_data():
    default_data = {
        "stok": {
            "Nasi Goreng": 10, "Mie Ayam": 15, "Gorengan": 50,
            "Pop Ice": 100, "Nutrisari": 100, "Teh Sisri": 100,
            "Buku Tulis": 25, "Pulpen": 50, "Pensil": 30
        },
        "harga": {
            "Nasi Goreng": 10000, "Mie Ayam": 12000, "Gorengan": 2000,
            "Pop Ice": 5000, "Nutrisari": 3000, "Teh Sisri": 2000,
            "Buku Tulis": 5000, "Pulpen": 3000, "Pensil": 2000
        },
        "saldo_kas": 500000,
        "history": []
    }
    
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                # Sinkronisasi Otomatis (Anti KeyError)
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                return data
        except:
            return default_data
    return default_data

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def tampilkan_katalog(data):
    print("\n" + "="*45)
    print(f"{'📦 DAFTAR MENU & STOK':^45}")
    print("="*45)
    print(f"{'Nama Barang':<18} | {'Harga':<10} | {'Stok':<5}")
    print("-" * 45)
    stok = data.get("stok", {})
    harga = data.get("harga", {})
    for k, v in stok.items():
        print(f" {k:<18} | Rp{harga.get(k, 0):<8,} | {v:<5}")
    print("-" * 45)

def main():
    data = load_data()
    
    while True:
        clear_screen()
        waktu = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("=============================================")
        print("    🌟 RPL CANTEEN ULTIMATE V17 (FINAL) 🌟   ")
        print(f"      {waktu}")
        print("=============================================")
        saldo = data.get('saldo_kas', 0)
        print(f" 💰 SALDO KAS KANTIN : Rp{saldo:,}")
        print("---------------------------------------------")
        print(" [1] 🛒 BUAT PESANAN (Nama & Kelas)")
        print(" [2] 📦 RESTOCK BARANG (Kulakan)")
        print(" [3] 📊 LIHAT DAFTAR STOK")
        print(" [4] 📜 LAPORAN TRANSAKSI")
        print(" [5] 🚪 KELUAR & SIMPAN DATA")
        print("---------------------------------------------")
        
        pilihan = input(" Pilih Menu (1-5): ")

        if pilihan == '1':
            clear_screen()
            print("--- 👤 IDENTITAS PEMBELI ---")
            nama = input(" Nama Lengkap : ")
            kelas = input(" Kelas        : ")
            
            clear_screen()
            print(f" Halo, {nama}! Pilih pesananmu di bawah ini:")
            tampilkan_katalog(data)
            
            item = input(" Ketik Nama Barang: ")
            
            if item in data['stok']:
                rasa = ""
                # Fitur Rasa-Rasa Otomatis
                if item.lower() in ["pop ice", "nutrisari", "teh sisri"]:
                    print(f"\n Menyiapkan {item}...")
                    rasa = f" ({input(' Mau Rasa Apa? : ')})"

                try:
                    qty = int(input(f" Mau Beli Berapa? : "))
                    if qty <= data['stok'][item]:
                        total = qty * data['harga'][item]
                        
                        clear_screen()
                        print("--- 💸 METODE PEMBAYARAN ---")
                        print(f" Total Tagihan: Rp{total:,}")
                        print(" 1. Tunai | 2. QRIS | 3. Transfer")
                        met_pil = input(" Pilih (1-3): ")
                        metode = "Tunai" if met_pil == '1' else "QRIS" if met_pil == '2' else "Transfer"
                        
                        # Update Data
                        data['stok'][item] -= qty
                        data['saldo_kas'] += total
                        
                        item_final = f"{item}{rasa}"
                        log = f"[{waktu}] JUAL: {item_final} x{qty} | Rp{total:,} | {metode} | {nama} ({kelas})"
                        data['history'].append(log)
                        
                        print(f"\n✅ BERHASIL! Pesanan {item_final} sedang diproses.")
                    else:
                        print("\n❌ GAGAL: Stok tidak cukup!")
                except ValueError:
                    print("\n❌ GAGAL: Input harus angka!")
            else:
                print("\n❌ GAGAL: Barang tidak ada di menu!")
            input("\nTekan Enter...")

        elif pilihan == '2':
            clear_screen()
            print("--- 📦 RESTOCK BARANG (MODAL KAS) ---")
            item = input(" Nama Barang : ")
            try:
                qty = int(input(" Jumlah Beli : "))
                modal = int(input(" Total Harga : Rp"))
                
                if data['saldo_kas'] >= modal:
                    data['saldo_kas'] -= modal
                    data['stok'][item] = data['stok'].get(item, 0) + qty
                    if item not in data['harga']:
                        data['harga'][item] = int(input(" Set Harga Jual Satuan: Rp"))
                    
                    log = f"[{waktu}] RESTOCK: {item} x{qty} | -Rp{modal:,}"
                    data['history'].append(log)
                    print("\n✅ RESTOCK BERHASIL! Stok bertambah, saldo berkurang.")
                else:
                    print("\n❌ SALDO KAS TIDAK CUKUP!")
            except:
                print("\n❌ GAGAL: Input salah!")
            input("\nTekan Enter...")

        elif pilihan == '3':
            clear_screen()
            tampilkan_katalog(data)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '4':
            clear_screen()
            print("--- 📜 RIWAYAT TRANSAKSI TERAKHIR ---")
            if not data['history']: print(" Belum ada transaksi.")
            for h in data['history'][-15:]: # Lihat 15 transaksi terakhir
                print(h)
            input("\nTekan Enter...")

        elif pilihan == '5':
            save_data(data)
            print("\n✅ DATA TERSIMPAN AMAN. Bye, Samuel!")
            break

if __name__ == "__main__":
    main()
