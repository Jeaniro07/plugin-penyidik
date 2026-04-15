"""
Bot Telegram — Asisten Penyidik Polri
Ditreskrimum Polda Sulawesi

Persyaratan:
  pip install python-telegram-bot openai python-dotenv

Cara menjalankan:
  1. Salin file .env.example ke .env dan isi token
  2. python telegram_bot.py

Cara mendapatkan token:
  - Telegram Bot Token: chat dengan @BotFather di Telegram, ketik /newbot
  - OpenAI API Key: https://platform.openai.com/api-keys
  - (Opsional) Anthropic API Key: https://console.anthropic.com/
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
import openai

load_dotenv()

# ─── Konfigurasi ────────────────────────────────────────────────────────────

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Opsional: batasi akses hanya ke ID Telegram tertentu (keamanan)
ALLOWED_USER_IDS = set(
    int(x) for x in os.getenv("ALLOWED_USER_IDS", "").split(",") if x.strip()
)

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── System Prompt ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
Kamu adalah Asisten Penyidik Polri yang berpengalaman, dikonfigurasi untuk
Direktorat Reserse Kriminal Umum (Ditreskrimum) Polda Sulawesi.

KETENTUAN HUKUM WAJIB:
- KUHP Baru: UU No. 1/2023 jo. UU No. 1/2026 tentang Penyesuaian Pidana
- KUHAP Baru: UU No. 20/2025 (berlaku 2 Januari 2026)
- Pasal 90 KUHAP Baru: penetapan tersangka minimal 2 alat bukti sah
- Pasal 100 KUHAP Baru: penahanan hanya untuk ancaman 5 tahun atau lebih
- Pasal 142 KUHAP Baru: hak tersangka (advokat, keadilan restoratif)
- Pasal 235 KUHAP Baru: 7+ jenis alat bukti sah (petunjuk dihapus, bukti elektronik masuk)
- PERKABA No. 1/2022: SOP administrasi penyidikan

SATUAN: Ditreskrimum Polda Sulawesi
KOPSTUK: KEPOLISIAN NEGARA REPUBLIK INDONESIA / DAERAH SULAWESI [...] / DIREKTORAT RESERSE KRIMINAL UMUM
PERKARA PRIORITAS: Pidana Umum, Tipidkor, Narkoba, Siber/ITE

KEMAMPUAN:
1. Buat pertanyaan pemeriksaan tersangka (dengan analisis unsur pasal, GraphRAG, matriks what-if)
2. Buat pertanyaan pemeriksaan saksi/pelapor/korban/ahli
3. Analisis kecukupan barang bukti
4. Review kelengkapan berkas perkara
5. Buat dokumen administrasi: SP.Sidik, SP.Gas, SPDP, surat panggilan, BAP, resume penyidikan

FORMAT OUTPUT: Bahasa Indonesia formal. Terstruktur dengan heading yang jelas.
Untuk pertanyaan: beri nomor, target unsur, dan tujuan setiap pertanyaan.

Jawab langsung dan profesional. Jika diminta membuat surat, langsung buat template lengkap.
"""

# ─── Riwayat Percakapan (per user) ──────────────────────────────────────────

conversation_history: dict[int, list[dict]] = {}

def get_history(user_id: int) -> list[dict]:
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    return conversation_history[user_id]

def add_to_history(user_id: int, role: str, content: str):
    history = get_history(user_id)
    history.append({"role": role, "content": content})
    # Batasi riwayat 20 pesan terakhir untuk hemat token
    if len(history) > 20:
        conversation_history[user_id] = history[-20:]

# ─── Fungsi AI ───────────────────────────────────────────────────────────────

async def ask_ai(user_id: int, user_message: str) -> str:
    add_to_history(user_id, "user", user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(user_id)

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=4000,
            temperature=0.3,  # Rendah untuk konsistensi dokumen hukum
        )
        assistant_message = response.choices[0].message.content
        add_to_history(user_id, "assistant", assistant_message)
        return assistant_message
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return f"❌ Terjadi kesalahan saat menghubungi AI: {str(e)}"

# ─── Handler ─────────────────────────────────────────────────────────────────

def is_authorized(user_id: int) -> bool:
    if not ALLOWED_USER_IDS:
        return True  # Jika tidak ada whitelist, izinkan semua
    return user_id in ALLOWED_USER_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("⛔ Akses tidak diizinkan.")
        return

    welcome = (
        "🚔 *Asisten Penyidik Polri — Ditreskrimum Polda Sulawesi*\n\n"
        "Saya siap membantu tugas penyidikan Anda.\n\n"
        "*Perintah yang tersedia:*\n"
        "• Ketik langsung deskripsi kasus\n"
        "• /tersangka — pertanyaan pemeriksaan tersangka\n"
        "• /saksi — pertanyaan pemeriksaan saksi\n"
        "• /bukti — analisis barang bukti\n"
        "• /review — review kelengkapan berkas\n"
        "• /surat — buat dokumen administrasi\n"
        "• /reset — hapus riwayat percakapan\n"
        "• /bantuan — tampilkan panduan\n\n"
        "_Dasar hukum: KUHP Baru (UU 1/2023) · KUHAP Baru (UU 20/2025) · PERKABA 2022_"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    help_text = (
        "📋 *Panduan Penggunaan*\n\n"
        "*Cara 1 — Ketik Langsung:*\n"
        "Cukup deskripsikan kebutuhan Anda, contoh:\n"
        "_\"Buatkan pertanyaan untuk tersangka kasus penggelapan Pasal 372 KUHP Baru, "
        "tersangka Budi Santoso, korban PT XYZ, kerugian Rp 500 juta\"_\n\n"
        "*Cara 2 — Perintah Cepat:*\n"
        "• /tersangka [deskripsi] — pertanyaan BAP tersangka\n"
        "• /saksi [deskripsi] — pertanyaan BAP saksi\n"
        "• /korban [deskripsi] — pertanyaan BAP korban\n"
        "• /pelapor [deskripsi] — pertanyaan BAP pelapor\n"
        "• /ahli [bidang] — pertanyaan pemeriksaan ahli\n"
        "• /bukti [uraian] — analisis barang bukti\n"
        "• /review [uraian berkas] — review kelengkapan\n"
        "• /spdp [data perkara] — buat SPDP\n"
        "• /spsidik [data perkara] — buat SP.Sidik\n"
        "• /panggil [data saksi/tersangka] — surat panggilan\n\n"
        "*Tips:*\n"
        "Sertakan detail kasus (pasal, tersangka, korban, bukti) untuk hasil lebih akurat."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    user_id = update.effective_user.id
    conversation_history[user_id] = []
    await update.message.reply_text("🔄 Riwayat percakapan telah dihapus. Siap untuk kasus baru.")

async def cmd_tersangka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    args = " ".join(context.args) if context.args else ""
    if not args:
        await update.message.reply_text(
            "ℹ️ Gunakan: /tersangka [deskripsi kasus]\n"
            "Contoh: /tersangka Kasus penipuan Pasal 378, tersangka Budi, korban 3 orang"
        )
        return
    await update.message.reply_text("⏳ Menyusun pertanyaan pemeriksaan tersangka...")
    response = await ask_ai(
        update.effective_user.id,
        f"Buatkan daftar pertanyaan pemeriksaan TERSANGKA yang komprehensif untuk kasus berikut:\n{args}"
    )
    await send_long_message(update, response)

async def cmd_saksi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    args = " ".join(context.args) if context.args else ""
    if not args:
        await update.message.reply_text("ℹ️ Gunakan: /saksi [deskripsi kasus dan identitas saksi]")
        return
    await update.message.reply_text("⏳ Menyusun pertanyaan pemeriksaan saksi...")
    response = await ask_ai(
        update.effective_user.id,
        f"Buatkan daftar pertanyaan pemeriksaan SAKSI untuk kasus berikut:\n{args}"
    )
    await send_long_message(update, response)

async def cmd_bukti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    args = " ".join(context.args) if context.args else ""
    if not args:
        await update.message.reply_text("ℹ️ Gunakan: /bukti [uraian barang bukti yang ada]")
        return
    await update.message.reply_text("⏳ Menganalisis barang bukti...")
    response = await ask_ai(
        update.effective_user.id,
        f"Lakukan analisis kecukupan barang bukti dan rekomendasi langkah penyidikan lanjutan:\n{args}"
    )
    await send_long_message(update, response)

async def cmd_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    args = " ".join(context.args) if context.args else ""
    if not args:
        await update.message.reply_text("ℹ️ Gunakan: /review [uraian dokumen yang ada dalam berkas]")
        return
    await update.message.reply_text("⏳ Mereview kelengkapan berkas perkara...")
    response = await ask_ai(
        update.effective_user.id,
        f"Review kelengkapan dan kualitas berkas penyidikan berikut:\n{args}"
    )
    await send_long_message(update, response)

async def cmd_surat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    args = " ".join(context.args) if context.args else ""
    if not args:
        await update.message.reply_text(
            "ℹ️ Gunakan: /surat [jenis surat] [data perkara]\n"
            "Contoh: /surat SPDP perkara narkotika LP/B/012/IV/2026"
        )
        return
    await update.message.reply_text("⏳ Membuat dokumen administrasi...")
    response = await ask_ai(
        update.effective_user.id,
        f"Buatkan dokumen administrasi penyidikan berikut dengan format PERKABA 2022 "
        f"dan kopstuk Ditreskrimum Polda Sulawesi:\n{args}"
    )
    await send_long_message(update, response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("⛔ Akses tidak diizinkan.")
        return

    user_message = update.message.text
    await update.message.reply_text("⏳ Memproses...")

    response = await ask_ai(update.effective_user.id, user_message)
    await send_long_message(update, response)

async def send_long_message(update: Update, text: str):
    """Kirim pesan panjang dengan memotong per 4000 karakter (batas Telegram)."""
    max_len = 4000
    if len(text) <= max_len:
        await update.message.reply_text(text)
        return

    parts = []
    while text:
        if len(text) <= max_len:
            parts.append(text)
            break
        # Potong di newline terdekat sebelum batas
        cut = text.rfind("\n", 0, max_len)
        if cut == -1:
            cut = max_len
        parts.append(text[:cut])
        text = text[cut:].lstrip("\n")

    for i, part in enumerate(parts, 1):
        header = f"📄 *Bagian {i}/{len(parts)}*\n\n" if len(parts) > 1 else ""
        await update.message.reply_text(header + part, parse_mode="Markdown")

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY tidak ditemukan di .env")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bantuan", bantuan))
    app.add_handler(CommandHandler("help", bantuan))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("tersangka", cmd_tersangka))
    app.add_handler(CommandHandler("saksi", cmd_saksi))
    app.add_handler(CommandHandler("bukti", cmd_bukti))
    app.add_handler(CommandHandler("review", cmd_review))
    app.add_handler(CommandHandler("surat", cmd_surat))

    # Pesan biasa
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🚔 Bot Asisten Penyidik Polri aktif...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
