

import os  # mengecek apakah file yg di tuju ada, kalo ga dia bisa buat atau hapus dan yg lainnya
import sys # kalo ini buat kalo ada perintah lansung berhenti dia akan rapih berhentinya tanpa menjalankan baris berikutnya

FILENAME = "database_siswa.txt"

# ---------------------------
# Helper functions
# ---------------------------
def hitung_statistik(nilai_list):
    """
    ngitung rata-rata (avg), nilai_tertinggi(maks), nilai_terendah(min).
    Mengembalikan tuple (avg , maks , min ). karena dia tidak bisa di ubah
    Jika list kosong, avg = 0, maks = None, min = None.
    """
    if not nilai_list:
        return 0, None, None
    total = sum(nilai_list)          #sum menjumlahkan semua angka dalam list.
    avg = total / len(nilai_list)     # len ngitung jumlah item yg ada di list
    return avg, max(nilai_list), min(nilai_list)  # return ngembaliin nilai yg di inginkan

def tentukan_grade(avg):
    """
    Menentukan grade berdasarkan aturan:
    >=85 A, >=75 B, >=65 C, >=50 D, <50 E
    Mengembalikan sebuah string grade.
    """
    try:
        if avg >= 85:
            return "A"
        if avg >= 75:
            return "B"
        if avg >= 65:
            return "C"
        if avg >= 50:
            return "D"
        return "E"
    except TypeError:
        return "E"

# ---------------------------
# File I/O
# ---------------------------
def load_data(filename):
    """
    Membaca file database_siswa.txt dan mengembalikan dictionary:
    { 'NIS': {'nama': '...', 'nilai': [..]}, ... }
    Jika file tidak ada, kembalikan dict kosong.
    Baris yang malformed akan di-skip dengan peringatan.
    """
    data = {} # siapkan dictionary kosong buat nyimpen hasil.
    if not os.path.exists(filename):   #os.path.exists -> ngecek apakah file ada atau tidak 
        return data

    try:
        with open(filename, "r", encoding="utf-8") as f:   # encoding="utf-8" = biar aman kalau ada karakter khusus (misalnya huruf é, ü, dll).
            for line_num, raw in enumerate(f, start=1):  # enumerate → ngasih nomor baris (line_num) + isi baris (raw). start=1 biar mulai dari 1 bukan 0
                line = raw.strip() #  hapus spasi/enter di awal & akhir baris.
                if line == "": 
                    continue
                # Format: NIS,NAMA,VAL1;VAL2;VAL3
                parts = line.split(",", 2)  # maksimal 3 bagian biar jadi 3 bagian
                if len(parts) < 2:
                    print(f"[Peringatan] Baris {line_num} diabaikan (format salah).")
                    continue
                nis = parts[0].strip()
                nama = parts[1].strip() if len(parts) >= 2 else ""
                nilai_list = []
                if len(parts) == 3 and parts[2].strip() != "":  # parts[2].strip() != "" → artinya kolom nilai nggak kosong. Kalau kosong → berarti siswa belum ada nilai → dilewati.
                    nilai_strs = parts[2].split(";")   #Fungsi split(";") dipakai untuk memecah string berdasarkan tanda ; jadinya list 
                    for v in nilai_strs:
                        v = v.strip()
                        if v == "":
                            continue
                        try:
                            nilai_list.append(int(v))
                        except ValueError:
                            # coba float->int, atau skip jika tidak bisa
                            try:
                                nilai_list.append(int(float(v)))
                            except Exception:
                                print(f"[Peringatan] Nilai '{v}' pada baris {line_num} diabaikan.")
                                continue
                data[nis] = {"nama": nama, "nilai": nilai_list}
    except Exception as e:
        print(f"[Error] Gagal membaca file: {e}")
    return data

def save_data(data, filename):
    """
    Menyimpan dictionary 'data' ke file dengan format:
    NIS,Nama,VAL1;VAL2;VAL3
    Menimpa file lama.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f: # with .... as f = "Hei Python, buka file ini, lalu selama blok ini jalan, panggil aja file itu dengan nama f. Setelah blok selesai, tutup otomatis."
            for nis, info in data.items():
                nama = info.get("nama", "").strip()
                nilai_list = info.get("nilai", [])
                nilai_str = ";".join(str(int(v)) for v in nilai_list) if nilai_list else ""
                line = f"{nis},{nama},{nilai_str}\n"
                f.write(line)
        return True
    except Exception as e:
        print(f"[Error] Gagal menyimpan data: {e}")
        return False

# ---------------------------
# Fitur menu (fungsi terpisah)
# ---------------------------
def lihat_daftar_siswa(data_siswa):
    """
    Menampilkan daftar semua siswa: NIS: Nama Lengkap
    """
    if not data_siswa:
        print("Belum ada data siswa.")
        return
    print("\nDaftar Siswa:")
    for nis in sorted(data_siswa.keys()):       # sorted() dipakai biar daftar siswa tampil urut berdasarkan NIS → rapi & gampang dibaca.
        nama = data_siswa[nis].get("nama", "")
        print(f"{nis}: {nama}")
    print()

def lihat_detail_siswa(data_siswa):
    """
    Meminta NIS, lalu menampilkan detail (NIS, Nama, daftar nilai, rata-rata, max, min, grade)
    """
    nis = input("Masukkan NIS siswa: ").strip()
    if nis == "":
        print("NIS tidak boleh kosong.")
        return
    if nis not in data_siswa:
        print(f"NIS {nis} tidak ditemukan.")
        return
    info = data_siswa[nis]
    nama = info.get("nama", "")          # ambil nama (kalau gak ada, isi string kosong)
    nilai_list = info.get("nilai", [])    # ambil nilai (kalau gak ada, isi list kosong)
    avg, maks, mn = hitung_statistik(nilai_list)
    grade = tentukan_grade(avg)
    print("\n--- Detail Siswa ---")
    print(f"NIS   : {nis}")
    print(f"Nama  : {nama}")
    if nilai_list:
        print("Nilai : " + ", ".join(str(int(v)) for v in nilai_list))
    else:
        print("Nilai : (belum ada nilai)")
    # Tampilkan statistik
    print(f"Rata-rata : {avg:.2f}")
    if maks is not None and mn is not None:
        print(f"Nilai Tertinggi : {int(maks)}")
        print(f"Nilai Terendah  : {int(mn)}")
    else:
        print("Nilai Tertinggi : -")
        print("Nilai Terendah  : -")
    print(f"Grade Akhir : {grade}")
    print("-------------------\n")

def tambah_siswa_baru(data_siswa):
    """
    Menambah siswa baru: minta NIS dan nama. Validasi NIS duplicate.
    """
    nis = input("Masukkan NIS baru: ").strip()
    if nis == "":
        print("NIS tidak boleh kosong.")
        return
    if nis in data_siswa:
        print(f"Error: NIS {nis} sudah terdaftar. Pembatalan penambahan.")
        return
    nama = input("Masukkan Nama Lengkap: ").strip()
    if nama == "":
        print("Nama tidak boleh kosong. Pembatalan penambahan.")
        return
    data_siswa[nis] = {"nama": nama, "nilai": []}
    print(f"Siswa dengan NIS {nis} bernama '{nama}' berhasil ditambahkan.\n")

def tambah_nilai_siswa(data_siswa):
    """
    Menambah nilai untuk siswa yang sudah ada.
    """
    nis = input("Masukkan NIS siswa: ").strip()
    if nis == "":
        print("NIS tidak boleh kosong.")
        return
    if nis not in data_siswa:
        print(f"NIS {nis} tidak ditemukan. Pembatalan penambahan nilai.")
        return
    # Minta nilai baru sebagai angka
    raw = input("Masukkan nilai baru (0-100): ").strip()
    if raw == "":
        print("Input kosong. Pembatalan.")
        return
    try:
        nilai = float(raw)
        # float(raw) → mengubah input user (raw) jadi angka desimal (misalnya "85" jadi 85.0)
        nilai_int = int(nilai)
        # Setelah jadi float, ubah ke integer (int). Misalnya 85.0 jadi 85
        if not (0 <= nilai_int <= 100):
            print("Nilai harus antara 0 dan 100. Pembatalan.")
            return
        data_siswa[nis].setdefault("nilai", []).append(nilai_int)   #setdefault("nilai", []) artinya kalau siswa belum punya list nilai, otomatis dibuat list kosong [].
        print(f"Nilai {nilai_int} berhasil ditambahkan untuk NIS {nis}.\n")
    except ValueError:
        print("Input bukan angka yang valid. Pembatalan.")

def simpan_dan_keluar(data_siswa, filename):
    """
    Menyimpan data ke file dan mengakhiri program.
    Mengembalikan tuple (status_bool, pesan)
    """
    ok = save_data(data_siswa, filename)
    if ok:
        return True, "Data berhasil disimpan. Program berakhir."
    else:
        return False, "Terjadi kesalahan saat menyimpan data."

# ---------------------------
# Main program
# ---------------------------
def main():
    print("=== Sistem Informasi Siswa (SIS) Sederhana ===")
    # Saat mulai: muat file jika ada
    data_semua_siswa = load_data(FILENAME)   #Manggil fungsi load_data() buat baca isi file database_siswa.txt
    if data_semua_siswa:
        print(f"Data dimuat dari '{FILENAME}'. Jumlah siswa: {len(data_semua_siswa)}")
    else:
        # Jika file tidak ada atau kosong
        if os.path.exists(FILENAME):
            print(f"'{FILENAME}' ada tetapi tidak memuat data siswa yang valid.")
        else:
            print(f"Tidak ditemukan file '{FILENAME}'. Memulai dengan data kosong.")

    # Loop utama
    while True:
        print("\n--- Sistem Informasi Siswa ---")
        print("1. Lihat Daftar Siswa")
        print("2. Lihat Detail Siswa")
        print("3. Tambah Siswa Baru")
        print("4. Tambah Nilai Siswa")
        print("5. Simpan & Keluar")
        print("------------------------------")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_daftar_siswa(data_semua_siswa)
        elif pilihan == "2":
            lihat_detail_siswa(data_semua_siswa)
        elif pilihan == "3":
            tambah_siswa_baru(data_semua_siswa)
        elif pilihan == "4":
            tambah_nilai_siswa(data_semua_siswa)
        elif pilihan == "5":
            status, pesan = simpan_dan_keluar(data_semua_siswa, FILENAME)
            print(pesan)
            # Hentikan program
            if status:
                break
            else:
                # jika penyimpanan gagal, tetap di loop agar user bisa coba lagi
                continue
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Jika user tekan Ctrl+C, coba simpan dulu (opsional)
        print("\nTerhenti oleh pengguna (KeyboardInterrupt).")
        # Menawarkan penyimpanan sebelum keluar
        try:
            ans = input("Simpan data sebelum keluar? (y/n): ").strip().lower()
            if ans == "y":
                # muat ulang data dari runtime (tidak ada akses ke scope main's data_semua_siswa)
                # Jadi sarankan user menjalankan lagi program dan memilih Simpan & Keluar.
                print("Maaf — untuk menyimpan, jalankan program lagi dan pilih 'Simpan & Keluar'.")
        except Exception:
            pass
        print("Keluar tanpa menyimpan.")
        sys.exit(0)   # sys.exit() dipakai untuk menghentikan program Python secara paksa tapi rapi.