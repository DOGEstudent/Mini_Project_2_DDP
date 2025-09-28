import getpass
from prettytable import PrettyTable

# Watchlist Saham Saat ini
watchlist = ("BBCA", "BBRI", "BBNI", "BMRI")

# Data untuk login
users = {
    "Wellson_Lo": {"password": "CEO_Well$onL0_SeK#r!T4$_2025^X", "role": "CEO"},
    "Rahman": {"password": "HidupD1n1kMat!4jA", "role": "Nasabah"},
    "Andry_Hakim": {"password": "N0risk_NoFerr4r!", "role": "Nasabah"},
    "PT_Investment": {"password": "v9$Tq7#xPzL2!mR4wG8@", "role": "Nasabah"},
}

# list untuk simpan orders
orders = []
order_id_counter = 1


# Login
def login():
    print("\n=== LOGIN SISTEM ORDERBOOK ===")
    percobaan = 0
    max_percobaan = 3
    
    while percobaan < max_percobaan:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        
        if username in users and users[username]["password"] == password:
            print(f"Login berhasil! Selamat datang {users[username]['role']} {username}!")
            return username, users[username]["role"]
        else:
            percobaan += 1
            print(f"Login gagal! Silakan Coba lagi.")
    return None, None


# Menampilkan Orderbook dalam sebuah format tabel
def display_orderbook():
    if len(orders) == 0:
        print("\n📊 Belum ada transaksi.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Saham", "Tipe Order", "Harga", "Lot", "User"]
    
    for order in orders:
        emoji = "🟢" if order["tipe_order"] == "BID" else "🔴"
        table.add_row([
            order["id"],
            order["saham"],
            f"{emoji} {order['tipe_order']}",
            f"{order['harga']:,.0f}",
            order["lot"],
            order["username"]
        ])
    
    print("\n📊 ORDERBOOK SAHAM")
    print(table)


# Create. Tambah order
def tambah_order(username):
    global order_id_counter
    
    print("\n➕ TAMBAH ORDER BARU")
    
    try:
        # Input data order
        saham = input("Masukkan kode Saham (BBCA, BBRI, BBNI, BMRI): ").upper()
        
        if saham not in watchlist:
            print("❌ Kode saham belum ada! Saat ini hanya: BBCA, BBRI, BBNI, BMRI")
            return
        
        tipe_order = input("Posisi order (BID/ASK): ").upper()
        if tipe_order not in ["BID", "ASK"]:
            print("❌ Posisi order harus BID atau ASK!")
            return
        
        harga = float(input("Harga: "))
        if harga <= 3000:
            print("❌ Ditolak. ARB saat ini ialah 3000!")
            return
        
        lot = int(input("Lot: "))
        if lot <= 0:
            print("❌ Transaksi dibatalkan karena lot 0!")
            return
        
        # Create order dictionary
        order_baru = {
            "id": order_id_counter,
            "saham": saham,
            "tipe_order": tipe_order,
            "harga": harga,
            "lot": lot,
            "username": username
        }
        
        orders.append(order_baru)
        order_id_counter += 1
        print("✅ Order berhasil ditambahkan!")
        
    except ValueError:
        print("❌ Hanya bisa angka!")
    except Exception as e:
        print(f"❌ Error: {e}")


# Read. lihat orderbook berdasarkan role
def lihat_order(role, username):
    if len(orders) == 0:
        print("\n📊 Belum ada transaksi.")
        return
    
    table = PrettyTable()
    
    if role == "CEO":
        # CEO bisa lihat semua order transaksi
        table.field_names = ["ID", "Saham", "Tipe Order", "Harga", "Lot", "User"]
        filtered_orders = orders
        print("\n📊 PANATU ORDER")
    else:
        # Nasabah hanya bisa lihat order miliknya
        table.field_names = ["ID", "Saham", "Tipe Order", "Harga", "Lot"]
        filtered_orders = [order for order in orders if order["username"] == username]
        print(f"\n📊 LIHAT ORDER ANDA, {username}")
    
    if len(filtered_orders) == 0:
        print("Belum ada transaksi.")
        return
    
    for order in filtered_orders:
        emoji = "🟢" if order["tipe_order"] == "BID" else "🔴"
        if role == "CEO":
            table.add_row([
                order["id"],
                order["saham"],
                f"{emoji} {order['tipe_order']}",
                f"{order['harga']:,.0f}",
                order["lot"],
                order["username"]
            ])
        else:
            table.add_row([
                order["id"],
                order["saham"],
                f"{emoji} {order['tipe_order']}",
                f"{order['harga']:,.0f}",
                order["lot"]
            ])
    
    print(table)


# Update. Tampilkan order yang bisa diupdate sesuai role
def update_order(username, role):
    if role == "CEO":
        filtered_orders = orders
        print("\n📝 MAINTENANCE ORDER")
    else:
        filtered_orders = [order for order in orders if order["username"] == username]
        print(f"\n📝 UPDATE ORDER ANDA, {username}")
    
    if len(filtered_orders) == 0:
        print("❌ Tidak ada order untuk diupdate.")
        return
    
    # Tampilkan order yang tersedia
    table = PrettyTable()
    table.field_names = ["ID", "Saham", "Tipe Order", "Harga", "Lot", "User"] if role == "CEO" else ["ID", "Saham", "Tipe Order", "Harga", "Lot"]
    
    for order in filtered_orders:
        emoji = "🟢" if order["tipe_order"] == "BID" else "🔴"
        if role == "CEO":
            table.add_row([
                order["id"],
                order["saham"],
                f"{emoji} {order['tipe_order']}",
                f"{order['harga']:,.0f}",
                order["lot"],
                order["username"]
            ])
        else:
            table.add_row([
                order["id"],
                order["saham"],
                f"{emoji} {order['tipe_order']}",
                f"{order['harga']:,.0f}",
                order["lot"]
            ])
    
    print(table)
    
    try:
        order_id = int(input("\nMasukkan ID order yang akan diupdate: "))
        
        # Cari order berdasarkan ID
        order_to_update = None
        for order in orders:
            if order["id"] == order_id:
                order_to_update = order
                break
        
        if not order_to_update:
            print("❌ Order ID gak ada!")
            return
        
        # Cek hak akses
        if role != "CEO" and order_to_update["username"] != username:
            print("❌ Akses ditolak! Anda hanya bisa mengupdate order sendiri.")
            return
        
        print(f"\n📝 Mengupdate Order ID {order_id}")
        print("Kosongkan input jika tidak ingin mengubah")
        
        # Input data baru
        saham_baru = input(f"Saham [{order_to_update['saham']}]: ").upper()
        if saham_baru and saham_baru not in watchlist:
            print("❌ Kode saham belum ada!")
            return
        
        jenis_baru = input(f"Tipe order [{order_to_update['tipe_order']}]: ").upper()
        if jenis_baru and jenis_baru not in ["BID", "ASK"]:
            print("❌ Tipe order harus BID atau ASK!")
            return
        
        harga_baru = input(f"Harga [{order_to_update['harga']:,.0f}]: ")
        jumlah_baru = input(f"Lot [{order_to_update['lot']}]: ")
        
        # Update data
        if saham_baru:
            order_to_update["saham"] = saham_baru
        if jenis_baru:
            order_to_update["tipe_order"] = jenis_baru
        if harga_baru:
            order_to_update["harga"] = float(harga_baru)
        if jumlah_baru:
            order_to_update["lot"] = int(jumlah_baru)
        
        print("✅ Order berhasil diupdate!")
        
    except ValueError:
        print("❌ Input harus angka untuk ID, Harga, dan Jumlah lot!")
    except Exception as e:
        print(f"❌ Error: {e}")


# Delete. Hapus order berdasarkan role
def delete_order(username, role):
    if role == "CEO":
        filtered_orders = orders
        print("\n🗑️  BATALKAN ORDER")
    else:
        filtered_orders = [order for order in orders if order["username"] == username]
        print(f"\n🗑️  BATALKAN ORDER ANDA, {username}")
    
    if len(filtered_orders) == 0:
        print("❌ Tidak ada order untuk dibatalkan karena kosong.")
        return
    
    # Tampilkan order yang tersedia
    table = PrettyTable()
    table.field_names = ["ID", "Saham", "Tipe Order", "Harga", "Lot", "User"] if role == "CEO" else ["ID", "Saham", "Tipe Order", "Harga", "Lot"]
    
    for order in filtered_orders:
        emoji = "🟢" if order["tipe_order"] == "BID" else "🔴"
        if role == "CEO":
            table.add_row([
                order["id"],
                order["saham"],
                f"{emoji} {order['tipe_order']}",
                f"{order['harga']:,.0f}",
                order["lot"],
                order["username"]
            ])
        else:
            table.add_row([
                order["id"],
                order["saham"],
                f"{emoji} {order['tipe_order']}",
                f"{order['harga']:,.0f}",
                order["lot"]
            ])
    
    print(table)
    
    try:
        order_id = int(input("\nMasukkan ID order yang akan dibatalkan: "))
        
        # Cari order berdasarkan ID
        for hapus, order in enumerate(orders):
            if order["id"] == order_id:
                # Cek hak akses
                if role != "CEO" and order["username"] != username:
                    print("❌ Akses ditolak! Anda hanya bisa membatalkan order sendiri.")
                    return
                
                confirm = input(f"Apakah Anda yakin ingin membatalkan order dengan ID {order_id}? (y/n): ").lower()
                if confirm == 'y':
                    del orders[hapus]
                    print("✅ Transaksi Order berhasil dibatalkan!")
                else:
                    print("❌ Transaksi Order tidak jadi dibatalkan.")
                return
        
        print("❌ Order ID tidak ditemukan!")
        
    except ValueError:
        print("❌ Input ID harus angka!")
    except Exception as e:
        print(f"❌ Error: {e}")


# Menunya CEO
def menu_CEO(username):
    while True:
        print(f"\n=== MENU UTAMA CEO ===")
        print("1. Tambah Order Baru")
        print("2. Lihat Semua Order")
        print("3. Update Order")
        print("4. Delete Order")
        print("5. Logout")
        print("6. Keluar Platform")
        
        try:
            pilihan = int(input("Pilih menu: "))
            
            if pilihan == 1:
                tambah_order(username)
            elif pilihan == 2:
                lihat_order("CEO", username)
            elif pilihan == 3:
                update_order(username, "CEO")
            elif pilihan == 4:
                delete_order(username, "CEO")
            elif pilihan == 5:
                print("Logout berhasil.")
                return True  # Kembali ke login
            elif pilihan == 6:
                print("Terima kasih telah menggunakan Orderbook Emiten.🙏🏻")
                return False  # Keluar platform
            else:
                print("❌ Sorry CEO, Pilihan hanya 1-6.🙏🏻")
                
        except ValueError:
            print("❌ Sorry CEO. Input cuma bisa angka.🙏🏻")
        except Exception as e:
            print(f"❌ Error: {e}")


# Menu Nasabah
def menu_nasabah(username):
    while True:
        print(f"\n=== MENU UTAMA ===")
        print("1. Tambah Order Baru")
        print("2. Lihat Order Saya")
        print("3. Update Order Saya")
        print("4. Delete Order Saya")
        print("5. Logout")
        print("6. Keluar Program")
        
        try:
            pilihan = int(input("Pilih menu: "))
            
            if pilihan == 1:
                tambah_order(username)
            elif pilihan == 2:
                lihat_order("Nasabah", username)
            elif pilihan == 3:
                update_order(username, "Nasabah")
            elif pilihan == 4:
                delete_order(username, "Nasabah")
            elif pilihan == 5:
                print("Logout berhasil!")
                return True  # Kembali ke login
            elif pilihan == 6:
                print("Terima kasih telah menggunakan Orderbook Emiten!")
                return False  # Keluar platform
            else:
                print("❌ Cuma bisa pilih 1-6!")
                
        except ValueError:
            print("❌ Pilih angka!")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    print("=== SISTEM ORDERBOOK EMITEN ===")
    print(" Simulasi Cara Kerja Orderbook ")
    
    while True:
        # Sistem Login
        username, role = login()
        
        if username is None:  # Jika login gagal 3x
            print("\n⚠ Akses Diblokir Sementara. Silakan Kembali esok.")
            break
        
        # Redirect ke login screen sesuai role
        if role == "CEO":
            should_relogin = menu_CEO(username)
        else:
            should_relogin = menu_nasabah(username)
        
        # Jika user memilih logout, kembali ke login screen
        if not should_relogin:
            break

if __name__ == "__main__":
    main()