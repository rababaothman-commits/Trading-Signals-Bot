"""
====================================================================
  TradingView → Telegram Signal Bot
  بوت تلغرام لاستقبال إشارات TradingView وإرسالها للقناة
====================================================================
  النشر على:  GitHub + Railway
  المتطلبات:  flask  |  requests  |  gunicorn
====================================================================
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import requests

# ─────────────────────────────────────────────
#  إعداد نظام تسجيل الأحداث (Logging)
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  قراءة المتغيرات السرية من البيئة
#  يتم ضبطها في Railway → Variables
# ─────────────────────────────────────────────
TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "")
WEBHOOK_SECRET_KEY  = os.environ.get("WEBHOOK_SECRET_KEY", "")

# التحقق من وجود المتغيرات الأساسية عند بدء التشغيل
if not TELEGRAM_BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN غير مضبوط في Variables!")
if not TELEGRAM_CHANNEL_ID:
    logger.error("❌ TELEGRAM_CHANNEL_ID غير مضبوط في Variables!")
else:
    logger.info("✅ المتغيرات السرية تم تحميلها بنجاح.")

# ─────────────────────────────────────────────
#  إنشاء تطبيق Flask
# ─────────────────────────────────────────────
app = Flask(__name__)


# ─────────────────────────────────────────────
#  دالة إرسال الرسالة إلى تلغرام
# ─────────────────────────────────────────────
def send_telegram_message(message_text: str) -> bool:
    """
    ترسل رسالة نصية إلى قناة التلغرام عبر Telegram Bot API.
    القيمة المُعادة: True إذا نجح، False إذا فشل.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        logger.error("لا يمكن الإرسال: التوكن أو معرّف القناة غير مضبوط.")
        return False

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id":    TELEGRAM_CHANNEL_ID,
        "text":       message_text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()

        if response.json().get("ok"):
            logger.info("✅ تم إرسال الرسالة إلى تلغرام بنجاح.")
            return True
        else:
            logger.error(f"❌ فشل الإرسال: {response.json()}")
            return False

    except requests.exceptions.Timeout:
        logger.error("❌ انتهت مهلة الاتصال بـ Telegram API.")
    except requests.exceptions.ConnectionError:
        logger.error("❌ خطأ في الاتصال بـ Telegram API.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ خطأ HTTP: {e}")
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")

    return False


# ─────────────────────────────────────────────
#  دالة بناء نص الرسالة المنسّقة
# ─────────────────────────────────────────────
def build_signal_message(data: dict) -> str:
    """
    تبني نص الرسالة المنسّقة بناءً على JSON القادم من TradingView.
    """
    symbol    = data.get("symbol",    "غير محدد").upper()
    action    = data.get("action",    "غير محدد").upper()
    timeframe = data.get("timeframe", "غير محدد")
    entry     = data.get("entry",     "غير محدد")
    stop_loss = data.get("stop_loss", "غير محدد")
    tp1       = data.get("tp1",       "غير محدد")
    tp2       = data.get("tp2",       "غير محدد")

    if action == "BUY":
        direction_emoji = "🟢"
        direction_text  = "شراء  (BUY)"
    elif action == "SELL":
        direction_emoji = "🔴"
        direction_text  = "بيع  (SELL)"
    else:
        direction_emoji = "⚪"
        direction_text  = action

    current_time = datetime.utcnow().strftime("%Y-%m-%d  %H:%M  UTC")

    message = (
        f"🚨 <b>إشارة تداول جديدة</b> 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>الأداة المالية :</b>  <code>{symbol}</code>\n"
        f"📊 <b>الاتجاه        :</b>  {direction_text}  {direction_emoji}\n"
        f"⏱  <b>الفريم الزمني  :</b>  {timeframe}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>سعر الدخول    :</b>  <code>{entry}</code>\n"
        f"❌ <b>وقف الخسارة   :</b>  <code>{stop_loss}</code>\n"
        f"🎯 <b>الهدف الأول   :</b>  <code>{tp1}</code>\n"
        f"🎯 <b>الهدف الثاني  :</b>  <code>{tp2}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🕐 <i>{current_time}</i>\n"
        f"⚡️ <i>مُولَّدة تلقائياً عبر TradingView</i>"
    )

    return message


# ─────────────────────────────────────────────
#  Webhook — استقبال الإشارات من TradingView
# ─────────────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def receive_webhook():
    """
    يستقبل POST من TradingView ويرسل الإشارة إلى تلغرام.
    URL في TradingView:
        https://<railway-domain>/webhook?secret=YOUR_SECRET
    """

    # ── التحقق من المفتاح السري ──────────────────────────────────────
    if WEBHOOK_SECRET_KEY:
        incoming = request.args.get("secret", "")
        if incoming != WEBHOOK_SECRET_KEY:
            logger.warning("⚠️ وصول مرفوض: مفتاح سري خاطئ.")
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # ── استخراج JSON ─────────────────────────────────────────────────
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            raise ValueError("JSON فارغ أو غير صالح")
    except Exception as e:
        logger.error(f"❌ فشل تحليل JSON: {e}")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    logger.info(f"📥 إشارة واردة: {json.dumps(data, ensure_ascii=False)}")

    # ── التحقق من الحقول الأساسية ────────────────────────────────────
    required = ["symbol", "action", "entry"]
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({"status": "error", "message": f"Missing: {missing}"}), 400

    # ── الإرسال ──────────────────────────────────────────────────────
    msg     = build_signal_message(data)
    success = send_telegram_message(msg)

    if success:
        return jsonify({"status": "ok", "message": "Signal sent!"}), 200
    return jsonify({"status": "error", "message": "Telegram send failed"}), 500


# ─────────────────────────────────────────────
#  Health Check — للتحقق من أن السيرفر يعمل
# ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status":           "running 🚀",
        "bot_token_set":    bool(TELEGRAM_BOT_TOKEN),
        "channel_id_set":   bool(TELEGRAM_CHANNEL_ID),
        "secret_key_set":   bool(WEBHOOK_SECRET_KEY),
        "webhook_endpoint": "POST /webhook",
    }), 200


# ─────────────────────────────────────────────
#  Test — إرسال إشارة تجريبية
# ─────────────────────────────────────────────
@app.route("/test", methods=["GET"])
def test_signal():
    """
    افتح https://<domain>/test لإرسال إشارة تجريبية إلى قناتك.
    """
    test_data = {
        "symbol":    "BTCUSDT",
        "action":    "BUY",
        "timeframe": "1H",
        "entry":     "67,500.00",
        "stop_loss": "65,800.00",
        "tp1":       "69,000.00",
        "tp2":       "71,500.00",
    }
    success = send_telegram_message(build_signal_message(test_data))

    if success:
        return jsonify({"status": "ok", "message": "✅ Test signal sent!"}), 200
    return jsonify({"status": "error", "message": "❌ Failed. Check Railway logs."}), 500


# ─────────────────────────────────────────────
#  تشغيل التطبيق
#  Railway يضبط PORT تلقائياً — لا تغيّره
# ─────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 البوت يعمل على المنفذ {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
