# Setup Microsoft Copilot Studio — Asisten Penyidik Polri

## Opsi A: Microsoft Copilot Chat (Paling Mudah)

Jika instansi Anda menggunakan **Microsoft 365 / Teams**, bisa langsung menggunakan Copilot dengan menyisipkan system prompt di awal percakapan.

### Cara Cepat di Teams/Copilot Chat:

1. Buka **Microsoft Copilot** (copilot.microsoft.com) atau buka **Teams → Copilot**
2. Mulai percakapan baru
3. Di pesan pertama, paste system prompt berikut lalu Enter:

```
[Paste seluruh isi SYSTEM_PROMPT.md di sini]

Konfirmasi bahwa kamu siap membantu sebagai Asisten Penyidik Polri untuk Ditreskrimum Polda Sulawesi.
```

4. Copilot akan mengkonfirmasi dan siap digunakan untuk sesi tersebut.

> ⚠️ **Catatan**: Dengan cara ini, system prompt hanya berlaku untuk satu sesi. Harus diulang setiap memulai percakapan baru.

---

## Opsi B: Copilot Studio (Permanen & Lebih Baik)

Untuk membuat asisten permanen yang bisa diakses seluruh anggota satuan via Teams.

### Persyaratan:
- Akun Microsoft 365 dengan lisensi **Copilot Studio** (atau Power Platform)
- Akses admin ke tenant organisasi

### Langkah-langkah:

#### 1. Buka Copilot Studio
- Buka https://copilotstudio.microsoft.com
- Login dengan akun Microsoft 365 instansi

#### 2. Buat Copilot Baru
- Klik **"Create"** → **"New copilot"**
- Isi nama: `Asisten Penyidik Polri`
- Bahasa: **Indonesian**
- Klik **"Create"**

#### 3. Tambahkan System Prompt (Instructions)
- Buka tab **"Settings"** → **"AI capabilities"**
- Di bagian **"Instructions"**, paste seluruh isi `SYSTEM_PROMPT.md`
- Klik **"Save"**

#### 4. Tambahkan Knowledge Base (Opsional)
- Buka tab **"Knowledge"**
- Klik **"Add knowledge"** → **"Upload file"**
- Upload dokumen referensi:
  - Template surat penyidikan (.docx / .pdf)
  - PERKABA No. 1/2022 (jika ada filenya)
  - SOP satuan Anda

#### 5. Publish ke Microsoft Teams
- Buka tab **"Channels"** → **"Microsoft Teams"**
- Klik **"Add to Teams"**
- Ikuti proses instalasi
- Bagikan ke anggota tim Ditreskrimum

---

## Opsi C: Copilot dalam Microsoft Word/Outlook

Untuk membuat dokumen administrasi penyidikan langsung dari Word:

1. Buka **Microsoft Word** dengan Copilot aktif
2. Klik ikon Copilot di ribbon
3. Ketik perintah seperti:

```
Berperan sebagai asisten penyidik Polri (Ditreskrimum Polda Sulawesi).
Buatkan Surat Perintah Penyidikan dengan format PERKABA 2022 dan
dasar hukum KUHP Baru (UU 1/2023) dan KUHAP Baru (UU 20/2025).
Perkara: [isi perkara]
```

---

## Biaya Microsoft Copilot Studio

| Paket | Harga | Keterangan |
|-------|-------|-----------|
| Microsoft 365 Copilot | USD 30/user/bulan | Termasuk Copilot di Teams, Word, Outlook |
| Copilot Studio | USD 200/bulan per tenant | Untuk membuat custom copilot |
| Power Platform (legacy) | Bervariasi | Bisa untuk bot sederhana |

> Hubungi IT atau pengadaan instansi untuk pembelian lisensi enterprise.

---

## Tips Keamanan Data

- Gunakan **akun Microsoft 365 instansi** (bukan akun pribadi) agar data perkara terlindungi
- Aktifkan **sensitivity labels** untuk dokumen rahasia
- Jangan memasukkan data tersangka/korban yang identifiable ke Copilot publik
- Gunakan **Copilot Studio** dengan tenant terisolir untuk keamanan data maksimal
