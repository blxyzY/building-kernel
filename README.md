# Custom Android Kernel Builder 🚀

This repository allows you to compile (build) an Android kernel automatically using **GitHub Actions**. No high-spec PC required—just leverage GitHub's cloud infrastructure.

## ✨ Features
- Uses the latest Ubuntu environment for building.
- Automatically downloads specified Toolchains (Clang/GCC).
- Supports customization for `defconfig`, kernel names, and compiler flags.
- Uploads the final build (.zip or Image) directly to GitHub Artifacts / Releases.

---

## 🛠️ Step-by-Step Guide

Follow these steps to start building your custom kernel:

### 1. Fork This Repository
* Click the **Fork** button at the top right corner of this page to copy this repository to your own GitHub account.

### 2. Configure Kernel Variables
* Go to your forked repository.
* Navigate to and open the workflow configuration file located at `.github/workflows/build-kernel.yml`.
* Edit the `env` (Environment Variables) section to match your device and kernel source. Example:
```yaml
  env:
    KERNEL_REPO: "https://github.com/blxyzY/ScamsungKernel.git"
    KERNEL_BRANCH: "main"
    KERNEL_DEFCONFIG: "vendor/device_defconfig"
    CLANG_VERSION: "clang-10"
