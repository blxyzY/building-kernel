# Custom Android Kernel Builder 🚀

Repositori ini digunakan untuk mengompilasi (build) kernel Android secara otomatis menggunakan **GitHub Actions**. Kamu tidak perlu memiliki PC berspesifikasi tinggi, cukup gunakan infrastruktur cloud dari GitHub.

## ✨ Fitur
- Menggunakan Ubuntu terbaru sebagai lingkungan build.
- Otomatis mengunduh Toolchain (Clang/GCC) yang ditentukan.
- Mendukung kustomisasi `defconfig` dan nama kernel.
- Hasil build (.zip atau Image) otomatis diunggah ke Github Artifacts / Release.

---

## 🛠️ Langkah-Langkah Penggunaan

Ikuti panduan berikut untuk mulai membuat kernel kamu sendiri:

### 1. Fork Repositori Ini
* Jalankan proses **Fork** pada repositori ini ke akun GitHub kamu sendiri dengan menekan tombol `Fork` di pojok kanan atas halaman ini.

### 2. Atur Variabel / Konfigurasi Kernel
* Masuk ke repositori hasil fork di akunmu.
* Buka file konfigurasi workflow yang berada di folder `.github/workflows/build-kernel.yml`.
* Edit bagian `env` (Environment Variables) sesuai dengan perangkat dan kernel yang ingin kamu build. Contoh:
  ```yaml
  env:
    KERNEL_REPO: "[https://github.com/username/android_kernel_device](https://github.com/username/android_kernel_device)"
    KERNEL_BRANCH: "lineage-21"
    KERNEL_DEFCONFIG: "vendor/device_defconfig"
    CLANG_VERSION: "r481632.1"
