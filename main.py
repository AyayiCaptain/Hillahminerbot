from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# Dein Telegram Bot Token
TOKEN = "7618526256:AAHBUG16X1DTaFgUBUPsEjJXlR_Mjy7UjRI"

# Trading Tipps
TIPS = [
    "Tipp: Nutze immer Stop-Loss, um Verluste zu begrenzen.",
    "Tipp: Diversifiziere dein Portfolio für mehr Sicherheit.",
    "Tipp: Gewinne regelmäßig sichern, nicht alles reinvestieren.",
    "Tipp: Lass dich nicht von Angst oder Gier leiten.",
]

# Coins, die gemined werden können
COINS = ["USDT", "Sahara", "HillahCoin"]

# VIP-Level mit Bonusfaktor (Multiplikator)
VIP_TIERS = {
    50: ("Bronze VIP", 1.10),
    75: ("Silber VIP", 1.25),
    150: ("Gold VIP", 1.50)
}

# Speichern von Nutzer-Status in-memory (verlieren sich nach Bot-Neustart)
user_vip_status = {}
user_balance = {}

# /start Befehl
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Willkommen beim Hillah Miner Bot!\n\n"
        "Folgende Befehle:\n"
        "/tip – Trading Tipp bekommen\n"
        "/mine – Kryptowährung minen\n"
        "/vip – VIP Status anzeigen\n"
        "/setvip <Betrag> – VIP Status aktivieren (50, 75, 150)\n"
        "/balance – Kontostand anzeigen\n"
        "/withdraw – Auszahlung ab 250 € beantragen\n\n"
        "Folge @AyayiCaptain auf Instagram!"
    )

# /tip Befehl
async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 " + random.choice(TIPS))

# /mine Befehl – minen mit VIP Bonus
async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    coin = random.choice(COINS)
    base_earn = round(random.uniform(1, 10), 2)
    boost = 1.0
    if user_id in user_vip_status:
        boost = user_vip_status[user_id][1]
    earned = round(base_earn * boost, 2)
    user_balance[user_id] = user_balance.get(user_id, 0) + earned
    await update.message.reply_text(f"⛏ Du hast {earned} € in {coin} gemined!")

# /vip Befehl – zeigt VIP Optionen
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 VIP Status aktivieren:\n"
        "50 € – Bronze VIP (+10% Mining Bonus)\n"
        "75 € – Silber VIP (+25% Mining Bonus)\n"
        "150 € – Gold VIP (+50% Mining Bonus)\n\n"
        "Beispiel: /setvip 75"
    )
    await update.message.reply_text(text)

# /setvip <Betrag> Befehl – VIP Status setzen
async def setvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Bitte gib einen Betrag an. Beispiel: /setvip 75")
        return
    try:
        amount = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Ungültiger Betrag.")
        return
    if amount not in VIP_TIERS:
        await update.message.reply_text("Ungültiger Betrag. Erlaubt: 50, 75, 150")
        return
    status, boost = VIP_TIERS[amount]
    user_vip_status[user_id] = (status, boost)
    await update.message.reply_text(f"✅ VIP Status aktiviert: {status} mit x{boost} Mining Bonus")

# /balance Befehl – Kontostand anzeigen
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = user_balance.get(user_id, 0)
    await update.message.reply_text(f"💰 Dein Kontostand: {bal} €")

# /withdraw Befehl – Auszahlung ab 250€
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = user_balance.get(user_id, 0)
    if bal < 250:
        await update.message.reply_text(f"❌ Du brauchst mindestens 250 € für Auszahlung. Aktuell: {bal} €")
        return
    # Auszahlung simuliert (hier könnte API-Aufruf kommen)
    await update.message.reply_text("✅ Auszahlung beantragt! Unser Team meldet sich bei dir.")
    user_balance[user_id] = 0

# Bot starten
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("mine", mine))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("setvip", setvip))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.run_polling()

if __name__ == "__main__":
    main()
