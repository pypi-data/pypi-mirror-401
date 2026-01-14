
import time

class IndoTime:
    def __init__(self, *args):
        self._wib_offset = 7 * 3600
        self._now = time.time() + self._wib_offset
        
        self._nama_hari = {
            0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis",
            4: "Jumat", 5: "Sabtu", 6: "Minggu"
        }
        self._nama_bulan = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }

        if not args:
            self._current_time = self._get_time_struct(self._now)
        else:
            # This is a simplified constructor and may not handle all edge cases.
            # For a real-world library, more robust parsing would be needed.
            if len(args) == 4: # indotime(hari, tgl, bln, thn)
                # This is a bit tricky without datetime library.
                # We'll assume the user provides valid data.
                # This is more for display than calculation.
                self._current_time = self._get_time_struct(self._now) # Fallback to now
            elif len(args) == 3: # indotime(jam, menit, detik)
                self._current_time = self._get_time_struct(self._now)
                # Not a standard struct_time, but we can fake it for our purpose
                self._current_time = time.struct_time((
                    self._current_time.tm_year, self._current_time.tm_mon, self._current_time.tm_mday,
                    args[0], args[1], args[2],
                    self._current_time.tm_wday, self._current_time.tm_yday, self._current_time.tm_isdst
                ))
            elif len(args) == 1 and isinstance(args[0], str): # indotime(bln_string)
                self._current_time = self._get_time_struct(self._now)
                # This is also for display, assuming current year and day
                month_num = list(self._nama_bulan.values()).index(args[0]) + 1
                self._current_time = time.struct_time((
                    self._current_time.tm_year, month_num, self._current_time.tm_mday,
                    self._current_time.tm_hour, self._current_time.tm_min, self._current_time.tm_sec,
                    self._current_time.tm_wday, self._current_time.tm_yday, self._current_time.tm_isdst
                ))


    def _get_time_struct(self, seconds):
        return time.gmtime(seconds)

    def hari(self):
        return self._nama_hari[self._current_time.tm_wday]

    def tanggal(self):
        return f"{self._current_time.tm_mday:02d}"

    def bulan(self):
        return f"{self._current_time.tm_mon:02d}"

    def bulan_string(self):
        return self._nama_bulan[self._current_time.tm_mon]

    def tahun(self):
        return str(self._current_time.tm_year)

    def jam(self):
        return f"{self._current_time.tm_hour:02d}:{self._current_time.tm_min:02d}:{self._current_time.tm_sec:02d}"

    def lengkap(self):
        return f"{self.hari()}, {self.tanggal()} {self.bulan_string()} {self.tahun()}, {self.jam()} WIB"

# --- Contoh Penggunaan ---
if __name__ == "__main__":
    # 1. Menampilkan tanggal dan jam lengkap saat ini
    now = IndoTime()
    print("Waktu saat ini:")
    print(f"Format Lengkap: {now.lengkap()}")
    print(f"Format Tanggal: {now.tanggal()}-{now.bulan()}-{now.tahun()}")
    print(f"Format Jam: {now.jam()}")
    print(f"Hari: {now.hari()}")
    print(f"Bulan: {now.bulan_string()}")
    print("-" * 20)

    # 2. Membuat objek dengan waktu spesifik (jam, menit, detik)
    waktu_custom = IndoTime(20, 15, 0)
    print("Waktu custom (jam):")
    print(f"Jam: {waktu_custom.jam()}")
    # Tanggal akan mengikuti tanggal hari ini
    print(f"Lengkap (dengan tanggal hari ini): {waktu_custom.lengkap()}")
    print("-" * 20)

    # 3. Membuat objek dengan bulan spesifik (dalam string)
    waktu_bulan = IndoTime("Agustus")
    print("Waktu custom (bulan):")
    print(f"Bulan: {waktu_bulan.bulan_string()}")
    # Sisa waktu akan mengikuti waktu saat ini
    print(f"Lengkap: {waktu_bulan.lengkap()}")
    print("-" * 20)
    
    # 4. Pemanggilan fleksibel lainnya (sebagai contoh konseptual)
    # Perlu diingat, implementasi untuk (hari, tgl, bln, thn) cukup rumit
    # tanpa library eksternal dan tidak diimplementasikan sepenuhnya.
    # Kode di bawah ini akan kembali ke waktu saat ini sebagai fallback.
    waktu_tanggal_custom = IndoTime("Senin", 17, 8, 1945)
    print("Contoh pemanggilan dengan tanggal custom (fallback):")
    print(waktu_tanggal_custom.lengkap())
