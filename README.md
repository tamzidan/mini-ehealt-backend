# Backend - Aplikasi Booking Dokter

Ini adalah layanan backend REST API untuk aplikasi booking dokter. Dibangun menggunakan **Python** dengan framework **Flask**, API ini menyediakan semua logika bisnis, manajemen data, dan otentikasi yang dibutuhkan oleh aplikasi frontend.

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Deskripsi Proyek

Proyek ini merupakan bagian backend dari aplikasi *full-stack* yang memungkinkan pengguna untuk mencari dokter, melihat jadwal, dan melakukan booking konsultasi. Backend ini bertanggung jawab untuk:
-   Menyediakan data dokter, termasuk detail dan jadwal.
-   Mengelola proses booking dan ketersediaan slot waktu.
-   Berinteraksi dengan database PostgreSQL untuk menyimpan dan mengambil data.

---

## 🔗 Link Terkait

-   **Dokumentasi API (Swagger/OpenAPI)**: `https://github.com/tamzidan/mini-ehealt-backend/blob/main/api-doc.json`
-   **Repositori Frontend**: `https://github.com/tamzidan/mini-ehealt-frontend`
-   **Live Demo Frontend**: `https://mini-ehealt-frontend.vercel.app`

---

## ✨ Fitur Utama

-   **Manajemen Dokter**: Endpoint untuk mendapatkan daftar dokter dengan filter, paginasi, dan detail spesifik.
-   **Manajemen Jadwal**: Menyediakan data jadwal yang tersedia untuk setiap dokter.
-   **Sistem Booking**: Endpoint untuk membuat booking baru dengan validasi ketersediaan slot.
-   **Kesehatan Sistem**: Endpoint `/health` untuk memonitor status aplikasi dan koneksi database.

---

## 🛠️ Tumpukan Teknologi (Tech Stack)

-   **Bahasa**: Python
-   **Framework**: Flask
-   **ORM**: SQLAlchemy
-   **Database**: PostgreSQL
-   **Server Produksi**: Gunicorn
-   **Deployment**: Railway
-   **Desain API**: Swagger / OpenAPI
-   **Version Control**: Git & GitHub

---

## 🚀 Menjalankan Proyek Secara Lokal

Berikut adalah panduan untuk menjalankan proyek ini di lingkungan pengembangan lokal.

### Prasyarat

-   Python 3.10+
-   PostgreSQL terinstal dan berjalan di komputer Anda.
-   Git

### Langkah-langkah Instalasi

1.  **Clone Repositori**
    ```bash
    git clone [https://github.com/tamzidan/mini-ehealt-backend.git](https://github.com/tamzidan/mini-ehealt-backend.git)
    cd mini-ehealt-backend
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install Dependensi**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Environment Variables**
    -   Buat file baru bernama `.env` di direktori root proyek.
    -   Salin konten dari `.env.example` (jika ada) atau isi dengan format berikut, sesuaikan dengan konfigurasi database PostgreSQL lokal Anda.

    ```env
    # file: .env
    DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<database_name>"
    FRONTEND_URL="http://localhost:3000"
    ```

5.  **Setup Database**
    -   Pastikan Anda sudah membuat database di PostgreSQL lokal Anda.
    -   Jalankan perintah berikut di terminal untuk membuat semua tabel berdasarkan model SQLAlchemy.
    ```bash
    # Buka Flask Shell
    flask shell
    # Di dalam shell, jalankan perintah berikut
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

6.  **(Opsional) Jalankan Seeder**
    -   Jika Anda ingin mengisi database dengan data awal, jalankan script seeder.
    ```bash
    python seed.py
    ```

7.  **Jalankan Aplikasi**
    ```bash
    flask run
    ```
    Aplikasi sekarang akan berjalan di `http://127.0.0.1:5000`.

---

## API Endpoints

Berikut adalah beberapa contoh endpoint utama yang tersedia:

| Method | Endpoint                    | Deskripsi                               |
| :----- | :-------------------------- | :-------------------------------------- |
| `GET`  | `/v1/health`                | Memeriksa status kesehatan aplikasi.    |
| `GET`  | `/v1/doctors`               | Mendapatkan daftar dokter dengan filter.  |
| `GET`  | `/v1/doctors/<id>`          | Mendapatkan detail satu dokter.         |
| `GET`  | `/v1/doctors/<id>/schedule` | Mendapatkan jadwal dokter.              |
| `POST` | `/v1/bookings`              | Membuat booking baru.                   |

---

## ☁️ Deployment

Aplikasi ini di-deploy ke **Railway**. Setiap *push* ke *branch* `main` akan secara otomatis memicu proses build dan deployment baru. *Environment variables* untuk produksi (seperti `DATABASE_URL` internal dan `FRONTEND_URL`) dikelola melalui dashboard Railway.

**Start Command** yang digunakan di Railway adalah: