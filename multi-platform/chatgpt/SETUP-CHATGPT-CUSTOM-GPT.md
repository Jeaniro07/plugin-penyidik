# Setup ChatGPT Custom GPT — Asisten Penyidik Polri

## Langkah 1: Buka GPT Builder

1. Login ke https://chatgpt.com
2. Klik **"Explore GPTs"** di sidebar kiri
3. Klik tombol **"+ Create"** (pojok kanan atas)
4. Pilih tab **"Configure"** (bukan "Create")

---

## Langkah 2: Isi Informasi GPT

| Field | Isian |
|-------|-------|
| **Name** | Asisten Penyidik Polri — Ditreskrimum |
| **Description** | Asisten penyidik untuk Ditreskrimum Polda Sulawesi. Bantu buat pertanyaan pemeriksaan, analisis bukti, review berkas, dan dokumen administrasi penyidikan sesuai KUHP/KUHAP Baru 2026. |
| **Profile Picture** | Upload logo Polri (opsional) |

---

## Langkah 3: Paste System Prompt

Di kolom **"Instructions"**, copy-paste **seluruh isi file `SYSTEM_PROMPT.md`**.

> ⚠️ Pastikan tidak ada karakter yang terpotong. Kolom ini mendukung hingga ~8.000 karakter.

---

## Langkah 4: Conversation Starters (Opsional tapi Disarankan)

Tambahkan conversation starters berikut:

```
Buatkan pertanyaan untuk pemeriksaan tersangka kasus [jelaskan kasus]
```
```
Analisis kecukupan barang bukti untuk perkara [pasal] berikut: [uraikan]
```
```
Review kelengkapan berkas perkara saya: [uraikan dokumen yang ada]
```
```
Buatkan SPDP untuk perkara [jenis perkara] dengan nomor LP [isi nomor]
```

---

## Langkah 5: Capabilities

Centang yang berikut:
- ✅ **Web Search** — untuk mencari referensi pasal terbaru
- ✅ **Code Interpreter** — untuk analisis tabel/data bukti
- ❌ DALL-E Image Generation — tidak diperlukan

---

## Langkah 6: Knowledge Files (Opsional)

Upload file-file berikut sebagai knowledge base tambahan:
- `SYSTEM_PROMPT.md` (file ini sendiri sebagai referensi)
- Dokumen SOP/PERKABA yang Anda miliki (format PDF/TXT)
- Template surat yang sering digunakan

---

## Langkah 7: Publish

1. Klik **"Save"**
2. Untuk **Access**: pilih **"Only me"** (privat, hanya Anda) atau **"Only people with a link"** (berbagi dengan rekan kerja)
3. Klik **"Confirm"**

GPT siap digunakan!

---

## Cara Menggunakan

Setelah dibuat, buka GPT Anda dan ketik perintah langsung:

```
Tersangka: Budi Santoso, kasus penipuan Pasal 378 KUHP Baru.
Korban: 5 orang, total kerugian Rp 2,3 miliar.
Bukti: transfer bank, chat WhatsApp, 3 saksi.
→ Buatkan pertanyaan pemeriksaan tersangka.
```

```
Buatkan Surat Perintah Penyidikan untuk perkara narkotika
LP Nomor: LP/B/032/IV/2026/SPKT.DITRESKRIMUM
Tersangka: [nama], tgl kejadian 5 April 2026
```

---

## Tips Penggunaan

- Makin detail deskripsi kasus yang diberikan, makin spesifik pertanyaan yang dihasilkan
- Bisa upload file BAP sebelumnya dan minta "jangan ulangi pertanyaan yang sudah ada"
- GPT akan otomatis menggunakan KUHP/KUHAP Baru sesuai system prompt
- Untuk perkara sensitif, gunakan mode **"Only me"** agar tidak bocor

---

## Biaya

Custom GPT tersedia di **ChatGPT Plus** (USD 20/bulan) atau **ChatGPT Team**.
Tidak tersedia di akun ChatGPT gratis.
