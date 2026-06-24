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
from dotenv import load_dotenv
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
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ──────────────────────────────────────────────
# DATA PROFIL — Sesuaikan dengan data kamu
# ──────────────────────────────────────────────
PROFIL = {
    "nama": "Dici",
    "tagline": "Programmer",
    "keahlian": ["Flutter", "React Native", "Node.js", "Firebase", "IoT", "Linux" , "Git", "Docker"],
    "github": "soon will be updated",
    "email": "soon will be updated",
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
            InlineKeyboardButton("👤 Profil", callback_data="profil", api_kwargs={'style': 'danger'}),
            InlineKeyboardButton("⚙️ Get List Tools!", callback_data="tools", api_kwargs={'style': 'success'}),
        ],
        [
            InlineKeyboardButton("📬 Kontak", callback_data="kontak", api_kwargs={'style': 'primary'}),
        ],
    ])


# ──────────────────────────────────────────────
# HANDLER — /start
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    teks = (
        f"Hello, {user.first_name}! 👋\n\n"
        f"Welcome to <b>Dici Apps Bot</b> 🤖\n"
        f"Bot portofolio personal milik <b>{PROFIL['nama']}</b>.\n\n"
        f"Please choose a menu below 👇"
    )
    await update.message.reply_text(
        teks,
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ──────────────────────────────────────────────
# HANDLER — /profile
# ──────────────────────────────────────────────
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keahlian_str = " • ".join(PROFIL["keahlian"])
    teks = (
        f"👤 <b>Profil Saya</b>\n"
        f"{'─' * 28}\n"
        f"<b>Nama</b>    : {PROFIL['nama']}\n"
        f"<b>Tagline</b> : {PROFIL['tagline']}\n\n"
        f"🛠 <b>Keahlian</b>\n"
        f"{keahlian_str}\n\n"
        f"🔗 <b>Link</b>\n"
        f"GitHub : {PROFIL['github']}\n"
        f"Email  : {PROFIL['email']}"
    )
    await update.message.reply_text(teks, parse_mode="HTML")


# ──────────────────────────────────────────────
# HANDLER — /proyek
# ──────────────────────────────────────────────
async def proyek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not PROYEK_LIST:
        await update.message.reply_text("Belum ada proyek yang ditambahkan.")
        return

    teks = f"🗂 <b>Proyek yang Telah Selesai</b> ({len(PROYEK_LIST)} proyek)\n{'─' * 28}\n\n"
    for i, p in enumerate(PROYEK_LIST, 1):
        teks += (
            f"<b>{i}. {p['nama']}</b>  {p['status']}\n"
            f"📅 {p['tahun']}\n"
            f"{p['deskripsi']}\n"
            f"⚙️ <i>{p['teknologi']}</i>\n\n"
        )

    await update.message.reply_text(teks, parse_mode="HTML")


# ──────────────────────────────────────────────
# HANDLER — /post_channel
# ──────────────────────────────────────────────
async def post_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan format: /post_channel @username_channel")
        return
    
    channel_id = context.args[0]
    teks = (
        f"👋 Halo! Saya <b>{PROFIL['nama']}</b>.\n"
        f"<i>{PROFIL['tagline']}</i>\n\n"
        f"Pilih menu di bawah ini untuk melihat detail lebih lanjut:"
    )
    
    try:
        await context.bot.send_message(
            chat_id=channel_id,
            text=teks,
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )
        await update.message.reply_text(f"Berhasil memposting profil ke {channel_id}!")
    except Exception as e:
        await update.message.reply_text(f"Gagal mengirim. Pastikan bot sudah menjadi Admin di {channel_id} dan memiliki hak untuk mengirim pesan.\nError: {e}")


# ──────────────────────────────────────────────
# HANDLER — /help
# ──────────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = (
        "📌 <b>Daftar Perintah</b>\n"
        f"{'─' * 28}\n"
        "/start   — Menu utama\n"
        "/profile — Lihat profil saya\n"
        "/proyek  — Lihat daftar proyek\n"
        "/help    — Bantuan\n"
    )
    await update.message.reply_text(teks, parse_mode="HTML")


# ──────────────────────────────────────────────
# HANDLER — Inline keyboard callback
# ──────────────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "profil":
        keahlian_str = " • ".join(PROFIL["keahlian"])
        teks = (
            f"👤 <b>Profil Saya</b>\n"
            f"{'─' * 28}\n"
            f"<b>Nama</b>    : {PROFIL['nama']}\n"
            f"<b>Tagline</b> : {PROFIL['tagline']}\n\n"
            f"🛠 <b>Keahlian</b>\n"
            f"{keahlian_str}\n\n"
            f"🔗 <b>Link</b>\n"
            f"GitHub : {PROFIL['github']}\n"
            f"Email  : {PROFIL['email']}"
        )
        await query.edit_message_text(teks, parse_mode="HTML", reply_markup=main_keyboard())

    elif query.data == "tools":
        teks = "🛠 <b>List Tools</b>\nBelum ada tools yang tersedia saat ini."
        await query.edit_message_text(teks, parse_mode="HTML", reply_markup=main_keyboard())

    elif query.data == "kontak":
        teks = (
            f"📬 <b>Kontak</b>\n"
            f"{'─' * 28}\n"
            f"Email  : {PROFIL['email']}\n"
            f"GitHub : {PROFIL['github']}"
        )
        await query.edit_message_text(teks, parse_mode="HTML", reply_markup=main_keyboard())


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("post_channel", post_channel))
    app.add_handler(CommandHandler("proyek", proyek))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Dici Apps Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
