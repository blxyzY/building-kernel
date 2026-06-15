# 🚀 Scamsung Kernel Builder

Repositori ini digunakan untuk mengompilasi (compile) Android Kernel `arm64` secara otomatis menggunakan GitHub Actions dan langsung mengunggah hasilnya ke halaman **GitHub Releases**.

---

## 🛠️ Struktur Repositori Wajib

Sebelum menjalankan, pastikan repositori GitHub kamu memiliki struktur seperti ini:
```text
├── .github/workflows/build.yml  # Berkas script workflow
└── ScamsungKernel/              # Folder berkas AnyKernel3 milikmu (Wajib ada)
