# **📘 RUNBOOK & DEPLOYMENT GUIDE: BOOK TRACKER APP**

Dokumen ini berfungsi sebagai panduan operasional utama untuk melakukan deployment, monitoring, penanganan masalah, serta pemulihan (*rollback*) sistem Book Tracker App.

## **🏗️ 1\. Diagram Arsitektur (ASCII)**

Aplikasi ini menggunakan desain *multi-container* yang terisolasi dengan dua jaringan (*network*) Docker terpisah untuk memisahkan lalu lintas operasional aplikasi dan aktivitas pemantauan (monitoring).

\==========================================================================================  
                                 ARCHITECTURE DIAGRAM  
\==========================================================================================

  HOST / PUBLIC NETWORK  
    │  
    ├── Port 8080 (Frontend UI) ──────────┐  
    ├── Port 5001 (Backend API) ────┐     │  
    ├── Port 5432 (Postgres DB) ──┐ │     │  
    ├── Port 9090 (Prometheus) ─┐ │ │     │  
    └── Port 3000 (Grafana) ──┐ │ │ │     │  
                              │ │ │ │     │  
──────────────────────────────┼─┼─┼─┼─────┼───────────────────────────────────────────────  
  DOCKER CONTAINERS           │ │ │ │     │  
                              │ │ │ │   ┌─▼───────────────────┐  
                              │ │ │ │   │      fe (UI)        │  
                              │ │ │ │   │  (build: ./frontend)│  
                              │ │ │ │   └─────────┬───────────┘  
                              │ │ │ │             │  
                              │ │ │ │             │ \[depends\_on: service\_healthy\]  
                              │ │ │ │             ▼  
                              │ │ │ ┌─────────────▼───────────┐  
                              │ │ │ │     be (API)            │  
                              │ │ │ │  (build: ./backend)     │  
                              │ │ │ └─────────────┬───────────┘  
                              │ │ │               │  
                              │ │ │               │ \[depends\_on: service\_healthy\]  
                              │ │ │               ▼  
                              │ │ ┌───────────────▼───────────┐  
                              │ │ │          db               │ ◄─── \[init.sql (bind mount)\]  
                              │ │ │  (postgres:17-alpine)     │  
                              │ │ └───────────────┬───────────┘  
                              │ │                 │  
                              │ │                 ▼  
                              │ │         \[ pg-data (Volume) \]  
                              │ │  
                              │ ┌───────────────▼─────────────┐  
                              │ │         prometheus          │ ◄─── \[config & alerts (bind)\]  
                              │ │   (prom/prometheus:v2)      │  
                              │ └─────────────────┬───────────┘  
                              │                   │  
                              │                   ▼  
                              │         \[ prom-data (Volume) \]  
                              │  
                        ┌─────▼───────────────────┐  
                        │        grafana          │  
                        │  (grafana/grafana:10)   │ ◄─── \[provisioning (bind mount)\]  
                        └─────────┬───────────────┘  
                                  │  
                                  ▼  
                         \[ grafana-data (Vol) \]

────────────────────────────────────────────────────────────────────────────────────────  
  DOCKER NETWORKS  
                                    ┌──────────────────────┐  
                                    │  postgres-exporter   │  
                                    └────┬────────────┬────┘  
                                         │            │  
                                         │            │  
  \[app-net\] ─────────────────────────────┴────────────┼─────────────────────────────────  
    ├── fe (Frontend)                                 │  
    ├── be (Backend)                                  │  
    ├── db (Postgres Database)                        │  
    └── postgres-exporter                             │  
                                                      │  
  \[monitoring-net\] ───────────────────────────────────┴─────────────────────────────────  
    ├── prometheus (Metrics Collector)  
    ├── grafana (Dashboard Visualizer)  
    └── postgres-exporter (Metrics Exporter)

\==========================================================================================  
                                  TRAFFIC & DATA FLOW  
\==========================================================================================

1\. Jalur Request Aplikasi : Client Browser ──► fe:8080 ──► be:5001 ──► db:5432  
2\. Jalur Monitoring       : grafana:3000 ──► prometheus:9090  
                            prometheus:9090 ──► postgres-exporter ──► db:5432

### **🔒 Analisis Isolasi Keamanan & Jaringan**

* **Isolasi Network (app-net):** Menampung container aplikasi utama (fe, be, db) serta agen pengumpul data database (postgres-exporter).  
* **Isolasi Monitoring (monitoring-net):** Digunakan secara khusus oleh tim operasional untuk membatasi akses visualisasi metrik (grafana) agar terisolasi dari traffic publik aplikasi.  
* **Bridge Component:** postgres-exporter dan prometheus berada di kedua jaringan untuk menjembatani pengumpulan metrik dari database menuju sistem visualisasi.

## **🚀 2\. Panduan Deployment (Langkah demi Langkah)**

### **Prasyarat Sistem**

* **Docker Engine** versi 24.0.0 atau yang lebih baru.  
* **Docker Compose** versi 2.20.0 atau yang lebih baru.  
* Hak akses administratif (sudo jika di lingkungan Linux).

### **Langkah 1: Kloning Repositori & Persiapan Direktori**

git clone \<url-repository-anda\> book-tracker  
cd book-tracker

### **Langkah 2: Mengonfigurasi Environment Variables**

Pastikan file .env untuk masing-masing container telah siap di root direktori proyek Anda sesuai dengan template berikut:

1. **db.env** (Untuk Database PostgreSQL):  
   POSTGRES\_USER=bookuser  
   POSTGRES\_PASSWORD=bookpass  
   POSTGRES\_DB=bookdb

2. **be.env** (Untuk Backend Flask):  
   FLASK\_ENV=development  
   FLASK\_DEBUG=True  
   FLASK\_HOST=0.0.0.0  
   FLASK\_PORT=5001  
   DATABASE\_URL=postgresql://bookuser:bookpass@db:5432/bookdb  
   CORS\_ORIGINS=http://localhost:8080,http://localhost:5173,\[http://127.0.0.1:8080\](http://127.0.0.1:8080),\[http://127.0.0.1:5173\](http://127.0.0.1:5173)  
   SECRET\_KEY=dev-secret-key-change-in-production-123456789  
   API\_PREFIX=/api  
   DATA\_FILE=books.json

3. **fe.env** (Untuk Frontend React/Vite):  
   VITE\_API\_URL=http://localhost:5001  
   VITE\_API\_BASE\_URL=http://localhost:5001/api  
   VITE\_APP\_TITLE=Book Tracker App (Dev)  
   VITE\_APP\_DESCRIPTION=A full-stack web application for managing your reading list  
   VITE\_NODE\_ENV=development  
   VITE\_ENABLE\_ANALYTICS=false  
   VITE\_ENABLE\_DEBUG=true  
   VITE\_ENABLE\_MOCK\_DATA=true  
   VITE\_API\_TIMEOUT=10000  
   VITE\_SHOW\_DEV\_TOOLS=true

*(Opsional)* Ekspor password administrasi Grafana ke environment sistem host sebelum menjalankan container:

export GRAFANA\_PASSWORD="TulisPasswordAmanDisini"

### **Langkah 3: Menjalankan Stack Aplikasi dengan Docker Compose**

Jalankan perintah berikut untuk mengunduh image, mem-build source code lokal backend & frontend, serta mengaktifkan seluruh service dalam mode latar belakang (*detached mode*):

docker compose up \-d \--build

### **Langkah 4: Memverifikasi Kesehatan Layanan**

Sistem menggunakan healthcheck berjenjang. Jalankan perintah di bawah ini untuk melihat status kesehatan setiap service:

docker compose ps

Pastikan kolom **STATUS** menunjukkan Up (healthy) untuk container db dan be.

## **📊 3\. Panduan Mengakses Monitoring**

Sistem monitoring dirancang untuk bekerja secara otomatis sejak pertama kali stack dijalankan menggunakan taktik *provisioning*.

### **1\. Prometheus (Time-Series Database & Metrics Collector)**

* **URL Akses:** http://localhost:9090  
* **Cara Penggunaan:**  
  * Buka menu **Status** \-\> **Targets** di navigasi atas.  
  * Pastikan target scrape postgres-exporter berstatus UP.  
  * Anda dapat menuliskan query *PromQL* sederhana di tab *Graph* (contoh: pg\_up atau pg\_stat\_database\_numbackends) untuk memverifikasi status database.

### **2\. Grafana (Dashboard Visualisasi Grafis)**

* **URL Akses:** http://localhost:3000  
* **Kredensial Default:**  
  * **Username:** admin  
  * **Password:** Sesuai nilai variabel ${GRAFANA\_PASSWORD} yang Anda set pada langkah deployment (jika tidak di-set, default-nya adalah admin).  
* **Melihat Dashboard:**  
  * Masuk ke menu **Dashboards**.  
  * Dashboard PostgreSQL metrics yang disediakan oleh postgres-exporter sudah otomatis ter-import berkat konfigurasi volume di folder ./monitoring/grafana/provisioning.

## **🔄 4\. Prosedur Pemulihan (How to Roll Back)**

Jika terjadi kegagalan sistem setelah Anda memperbarui kode atau konfigurasi (misalnya performa backend menurun drastis, db crash loop, dll.), ikuti langkah pemulihan cepat berikut:

### **Strategi A: Rollback Kode dan Konfigurasi (Tanpa Menghapus Data)**

Gunakan metode ini jika data di database aman, namun aplikasi mengalami kerusakan fungsionalitas (*buggy release*).

1. **Hentikan container yang bermasalah saat ini:**  
   docker compose down

2. **Kembalikan kode sumber ke commit Git stabil terakhir:**  
   git checkout \<hash-commit-stabil-sebelumnya\>

3. **Build ulang container menggunakan kode yang sudah di-rollback:**  
   docker compose up \-d \--build

### **Strategi B: Emergency Hard-Reset (Hapus Semua State & Rollback)**

⚠️ **PERHATIAN:** Langkah ini akan menghapus semua data transaksi aplikasi, histori log Prometheus, dan dashboard lokal Grafana. Gunakan hanya jika skema database rusak parah dan Anda ingin kembali ke kondisi awal bersih (*clean state*).

1. **Matikan seluruh service beserta seluruh volume Docker terikat:**  
   docker compose down \-v

2. **Hapus cache build yang usang dari memori Docker:**  
   docker builder prune \-f

3. **Kembalikan kode sumber sistem ke rilis stabil terakhir:**  
   git checkout \<hash-commit-stabil-sebelumnya\>

4. **Deploy ulang seluruh stack dari awal:**  
   Database akan ter-inisialisasi ulang secara otomatis menggunakan file SQL mentah yang terletak di ./backend/init.sql.  
   docker compose up \-d \--build

## **🛠️ 5\. Troubleshooting Ringkas**

| Gejala Masalah | Penyebab Umum | Solusi |
| :---- | :---- | :---- |
| **Backend (be) stuck dalam status unhealthy** | Database Postgres belum siap menerima koneksi saat backend mulai memeriksa API health. | Periksa log backend dengan docker compose logs be. Pastikan DATABASE\_URL di be.env sudah benar dan mengarah ke host db. |
| **Error CORS di browser client** | Port atau alamat frontend belum didaftarkan di backend. | Edit file be.env pada bagian CORS\_ORIGINS untuk mencantumkan URL asal frontend Anda (misal: http://localhost:8080). |
| **Grafana tidak menampilkan metrik DB** | Target postgres-exporter tidak dapat terhubung ke DB Postgres. | Pastikan DATA\_SOURCE\_NAME di bagian postgres-exporter pada file docker-compose.yml menggunakan kredensial yang sama dengan yang tertera di db.env. |

