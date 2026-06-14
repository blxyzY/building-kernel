# Ubuntu-Termux Kernel Builder 🚀

Sebuah panduan dan kumpulan skrip otomatisasi untuk melakukan kompilasi (build) kernel Linux atau Android langsung dari perangkat Android Anda menggunakan lingkungan **Ubuntu PRoot di Termux**.

## 📌 Prasyarat Sistem
Sebelum memulai, pastikan perangkat Anda memenuhi spesifikasi minimum berikut untuk menghindari kegagalan kompilasi:
* **Penyimpanan Kosong:** Minimal 15 GB s.d 30 GB (tergantung besar source kernel).
* **RAM:** Minimal 4 GB s.d 6GB+ (Disarankan mengaktifkan ZRAM/Swap).
* **Aplikasi:** [Termux (F-Droid)](https://f-droid.org) terbaru.

---

## 🛠️ Langkah 1: Menyiapkan Lingkungan Ubuntu
Buka Termux Anda, lalu jalankan perintah berikut untuk masuk ke chroot/proot Ubuntu:

```bash
# Pastikan Termux tidak sleep selama proses build
termux-wake-lock

# Masuk ke Ubuntu
proot-distro login ubuntu
```

---

## 📦 Langkah 2: Menginstal Dependensi Kompilasi
Di dalam terminal Ubuntu, instal seluruh paket dasar, compiler, dan pustaka yang dibutuhkan untuk membangun kernel:

```bash
apt update && apt upgrade -y
apt install -y git build-essential bc bison flex libssl-dev libelf-dev \
               ccache clang lld libncurses-dev xz-utils curl kmod rsync \
               cpio tzdata
```

---

## 📂 Langkah 3: Mengklon Source Kernel & Toolchain
Pilihlah *source code* kernel yang sesuai dengan tipe perangkat Anda serta *Toolchain* (seperti Proton Clang, GCC, atau AOSP Clang).

```bash
# Buat direktori kerja
mkdir -p ~/kernel-workspace && cd ~/kernel-workspace

# Klon Source Kernel (Contoh)
git clone --depth=1 <URL_REPOS_KERNEL_ANDA> android_kernel

# Klon Toolchain Compiler (Contoh: Proton Clang)
git clone --depth=1 https://github.com toolchain
```

---

## 🚀 Langkah 4: Proses Kompilasi (Building)

### 1. Ekspor Variabel Lingkungan (Environment Variables)
Arahkan compiler ke folder *toolchain* yang sudah diunduh sebelumnya:

```bash
export PATH="~/kernel-workspace/toolchain/bin:\$PATH"
export ARCH=arm64
export SUBARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export CC=clang
```

### 2. Atur Konfigurasi Defconfig
Ganti `nama_defconfig` dengan file konfigurasi bawaan target perangkat Anda (bisa ditemukan di folder `arch/arm64/configs/`):

```bash
cd android_kernel
make nama_defconfig
```

### 3. Mulai Kompilasi
Gunakan perintah `nproc` untuk memanfaatkan seluruh *core* CPU Android Anda agar proses lebih cepat:

```bash
make -j\$(nproc)
```

Jika kompilasi berhasil tanpa error, file kernel utama (`Image.gz`, `Image.gz-dtb`, atau `Image`) akan berada di direktori `arch/arm64/boot/`.

---

## ⚠️ Troubleshooting & Tips Singkat

* **Error `No rule to make target 'debian/canonical-certs.pem'`**
  Buka file `.config` atau jalankan perintah:
  ```bash
  scripts/config --disable SYSTEM_REVOCATION_KEYS
  scripts/config --disable SYSTEM_TRUSTED_KEYS
  ```
* **Termux Tiba-Tiba Keluar (Force Close):**
  Biasanya dipicu oleh kehabisan RAM (*Out of Memory*). Kurangi jumlah thread saat *build*, misalnya gunakan `make -j2` atau `make -j4` alih-alih `make -j$(nproc)`.
* **Gunakan AnyKernel3:** Untuk memaketkan hasil `Image.gz` menjadi file `.zip` flashable yang bisa dipasang via TWRP/OrangeFox.

---

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
