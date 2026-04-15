# Asisten Penyidik Polri v0.5.0

**Plugin AI untuk penyidik Kepolisian Negara Republik Indonesia**
Dikonfigurasi untuk **Direktorat Reserse Kriminal Umum (Ditreskrimum) Polda Sulawesi**

Tersedia di: Claude Desktop (Cowork) · ChatGPT · Microsoft Copilot · Bot Telegram · Bot WhatsApp · Web App

Dasar hukum yang digunakan:

| Regulasi | Keterangan |
|----------|-----------|
| **PERKABA No. 1 Tahun 2022** | SOP Administrasi Penyidikan Tindak Pidana |
| **UU No. 1 Tahun 2023** | KUHP Baru — Kitab Undang-Undang Hukum Pidana |
| **UU No. 1 Tahun 2026** | Penyesuaian terhadap Ketentuan Pidana (55 perubahan) |
| **UU No. 20 Tahun 2025** | KUHAP Baru — Kitab Undang-Undang Hukum Acara Pidana |

Seluruh ketentuan berlaku efektif sejak **2 Januari 2026**.

## Perintah (Commands)

| Perintah | Fungsi |
|----------|--------|
| `/pertanyaan-tersangka` | Buat pertanyaan interogasi tersangka berdasarkan **unsur-unsur pasal** yang dipersangkakan |
| `/pertanyaan-saksi` | Buat pertanyaan pemeriksaan saksi — **bervariasi**, tidak mengulang pertanyaan dari BAW sebelumnya |
| `/pertanyaan-pelapor` | Buat pertanyaan pemeriksaan pelapor berdasarkan unsur pasal dan kronologi pelaporan |
| `/pertanyaan-korban` | Buat pertanyaan pemeriksaan korban — dampak, kerugian, identifikasi pelaku, hak restitusi/kompensasi |
| `/pertanyaan-ahli` | Buat pertanyaan pemeriksaan ahli — pendapat ahli tentang unsur pasal, analisis barang bukti |
| `/analisis-bukti` | Analisis kecukupan barang bukti dan rekomendasi langkah lanjutan (termasuk bukti elektronik) |
| `/review-kasus` | Review kelengkapan dan kualitas berkas penyidikan |

## Keahlian (Skills)

| Skill | Fungsi |
|-------|--------|
| **Prosedur Penyidikan** | Panduan lengkap prosedur penyidikan sesuai KUHAP Baru — termasuk alat bukti baru (Pasal 235), penetapan tersangka (Pasal 90), penahanan (Pasal 100), keadilan restoratif, hak advokat/korban |
| **Resume Penyidikan** | Panduan membuat resume penyidikan format S-1.1.3 — analisa yuridis berdasarkan KUHP Baru |
| **Administrasi Penyidikan** | Panduan dan template untuk membuat 69+ jenis dokumen administrasi dan surat menyurat penyidikan |

## Fitur Utama

### Pertanyaan Berbasis Unsur Pasal
Setiap command pertanyaan akan mengidentifikasi pasal yang dipersangkakan (mengacu KUHP Baru UU 1/2023 jo. UU 1/2026), menguraikan unsur-unsurnya, dan membuat pertanyaan yang secara spesifik menggali pemenuhan setiap unsur.

### Variasi Pertanyaan Otomatis
Plugin akan membaca BAW (Berita Acara Wawancara) yang sudah ada dalam folder kasus dan memastikan pertanyaan baru **tidak mengulang** pertanyaan yang sudah pernah diajukan kepada saksi/pihak sebelumnya.

### Sistem Pembuktian Baru (KUHAP Baru Pasal 235)
Plugin mengacu pada 7+ jenis alat bukti sah menurut KUHAP Baru: keterangan saksi, keterangan ahli, surat, keterangan terdakwa, **barang bukti**, **bukti elektronik**, **pengamatan hakim**, dan segala sesuatu yang diperoleh secara tidak melawan hukum. Alat bukti "petunjuk" dari KUHAP lama telah dihapus.

### Hak Tersangka, Korban, dan Advokat
Plugin memperhatikan ketentuan baru tentang hak tersangka (Pasal 142 KUHAP Baru), hak advokat (akses salinan BAP), hak korban (restitusi dan kompensasi), serta mekanisme keadilan restoratif.

### Template Administrasi Lengkap
Skill administrasi mencakup template untuk: Laporan Polisi (Model A & B), SP.Sidik, SP.Gas, SPDP, Surat Panggilan, Surat Perintah Penangkapan/Penahanan/Penyitaan/Penggeledahan, Visum et Repertum, Surat Permintaan ke Instansi, SP2HP, dan banyak lagi.

### GraphRAG — Peta Pengetahuan Kasus
Command `/analisis-bukti` kini menyertakan pemetaan knowledge graph dari berkas perkara — membangun peta relasi antar entitas (tersangka, korban, saksi, barang bukti, transaksi, lokasi) untuk menemukan koneksi tersembunyi, mengidentifikasi gap pembuktian, dan mendeteksi aktor atau barang bukti sentral yang menjadi simpul utama tindak pidana.

### Simulasi Skenario What-If
Penyidik dapat menguji ketangguhan berkas sebelum pelimpahan dengan mensimulasikan skenario persidangan — alibi terbukti, saksi mencabut keterangan, bukti elektronik ditolak, tersangka ajukan keadilan restoratif — dan mendapatkan rekomendasi langkah antisipasi konkret untuk setiap skenario.

### Panel Review Multi-Agent (Penyidik, Jaksa, Hakim Simulasi)
Command `/review-kasus` kini menyertakan review berkas dari tiga perspektif serentak: sudut pandang Penyidik (kepatuhan PERKABA), Jaksa Penuntut Umum (kesiapan dakwaan), dan simulasi Hakim (ketangguhan pembuktian di persidangan). Pendekatan ini meminimalkan risiko P-18/P-19 atau putusan bebas.

### Simulasi Opini Publik
Untuk perkara berprofil tinggi, plugin dapat memodelkan bagaimana masyarakat kemungkinan merespons suatu perkara — mengidentifikasi narasi yang berpotensi berkembang, risiko interferensi tekanan publik terhadap proses hukum, dan rekomendasi pengelolaan informasi penyidikan.

## Cara Penggunaan

### Di Claude Desktop (Cowork)

Gunakan perintah langsung, atau cukup deskripsikan kebutuhan secara natural:

```
/pertanyaan-tersangka [path folder kasus atau deskripsi]
/pertanyaan-saksi    [path folder kasus atau deskripsi]
/pertanyaan-pelapor  [deskripsi kasus]
/pertanyaan-korban   [deskripsi kasus]
/pertanyaan-ahli     [deskripsi kasus dan jenis ahli]
/analisis-bukti      [path folder kasus]
/review-kasus        [path folder berkas perkara]
```

Untuk administrasi dan surat menyurat, cukup minta secara natural — misalnya "buatkan SPDP" atau "buat surat panggilan untuk saksi" — skill administrasi-penyidikan akan otomatis aktif.

### Di Platform Lain

Plugin ini juga tersedia di platform lain menggunakan `SYSTEM_PROMPT.md` sebagai fondasi. Lihat folder masing-masing untuk panduan setup:

| Platform | Folder/File | Cara Akses |
|----------|-------------|-----------|
| **ChatGPT** | `chatgpt/` | Custom GPT di ChatGPT Plus |
| **Microsoft Copilot / Teams** | `copilot/` | Copilot Studio atau Teams |
| **Bot Telegram** | `bot/telegram_bot.py` | Python, jalankan sendiri |
| **Bot WhatsApp** | `bot/whatsapp_bot.py` | Python + Twilio |
| **Web App** | `webapp/index.html` | Buka langsung di browser |

Contoh perintah di bot Telegram/WhatsApp:
```
tersangka Kasus penggelapan Pasal 374 KUHP Baru, tersangka Andi, kerugian Rp 500 juta
saksi    Saksi mata kejadian, melihat tersangka membawa barang milik korban
bukti    BB: rekening koran, CCTV, keterangan 3 saksi, HP tersangka
review   LP sudah ada, SP.Sidik ada, BAP 2 saksi, belum ada resume
surat    SPDP perkara narkotika LP/B/032/IV/2026/SPKT.DITRESKRIMUM
```

## Kustomisasi Satuan

Edit `config/profil-satuan.md` untuk menyesuaikan identitas satuan Anda:
- Nama spesifik Polda (Sulsel / Sulteng / Sulut / Sultra / Sulbar)
- Nama Direktur Reskrimum dan pangkat/NRP
- Alamat kantor, nomor telepon, dan kode satuan untuk format nomor surat

## Dasar Hukum

| Regulasi | Keterangan |
|----------|-----------|
| **PERKABA No. 1 Tahun 2022** (Lampiran II) | SOP Administrasi Penyidikan |
| **UU No. 2 Tahun 2002** | Kepolisian Negara Republik Indonesia |
| **UU No. 1 Tahun 2023** | KUHP Baru |
| **UU No. 1 Tahun 2026** | Penyesuaian Pidana (55 perubahan KUHP) |
| **UU No. 20 Tahun 2025** | KUHAP Baru |
| **Perkapolri No. 6 Tahun 2019** | Penyidikan Tindak Pidana |

Seluruh ketentuan baru berlaku efektif **2 Januari 2026**.

## Perubahan di v0.5.0

- **GraphRAG pada semua command pertanyaan**: Semua 5 command pembuatan pertanyaan (tersangka, saksi, pelapor, korban, ahli) kini menyertakan pre-analysis GraphRAG — memetakan posisi pihak yang diperiksa dalam jaringan entitas perkara sebelum pertanyaan disusun
- **Strategi interogasi multi-agent pada pertanyaan-tersangka**: Strategi interogasi diperluas dengan tiga perspektif serentak — Penyidik, Jaksa (apa yang dibutuhkan untuk dakwaan), dan Hakim simulasi (apa yang perlu terdokumentasi untuk meyakinkan majelis)
- **Matriks skenario what-if pembelaan pada pertanyaan-tersangka**: Tabel skenario pembelaan (bantah semua / akui sebagian / alibi / keadilan restoratif) dengan pertanyaan kritis dan alat bukti pendukung untuk setiap skenario
- **Catatan multi-perspektif pada semua pertanyaan saksi, pelapor, korban, ahli**: Setiap command pertanyaan kini menyertakan perspektif Jaksa dan Hakim simulasi, skenario what-if spesifik per peran, dan pertanyaan "pengunci" untuk mendokumentasikan keterangan kritis
- **Skenario opini publik pada pertanyaan-korban**: Pertimbangan identitas korban, perlindungan dari tekanan publik, dan dampak eksposur media terintegrasi dalam strategi pemeriksaan
- **GraphRAG entity mapping pada pertanyaan-ahli**: Secara eksplisit mengidentifikasi entitas dan relasi spesifik dalam knowledge graph perkara yang harus dinilai oleh ahli

## Perubahan di v0.4.0

- **GraphRAG**: Penambahan pemetaan knowledge graph pada `/analisis-bukti` (bagian G) — memetakan relasi antar entitas untuk menemukan koneksi tersembunyi dan gap pembuktian
- **Skenario What-If**: Simulasi rekonstruksi alternatif pada `/analisis-bukti` (bagian H) — uji ketangguhan berkas dengan 4 skenario persidangan sebelum pelimpahan ke Jaksa
- **Panel Review Multi-Agent**: Review perspektif Penyidik + Jaksa + Hakim simulasi pada `/review-kasus` (bagian I) — identifikasi kelemahan berkas dari tiga sudut pandang serentak
- **Simulasi Opini Publik**: Analisis dinamika sosial pada `/review-kasus` (bagian J) dan `/analisis-bukti` (bagian I) — untuk perkara berprofil tinggi
- **Teknik Investigasi Lanjutan**: Panduan GraphRAG, what-if, multi-agent, dan opini publik terintegrasi dalam skill prosedur-penyidikan
- **Penguatan Resume**: Peta relasi antar-entitas (C) dan uji skenario what-if (D) ditambahkan ke dalam bagian Pembahasan resume penyidikan

## Perubahan di v0.3.0

- Pembaruan menyeluruh mengacu KUHAP Baru (UU No. 20/2025)
- Sistem alat bukti baru Pasal 235 (menggantikan Pasal 184 KUHAP lama)
- Penambahan bukti elektronik sebagai alat bukti sah
- Ketentuan penetapan tersangka minimal 2 alat bukti (Pasal 90)
- Ketentuan penahanan baru — ancaman 5 tahun atau lebih (Pasal 100)
- Penambahan mekanisme keadilan restoratif
- Hak advokat diperluas (akses salinan BAP)
- Hak korban — restitusi dan kompensasi
- Penambahan UU No. 1 Tahun 2026 tentang Penyesuaian Pidana
- Pembaruan template dokumen sesuai format baru

## Penulis

Jean — Penyidik Polri
