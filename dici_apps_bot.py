"""
Dici Apps Bot - Telegram Bot
================================
Bot Telegram untuk portofolio personal Dici Apps.

Fitur saat ini:
  /start   - Sambutan & menu utama
  /profile - Profil pemilik bot
  /proyek  - Daftar proyek yang telah selesai
  /help    - Bantuan perintah

Setup:
  1. Install dependency:
       pip install python-telegram-bot

  2. Dapatkan token bot dari @BotFather di Telegram

  3. Isi TOKEN di bawah ini:
       BOT_TOKEN = "isi_token_kamu_di_sini"

  4. Jalankan:
       python dici_apps_bot.py
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ──────────────────────────────────────────────
# KONFIGURASI — Token dibaca dari environment variable
# Set di Railway: Settings → Variables → BOT_TOKEN
# ──────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "isi_token_kamu_di_sini")

# ──────────────────────────────────────────────
# DATA PROFIL — Sesuaikan dengan data kamu
# ──────────────────────────────────────────────
PROFIL = {
    "nama": "Dzakir",
    "tagline": "Mobile & Web Developer | IoT Enthusiast",
    "lokasi": "Padalarang, Jawa Barat 🇮🇩",
    "keahlian": ["Flutter", "React Native", "Node.js", "Firebase", "IoT"],
    "github": "https://github.com/username_kamu",
    "email": "email@kamu.com",
}

# ──────────────────────────────────────────────
# DATA PROYEK — Isi dengan proyek kamu
# ──────────────────────────────────────────────
PROYEK_LIST = [
    {
        "nama": "Smart Community Control Center",
        "deskripsi": "Aplikasi manajemen komunitas residensial pintar dengan dashboard admin web & mobile app untuk penghuni.",
        "teknologi": "Flutter • Node.js • Firebase • IoT",
        "status": "✅ Done",
        "tahun": "2024",
    },
    # Tambahkan proyek lainnya di sini:
    # {
    #     "nama": "Nama Proyek",
    #     "deskripsi": "Deskripsi singkat proyek.",
    #     "teknologi": "Teknologi yang dipakai",
    #     "status": "✅ Done",
    #     "tahun": "2024",
    # },
]

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# HELPER — Keyboard menu utama
# ──────────────────────────────────────────────
def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Profil", callback_data="profil"),
            InlineKeyboardButton("🗂 Proyek", callback_data="proyek"),
        ],
        [
            InlineKeyboardButton("📬 Kontak", callback_data="kontak"),
        ],
    ])


# ──────────────────────────────────────────────
# HANDLER — /start
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    teks = (
        f"Halo, {user.first_name}! 👋\n\n"
        f"Selamat datang di *Dici Apps Bot* 🤖\n"
        f"Bot portofolio personal milik *{PROFIL['nama']}*.\n\n"
        f"Silakan pilih menu di bawah ini 👇"
    )
    await update.message.reply_text(
        teks,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# ──────────────────────────────────────────────
# HANDLER — /profile
# ──────────────────────────────────────────────
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keahlian_str = " • ".join(PROFIL["keahlian"])
    teks = (
        f"👤 *Profil Saya*\n"
        f"{'─' * 28}\n"
        f"*Nama*    : {PROFIL['nama']}\n"
        f"*Tagline* : {PROFIL['tagline']}\n"
        f"*Lokasi*  : {PROFIL['lokasi']}\n\n"
        f"🛠 *Keahlian*\n"
        f"{keahlian_str}\n\n"
        f"🔗 *Link*\n"
        f"GitHub : {PROFIL['github']}\n"
        f"Email  : {PROFIL['email']}"
    )
    await update.message.reply_text(teks, parse_mode="Markdown")


# ──────────────────────────────────────────────
# HANDLER — /proyek
# ──────────────────────────────────────────────
async def proyek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not PROYEK_LIST:
        await update.message.reply_text("Belum ada proyek yang ditambahkan.")
        return

    teks = f"🗂 *Proyek yang Telah Selesai* ({len(PROYEK_LIST)} proyek)\n{'─' * 28}\n\n"
    for i, p in enumerate(PROYEK_LIST, 1):
        teks += (
            f"*{i}. {p['nama']}*  {p['status']}\n"
            f"📅 {p['tahun']}\n"
            f"{p['deskripsi']}\n"
            f"⚙️ _{p['teknologi']}_\n\n"
        )

    await update.message.reply_text(teks, parse_mode="Markdown")


# ──────────────────────────────────────────────
# HANDLER — /help
# ──────────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = (
        "📌 *Daftar Perintah*\n"
        "{'─' * 28}\n"
        "/start   — Menu utama\n"
        "/profile — Lihat profil saya\n"
        "/proyek  — Lihat daftar proyek\n"
        "/help    — Bantuan\n"
    )
    await update.message.reply_text(teks, parse_mode="Markdown")


# ──────────────────────────────────────────────
# HANDLER — Inline keyboard callback
# ──────────────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "profil":
        keahlian_str = " • ".join(PROFIL["keahlian"])
        teks = (
            f"👤 *Profil Saya*\n"
            f"{'─' * 28}\n"
            f"*Nama*    : {PROFIL['nama']}\n"
            f"*Tagline* : {PROFIL['tagline']}\n"
            f"*Lokasi*  : {PROFIL['lokasi']}\n\n"
            f"🛠 *Keahlian*\n"
            f"{keahlian_str}\n\n"
            f"🔗 *Link*\n"
            f"GitHub : {PROFIL['github']}\n"
            f"Email  : {PROFIL['email']}"
        )
        await query.edit_message_text(teks, parse_mode="Markdown", reply_markup=main_keyboard())

    elif query.data == "proyek":
        if not PROYEK_LIST:
            teks = "Belum ada proyek yang ditambahkan."
        else:
            teks = f"🗂 *Proyek yang Telah Selesai* ({len(PROYEK_LIST)} proyek)\n{'─' * 28}\n\n"
            for i, p in enumerate(PROYEK_LIST, 1):
                teks += (
                    f"*{i}. {p['nama']}*  {p['status']}\n"
                    f"📅 {p['tahun']}\n"
                    f"{p['deskripsi']}\n"
                    f"⚙️ _{p['teknologi']}_\n\n"
                )
        await query.edit_message_text(teks, parse_mode="Markdown", reply_markup=main_keyboard())

    elif query.data == "kontak":
        teks = (
            f"📬 *Kontak*\n"
            f"{'─' * 28}\n"
            f"Email  : {PROFIL['email']}\n"
            f"GitHub : {PROFIL['github']}"
        )
        await query.edit_message_text(teks, parse_mode="Markdown", reply_markup=main_keyboard())


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("proyek", proyek))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Dici Apps Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()