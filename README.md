# Asisten Penyidik Polri

**Plugin AI untuk penyidik Kepolisian Negara Republik Indonesia**
Dikonfigurasi untuk **Direktorat Reserse Kriminal Umum (Ditreskrimum) Polda Sulawesi**

[![Versi](https://img.shields.io/badge/versi-0.5.0-blue)](.)
[![Dasar Hukum](https://img.shields.io/badge/KUHAP%20Baru-UU%2020%2F2025-green)](.)
[![KUHP Baru](https://img.shields.io/badge/KUHP%20Baru-UU%201%2F2023-green)](.)
[![Platform](https://img.shields.io/badge/platform-Claude%20%7C%20ChatGPT%20%7C%20Copilot%20%7C%20Telegram%20%7C%20WhatsApp%20%7C%20Web-orange)](.)

---

## Daftar Isi

- [Tentang Plugin](#tentang-plugin)
- [Platform yang Didukung](#platform-yang-didukung)
- [Instalasi & Setup](#instalasi--setup)
- [Kemampuan](#kemampuan)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Repositori](#struktur-repositori)
- [Dasar Hukum](#dasar-hukum)
- [Kustomisasi Satuan](#kustomisasi-satuan)

---

## Tentang Plugin

Plugin ini membantu penyidik Polri dalam:

- Menyusun **pertanyaan pemeriksaan** tersangka, saksi, pelapor, korban, dan ahli berdasarkan unsur pasal yang dipersangkakan
- Melakukan **analisis barang bukti** dengan pendekatan GraphRAG (peta relasi antar entitas) dan simulasi skenario what-if
- **Mereview kelengkapan berkas** perkara dari tiga perspektif serentak: Penyidik, Jaksa, dan Hakim (simulasi)
- Membuat **dokumen administrasi penyidikan** (SP.Sidik, SP.Gas, SPDP, surat panggilan, BAP, resume, dan 69+ jenis dokumen lainnya)

Seluruh konten mengacu pada ketentuan terbaru yang berlaku efektif **2 Januari 2026**:
PERKABA No. 1/2022 · KUHP Baru (UU No. 1/2023 jo. UU No. 1/2026) · KUHAP Baru (UU No. 20/2025)

---

## Platform yang Didukung

Plugin ini tersedia di **6 platform**. Pilih yang paling sesuai dengan kebutuhan satuan Anda.

| Platform | File | Keterangan |
|----------|------|-----------|
| **Claude Desktop (Cowork)** | `asisten-penyidik-polri.plugin` | Instalasi langsung, fitur paling lengkap |
| **ChatGPT** | `chatgpt/SETUP-CHATGPT-CUSTOM-GPT.md` | Custom GPT di ChatGPT Plus |
| **Microsoft Copilot / Teams** | `copilot/SETUP-MICROSOFT-COPILOT.md` | Integrasi Microsoft 365 |
| **Bot Telegram** | `bot/telegram_bot.py` | Bot Python siap deploy |
| **Bot WhatsApp** | `bot/whatsapp_bot.py` | Via Twilio + Flask |
| **Web App (browser)** | `webapp/index.html` | Buka langsung di browser, tanpa install |

> **Rekomendasi untuk memulai cepat:** buka `webapp/index.html` di browser, masukkan OpenAI API key, langsung bisa digunakan.

---

## Instalasi & Setup

### Claude Desktop (Cowork) — Fitur Paling Lengkap

1. Download file `asisten-penyidik-polri.plugin` dari repositori ini
2. Buka **Claude Desktop** → **Cowork mode**
3. Buka pengaturan Plugin
4. Drag & drop file `.plugin` ke jendela Claude
5. Plugin aktif secara otomatis

### Web App (Paling Mudah — Tanpa Install)

1. Download file `webapp/index.html`
2. Buka file tersebut di browser (Chrome, Edge, Firefox)
3. Di sidebar kiri, masukkan **OpenAI API key** atau **Anthropic API key**
4. Langsung gunakan

> API key disimpan hanya di browser lokal Anda (localStorage). Tidak tersimpan di server manapun.

### Bot Telegram

```bash
# 1. Install dependensi
pip install -r bot/requirements.txt

# 2. Salin dan isi konfigurasi
cp bot/.env.example bot/.env
# Edit .env: isi TELEGRAM_BOT_TOKEN dan OPENAI_API_KEY

# 3. Jalankan bot
python bot/telegram_bot.py
```

Cara mendapatkan token Telegram: chat dengan **@BotFather**, ketik `/newbot`.

### Bot WhatsApp

```bash
# 1. Install dependensi
pip install -r bot/requirements.txt

# 2. Isi konfigurasi Twilio di .env
# (daftar di twilio.com, aktifkan WhatsApp Sandbox)

# 3. Jalankan server
python bot/whatsapp_bot.py

# 4. Expose ke internet (untuk menerima webhook Twilio)
ngrok http 5000
```

### ChatGPT Custom GPT

Ikuti panduan lengkap di `chatgpt/SETUP-CHATGPT-CUSTOM-GPT.md`.
Membutuhkan akun **ChatGPT Plus** (USD 20/bulan).

### Microsoft Copilot / Teams

Ikuti panduan di `copilot/SETUP-MICROSOFT-COPILOT.md`.
Tersedia tiga opsi: Copilot Chat biasa, Copilot Studio, atau langsung di Word/Outlook.

---

## Kemampuan

### Perintah Tersedia

| Perintah | Fungsi |
|----------|--------|
| `/pertanyaan-tersangka` | Pertanyaan BAP tersangka berbasis unsur pasal + GraphRAG + matriks what-if |
| `/pertanyaan-saksi` | Pertanyaan BAP saksi — bervariasi, tidak mengulang BAP sebelumnya |
| `/pertanyaan-pelapor` | Pertanyaan BAP pelapor berdasarkan kronologi pelaporan |
| `/pertanyaan-korban` | Pertanyaan BAP korban — dampak, kerugian, hak restitusi/kompensasi |
| `/pertanyaan-ahli` | Pertanyaan pemeriksaan ahli — pendapat teknis dan analisis barang bukti |
| `/analisis-bukti` | Analisis kecukupan bukti + GraphRAG + skenario what-if + opini publik |
| `/review-kasus` | Review berkas dari perspektif Penyidik + Jaksa + Hakim (simulasi) |

### Keahlian (Skills)

| Skill | Fungsi |
|-------|--------|
| **Administrasi Penyidikan** | 69+ template dokumen: SP.Sidik, SP.Gas, SPDP, BAP, surat panggilan, surat perintah penangkapan/penahanan/penyitaan/penggeledahan, SP2HP, dan lainnya |
| **Prosedur Penyidikan** | Panduan lengkap KUHAP Baru: alat bukti baru (Pasal 235), penetapan tersangka (Pasal 90), penahanan (Pasal 100), keadilan restoratif, hak advokat/korban |
| **Resume Penyidikan** | Panduan membuat resume format S-1.1.3 dengan analisis yuridis berdasarkan KUHP Baru |

### Fitur Unggulan

**GraphRAG — Peta Pengetahuan Kasus**
Memetakan relasi antar entitas perkara (tersangka, korban, saksi, barang bukti, transaksi, lokasi) untuk menemukan koneksi tersembunyi dan mengidentifikasi gap pembuktian.

**Simulasi Skenario What-If**
Uji ketangguhan berkas sebelum dilimpahkan ke Jaksa dengan mensimulasikan 4 skenario: alibi terbukti, saksi cabut keterangan, bukti elektronik ditolak, tersangka ajukan keadilan restoratif.

**Review Multi-Agent (Penyidik + Jaksa + Hakim)**
`/review-kasus` menghadirkan review dari tiga perspektif serentak untuk meminimalkan risiko P-18/P-19 atau putusan bebas.

**Sistem Pembuktian KUHAP Baru (Pasal 235)**
Menggunakan 7+ jenis alat bukti yang sah. Alat bukti "petunjuk" dari KUHAP lama telah dihapus; bukti elektronik kini diakui secara eksplisit.

---

## Cara Penggunaan

### Di Claude Desktop / Web App / ChatGPT

Cukup deskripsikan kebutuhan Anda secara natural:

```
Tersangka Budi Santoso, kasus penggelapan dalam jabatan Pasal 374 KUHP Baru.
Korban: PT Maju Bersama. Kerugian: Rp 1,2 miliar.
Bukti: rekening koran, CCTV, 4 saksi.
→ Buatkan pertanyaan pemeriksaan tersangka.
```

```
Buatkan SPDP untuk perkara narkotika:
LP Nomor: LP/B/032/IV/2026/SPKT.DITRESKRIMUM
Tersangka: [nama], tgl kejadian 10 April 2026
```

### Di Bot Telegram

```
/tersangka Kasus penipuan Pasal 378, tersangka Andi, korban 5 orang, kerugian Rp 800 juta
/saksi Saksi mata kasus penganiayaan, melihat kejadian dari jarak 5 meter
/bukti Barang bukti: pisau dapur, baju berdarah, rekaman CCTV, keterangan 2 saksi
/surat SPDP perkara narkoba LP/B/012/IV/2026
```

### Di Bot WhatsApp

Kirim pesan langsung ke nomor bot:
```
tersangka kasus korupsi pengadaan barang Pasal 2 UU Tipikor, tersangka Pak X, jabatan PPK
review berkas penyidikan: sudah ada LP, SP.Sidik, BAP 3 saksi, belum ada SP2HP
```

---

## Struktur Repositori

```
plugin-penyidik/
├── asisten-penyidik-polri.plugin       # File plugin untuk Claude Desktop
├── SYSTEM_PROMPT.md                    # System prompt universal (semua platform)
│
├── asisten-penyidik-polri/             # Source plugin
│   ├── config/
│   │   └── profil-satuan.md            # Konfigurasi satuan (edit di sini)
│   ├── commands/                       # Definisi perintah
│   ├── skills/                         # Keahlian (administrasi, prosedur, resume)
│   └── README.md
│
├── bot/                                # Bot Telegram & WhatsApp
│   ├── telegram_bot.py
│   ├── whatsapp_bot.py
│   ├── requirements.txt
│   └── .env.example
│
├── webapp/
│   └── index.html                      # Web app mandiri
│
├── chatgpt/
│   └── SETUP-CHATGPT-CUSTOM-GPT.md
│
└── copilot/
    └── SETUP-MICROSOFT-COPILOT.md
```

---

## Dasar Hukum

| Regulasi | Ketentuan |
|----------|-----------|
| **PERKABA No. 1 Tahun 2022** | SOP Administrasi Penyidikan Tindak Pidana |
| **UU No. 2 Tahun 2002** | Kepolisian Negara Republik Indonesia |
| **UU No. 1 Tahun 2023** | KUHP Baru — Kitab Undang-Undang Hukum Pidana |
| **UU No. 1 Tahun 2026** | Penyesuaian terhadap Ketentuan Pidana (55 perubahan KUHP) |
| **UU No. 20 Tahun 2025** | KUHAP Baru — Kitab Undang-Undang Hukum Acara Pidana |
| **Perkapolri No. 6 Tahun 2019** | Penyidikan Tindak Pidana |

Seluruh ketentuan baru berlaku efektif **2 Januari 2026**.

---

## Kustomisasi Satuan

Edit file `asisten-penyidik-polri/config/profil-satuan.md` untuk menyesuaikan:

- Nama spesifik Polda (Sulsel / Sulteng / Sulut / Sultra / Sulbar)
- Nama Direktur Reskrimum dan pangkat/NRP
- Alamat kantor dan nomor telepon satuan
- Kode resmi Polda untuk format nomor surat

---

## Catatan Keamanan

- Jangan memasukkan data perkara sensitif (nama tersangka/korban yang dapat diidentifikasi) ke layanan AI publik
- Gunakan versi Claude Desktop (Cowork) atau web app lokal untuk dokumen rahasia
- Untuk deployment instansi, gunakan Microsoft Copilot Studio dengan tenant terisolir
- API key disimpan hanya di browser lokal (web app) atau file `.env` lokal (bot)

---

*Penyidik: Jean — Ditreskrimum Polda Sulawesi*
*Plugin v0.5.0 — Terakhir diperbarui: April 2026*
