# ==========================================================
# PROYEK: RPL CANTEEN ELITE 
# DEVELOPER: Samuel Jaya S. Sianipar
# FITUR: 
# - Database Persistence (JSON)
# - Management Inventaris Pro (Restock & Add)
# - Sistem Hutang & Cicilan Dinamis
# - Laporan Penjualan (Top Selling Items)
# - Sistem Sub-Menu (Es Rasa-Rasa)
# - Buka/Tutup Toko dengan Rekapitulasi Otomatis
# ==========================================================

import os
import time
import json
from datetime import datetime

# --- CONFIGURATION ---
DB_FILE = "rpl_canteen_elite_db.json"
DISKON_MIN = 50000
DISKON_VAL = 5000

# --- DATA MENU LENGKAP (MASTER DATA) ---
menu_master = [
    # Makanan Berat
    {"id": 1, "nama": "Pecel Lele", "stok": 20, "harga": 15000, "kat": "MAKANAN"},
    {"id": 2, "nama": "Ayam Goreng", "stok": 20, "harga": 13000, "kat": "MAKANAN"},
    {"id": 3, "nama": "Nasi Padang", "stok": 15, "harga": 18000, "kat": "MAKANAN"},
    {"id": 4, "nama": "Ayam Krispi", "stok": 25, "harga": 12000, "kat": "MAKANAN"},
    {"id": 5, "nama": "Mie Sop Spesial", "stok": 20, "harga": 10000, "kat": "MAKANAN"},
    {"id": 6, "nama": "Burger Cheese", "stok": 15, "harga": 12000, "kat": "MAKANAN"},
    # Camilan
    {"id": 7, "nama": "Malkist", "stok": 50, "harga": 2000, "kat": "CAMILAN"},
    {"id": 8, "nama": "Otak-Otak Bakar", "stok": 40, "harga": 1000, "kat": "CAMILAN"},
    {"id": 9, "nama": "Sosis Bakar", "stok": 30, "harga": 2000, "kat": "CAMILAN"},
    {"id": 10, "nama": "Kentang Goreng", "stok": 20, "harga": 7000, "kat": "CAMILAN"},
    # Minuman & Dessert
    {"id": 11, "nama": "Es Krim Cone", "stok": 25, "harga": 5000, "kat": "MINUMAN"},
    {"id": 12, "nama": "Es Rasa-Rasa", "stok": 100, "harga": 4000, "kat": "MINUMAN"},
    {"id": 13, "nama": "Es Jeruk Peras", "stok": 30, "harga": 5000, "kat": "MINUMAN"},
    {"id": 14, "nama": "Mineral Water", "stok": 60, "harga": 3000, "kat": "MINUMAN"}
]

# --- DATABASE ENGINE ---

def save_db():
    data = {
        "menu": menu_db,
        "cash": cash_db,
        "debt": debt_db,
        "logs": logs_db,
        "jam_buka": jam_buka
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_db():
    global menu_db, cash_db, debt_db, logs_db, jam_buka
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                menu_db = data.get("menu", menu_master)
                cash_db = data.get("cash", 0)
                debt_db = data.get("debt", [])
                logs_db = data.get("logs", [])
                jam_buka = data.get("jam_buka", datetime.now().strftime("%d/%m/%Y %H:%M"))
        except:
            reset_db()
    else:
        reset_db()

def reset_db():
    global menu_db, cash_db, debt_db, logs_db, jam_buka
    menu_db = menu_master
    cash_db = 0
    debt_db = []
    logs_db = []
    jam_buka = datetime.now().strftime("%d/%m/%Y %H:%M")
    save_db()

# --- UI COMPONENTS ---

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def line(c="═", n=55):
    print(c * n)

def header(txt):
    cls()
    line("╔")
    print(f"║ {txt:^51} ║")
    line("╚")

def anim(msg):
    print(f"\n   {msg}", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

# --- SUB-MENUS ---

def select_flavor():
    flavors = ["Cokelat", "Strawberry", "Vanilla", "Melon", "Taro", "Boba Milk"]
    print("\n   --- PILIHAN RASA ---")
    for i, f in enumerate(flavors, 1):
        print(f"   [{i}] {f}")
    try:
        p = int(input("\n   Pilih Rasa: "))
        return flavors[p-1]
    except:
        return "Original"

# --- MAIN LOGIC ---

def handle_transaction():
    global cash_db
    header("PENDAFTARAN PELANGGAN")
    nama = input("   👤 Nama Pelanggan : ").strip().title()
    if not nama: return

    levels = ["TK", "SD", "SMP", "SMA", "SMK", "UMUM"]
    for i, v in enumerate(levels, 1): print(f"   [{i}] {v}")
    try:
        idx = int(input("\n   Pilih Jenjang: ")) - 1
        jen = levels[idx]
        sub = "-"
        if jen in ["SMA", "SMK"]:
            sub = input(f"   Masukkan Jurusan {jen}: ").upper()
    except: jen, sub = "Umum", "-"

    cart = []
    while True:
        header(f"POS: {nama} ({jen}-{sub})")
        print(f"   {'ID':<3} | {'Item Menu':<22} | {'Stok':<5} | {'Harga'}")
        line("-")
        
        cur_cat = ""
        for m in menu_db:
            if m['kat'] != cur_cat:
                cur_cat = m['kat']
                print(f"   >> {cur_cat}")
            
            s_label = m['stok'] if m['stok'] > 0 else "Habis"
            print(f"   [{m['id']:>2}] {m['nama']:<22} | {s_label:<5} | Rp{m['harga']:,}")
        
        print("\n   [S] Selesai & Bayar | [B] Batal")
        pilih = input("\n   Masukkan ID / Aksi: ").lower()
        
        if pilih == 's':
            if cart: break
            continue
        if pilih == 'b': return

        try:
            mid = int(pilih)
            item = next((x for x in menu_db if x['id'] == mid), None)
            
            if item and item['stok'] > 0:
                final_name = item['nama']
                if mid == 12: # Es Rasa-Rasa logic
                    flavor = select_flavor()
                    final_name = f"Es Rasa {flavor}"
                
                qty = int(input(f"   Jumlah '{final_name}': "))
                if 0 < qty <= item['stok']:
                    item['stok'] -= qty
                    cart.append({"nama": final_name, "qty": qty, "price": item['harga'], "sub": qty * item['harga']})
                    # Log for reporting
                    logs_db.append({"item": item['nama'], "qty": qty, "date": datetime.now().strftime("%Y-%m-%d")})
                    print("   ✓ Ditambahkan ke keranjang.")
                else: print("   ! Stok tidak mencukupi."); time.sleep(1)
            else: print("   ! Produk tidak tersedia."); time.sleep(1)
        except: pass

    total = sum(c['sub'] for c in cart)
    disc = DISKON_VAL if total >= DISKON_MIN else 0
    netto = total - disc

    header("MENU PEMBAYARAN")
    print(f"   Total Gross : Rp{total:,}")
    if disc > 0: print(f"   Diskon RPL  : -Rp{disc:,}")
    print(f"   Total Netto : Rp{netto:,}")
    line("-")
    print("   [1] Tunai (Cash)")
    print("   [2] E-Wallet / QRIS (Simulasi)")
    print("   [3] Catat Hutang (Kredit)")
    
    pay_opt = input("\n   Pilih Metode: ")
    
    if pay_opt in ['1', '2']:
        while True:
            try:
                bayar = int(input(f"   Bayar Nominal (Min Rp{netto:,}): "))
                if bayar >= netto:
                    kembali = bayar - netto
                    cash_db += netto
                    break
                else: print("   ! Saldo tidak cukup.")
            except: print("   ! Input angka saja.")
        status = "LUNAS"
    else:
        status = "HUTANG"
        debt_db.append({"nama": nama, "ket": f"{jen}-{sub}", "total": netto, "date": datetime.now().strftime("%H:%M")})
        bayar, kembali = 0, 0

    save_db()
    header("RPL CANTEEN - INVOICE")
    print(f"   Pelanggan : {nama} ({jen}-{sub})")
    print(f"   No. Struk : {int(time.time())}")
    print(f"   Status    : {status}")
    line("-")
    for c in cart:
        print(f"   {c['qty']:>2}x {c['nama']:<22} Rp{c['sub']:,}")
    line("-")
    print(f"   NET TOTAL : Rp{netto:,}")
    if status == "LUNAS":
        print(f"   CASH      : Rp{bayar:,}")
        print(f"   KEMBALI   : Rp{kembali:,}")
    line("═")
    print(f"{'TERIMA KASIH TELAH BERBELANJA':^51}")
    input("\n   Tekan Enter untuk kembali ke Dashboard...")

def manage_inventory():
    while True:
        header("MANAJEMEN INVENTARIS")
        print("   [1] Re-Stok (Tambah Stok Barang)")
        print("   [2] Tambah Produk Baru")
        print("   [3] Hapus Produk")
        print("   [4] Kembali")
        line("-")
        cmd = input("   Pilih Aksi: ")
        
        if cmd == '1':
            header("RE-STOK BARANG")
            for m in menu_db: print(f"   [{m['id']}] {m['nama']} (Stok: {m['stok']})")
            try:
                mid = int(input("\n   Masukkan ID Menu: "))
                item = next((x for x in menu_db if x['id'] == mid), None)
                if item:
                    add = int(input(f"   Jumlah stok baru untuk '{item['nama']}': "))
                    item['stok'] += add
                    save_db()
                    anim("Updating Inventory")
            except: pass
        elif cmd == '2':
            header("TAMBAH PRODUK")
            try:
                nama = input("   Nama Produk : ")
                hrg = int(input("   Harga Jual  : "))
                stk = int(input("   Stok Awal   : "))
                kat = input("   Kategori    : ").upper()
                new_id = max([m['id'] for m in menu_db]) + 1
                menu_db.append({"id": new_id, "nama": nama, "stok": stk, "harga": hrg, "kat": kat})
                save_db()
                anim("Menyimpan Produk Baru")
            except: pass
        elif cmd == '3':
            header("HAPUS PRODUK")
            try:
                mid = int(input("   ID yang akan dihapus: "))
                menu_db[:] = [m for m in menu_db if m['id'] != mid]
                save_db()
                anim("Menghapus Data")
            except: pass
        elif cmd == '4': break

def handle_debt():
    global cash_db
    while True:
        header("PELUNASAN HUTANG")
        if not debt_db:
            print("\n   [ Tidak ada data piutang ]")
            input("\n   Enter untuk kembali..."); break
            
        for i, d in enumerate(debt_db, 1):
            print(f"   [{i}] {d['nama']} ({d['ket']}) - Rp{d['total']:,}")
        
        print("\n   [B] Bayar Hutang | [K] Kembali")
        cmd = input("   Pilih: ").lower()
        if cmd == 'b':
            try:
                idx = int(input("   Pilih No. Urut: ")) - 1
                entry = debt_db[idx]
                amt = int(input(f"   Bayar Hutang {entry['nama']} (Rp{entry['total']:,}): "))
                if amt >= entry['total']:
                    cash_db += entry['total']
                    debt_db.pop(idx)
                    anim("Hutang Telah LUNAS")
                else:
                    entry['total'] -= amt
                    cash_db += amt
                    anim(f"Cicilan Diterima. Sisa: Rp{entry['total']:,}")
                save_db()
            except: pass
        elif cmd == 'k': break

def close_shop():
    header("REKAPITULASI PENUTUPAN TOKO")
    print(f"   Sesi Dibuka : {jam_buka}")
    print(f"   Sesi Ditutup: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    line("-")
    print(f"   Total Kas (Cash) : Rp{cash_db:,}")
    print(f"   Total Piutang    : Rp{sum(d['total'] for d in debt_db):,}")
    print(f"   Total Transaksi  : {len(logs_db)} Pesanan")
    line("-")
    
    # Top selling analysis
    if logs_db:
        counts = {}
        for l in logs_db: counts[l['item']] = counts.get(l['item'], 0) + l['qty']
        best = max(counts, key=counts.get)
        print(f"   ⭐ Produk Terlaris : {best} ({counts[best]} pcs)")
    
    anim("Saving Master Database")
    print("\n   TERIMA KASIH. RPL CANTEEN RESMI DITUTUP.")
    time.sleep(2)
    exit()

# --- APP START ---

def main():
    load_db()
    while True:
        header("RPL CANTEEN DASHBOARD")
        print(f"   📅 Sesi : {jam_buka}")
        print(f"   💰 Kas  : Rp{cash_db:,}")
        print(f"   💳 Piutang : Rp{sum(d['total'] for d in debt_db):,}")
        line("-")
        print("   [1] 🛒 Transaksi Baru")
        print("   [2] 📦 Inventaris & Stok")
        print("   [3] 💳 Pelunasan Hutang")
        print("   [4] 📊 Laporan Stok Barang")
        print("   [5] 🔴 TUTUP TOKO")
        line("-")
        
        opt = input("   Pilih Menu > ")
        if opt == '1': handle_transaction()
        elif opt == '2': manage_inventory()
        elif opt == '3': handle_debt()
        elif opt == '4':
            header("DAFTAR HARGA & STOK")
            for m in menu_db:
                tag = "[!]" if m['stok'] < 5 else "   "
                print(f"   {tag} {m['nama']:<22} | {m['stok']:>3} | Rp{m['harga']:,}")
            input("\n   Tekan Enter untuk kembali...")
        elif opt == '5':
            close_shop()

if __name__ == "__main__":
    main()#