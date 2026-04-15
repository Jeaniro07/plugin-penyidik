"""
Bot WhatsApp — Asisten Penyidik Polri
Ditreskrimum Polda Sulawesi

Menggunakan Twilio WhatsApp API + Flask + OpenAI

Persyaratan:
  pip install flask twilio openai python-dotenv

Cara menjalankan:
  1. Salin .env.example ke .env dan isi konfigurasi
  2. python whatsapp_bot.py
  3. Expose ke internet dengan: ngrok http 5000
  4. Daftarkan URL webhook di Twilio Console

Panduan Twilio WhatsApp Sandbox:
  https://www.twilio.com/docs/whatsapp/sandbox
"""

import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import openai

load_dotenv()

# ─── Konfigurasi ─────────────────────────────────────────────────────────────

TWILIO_ACCOUNT_SID  = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WA_NUMBER    = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY")
# Whitelist nomor WhatsApp (format: whatsapp:+62812xxxxx)
ALLOWED_NUMBERS     = set(
    x.strip() for x in os.getenv("ALLOWED_WA_NUMBERS", "").split(",") if x.strip()
)

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── System Prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
Kamu adalah Asisten Penyidik Polri untuk Ditreskrimum Polda Sulawesi.

KETENTUAN HUKUM: KUHP Baru (UU 1/2023 jo. 1/2026) · KUHAP Baru (UU 20/2025) · PERKABA 2022
- Pasal 90: penetapan tersangka min. 2 alat bukti
- Pasal 142: hak tersangka
- Pasal 235: 7+ alat bukti sah (petunjuk dihapus, bukti elektronik masuk)

KEMAMPUAN: pertanyaan BAP (tersangka/saksi/korban/pelapor/ahli), analisis bukti,
review berkas, dokumen administrasi (SP.Sidik, SPDP, surat panggilan, dll.).

FORMAT: Bahasa Indonesia formal. Ringkas namun lengkap untuk WhatsApp.
Gunakan emoji sparingly. Pisahkan bagian dengan baris kosong.
Jika output sangat panjang, beri tanda *LANJUT* di akhir dan tunggu perintah "lanjut".
"""

# ─── Riwayat Percakapan ───────────────────────────────────────────────────────

conversation_history: dict[str, list[dict]] = {}
pending_continuation: dict[str, list[str]] = {}

def get_history(phone: str) -> list[dict]:
    if phone not in conversation_history:
        conversation_history[phone] = []
    return conversation_history[phone]

def add_to_history(phone: str, role: str, content: str):
    history = get_history(phone)
    history.append({"role": role, "content": content})
    if len(history) > 20:
        conversation_history[phone] = history[-20:]

# ─── AI ───────────────────────────────────────────────────────────────────────

def ask_ai(phone: str, user_message: str) -> str:
    add_to_history(phone, "user", user_message)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(phone)

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=3000,
            temperature=0.3,
        )
        reply = response.choices[0].message.content
        add_to_history(phone, "assistant", reply)
        return reply
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return f"❌ Error AI: {str(e)}"

# ─── Kirim Pesan Panjang ──────────────────────────────────────────────────────

def send_long_whatsapp(to: str, text: str):
    """Kirim pesan panjang dalam beberapa bagian via Twilio."""
    max_len = 1500  # WhatsApp lebih baik dengan pesan lebih pendek
    parts = []
    while text:
        if len(text) <= max_len:
            parts.append(text)
            break
        cut = text.rfind("\n", 0, max_len)
        if cut == -1:
            cut = max_len
        parts.append(text[:cut])
        text = text[cut:].lstrip()

    for i, part in enumerate(parts):
        suffix = f"\n\n_(Bagian {i+1}/{len(parts)})_" if len(parts) > 1 else ""
        twilio_client.messages.create(
            from_=TWILIO_WA_NUMBER,
            to=to,
            body=part + suffix
        )

# ─── Webhook ──────────────────────────────────────────────────────────────────

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    from_number  = request.values.get("From", "")

    logger.info(f"Pesan dari {from_number}: {incoming_msg[:50]}")

    # Cek otorisasi
    if ALLOWED_NUMBERS and from_number not in ALLOWED_NUMBERS:
        resp = MessagingResponse()
        resp.message("⛔ Nomor Anda tidak terdaftar. Hubungi admin.")
        return str(resp)

    resp = MessagingResponse()

    # Perintah khusus
    lower = incoming_msg.lower()

    if lower in ["halo", "hi", "mulai", "start", "/start"]:
        reply = (
            "🚔 *Asisten Penyidik Polri — Ditreskrimum Sulawesi*\n\n"
            "Siap membantu tugas penyidikan Anda.\n\n"
            "Ketik langsung kebutuhan Anda atau gunakan perintah:\n"
            "• *tersangka* [kasus] — pertanyaan BAP\n"
            "• *saksi* [kasus] — pertanyaan saksi\n"
            "• *bukti* [uraian] — analisis bukti\n"
            "• *review* [berkas] — cek kelengkapan\n"
            "• *surat* [jenis] — buat dokumen\n"
            "• *reset* — hapus riwayat\n\n"
            "_Dasar: KUHP Baru · KUHAP Baru · PERKABA 2022_"
        )
        resp.message(reply)
        return str(resp)

    if lower == "reset":
        conversation_history[from_number] = []
        resp.message("🔄 Riwayat dihapus. Siap untuk kasus baru.")
        return str(resp)

    # Perintah dengan prefiks
    prefix_map = {
        "tersangka ": "Buatkan pertanyaan pemeriksaan TERSANGKA untuk kasus: ",
        "saksi ":     "Buatkan pertanyaan pemeriksaan SAKSI untuk kasus: ",
        "korban ":    "Buatkan pertanyaan pemeriksaan KORBAN untuk kasus: ",
        "pelapor ":   "Buatkan pertanyaan pemeriksaan PELAPOR untuk kasus: ",
        "ahli ":      "Buatkan pertanyaan pemeriksaan AHLI bidang ",
        "bukti ":     "Analisis kecukupan barang bukti berikut: ",
        "review ":    "Review kelengkapan berkas penyidikan: ",
        "surat ":     "Buatkan dokumen administrasi penyidikan (kopstuk Ditreskrimum Sulawesi): ",
    }

    final_message = incoming_msg
    for prefix, replacement in prefix_map.items():
        if lower.startswith(prefix):
            final_message = replacement + incoming_msg[len(prefix):]
            break

    # Proses dengan AI (async-like via Twilio)
    reply = ask_ai(from_number, final_message)

    # Jika reply panjang, kirim via Twilio langsung (bukan TwiML response)
    if len(reply) > 1500:
        send_long_whatsapp(from_number, reply)
        return ("", 204)  # No Content — sudah dikirim langsung
    else:
        resp.message(reply)
        return str(resp)

# ─── Health Check ─────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return "🚔 Bot Asisten Penyidik Polri aktif.", 200

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info("🚔 Memulai WhatsApp Bot Asisten Penyidik Polri...")
    logger.info("Untuk expose ke internet: ngrok http 5000")
    logger.info("Webhook URL: https://[ngrok-url]/whatsapp")
    app.run(host="0.0.0.0", port=5000, debug=False)
