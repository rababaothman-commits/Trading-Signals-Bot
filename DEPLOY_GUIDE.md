# 🚀 دليل النشر الكامل — GitHub + Railway

---

## 📁 هيكل المشروع النهائي

```
tradingview_bot/
├── main.py            ← الكود الرئيسي للبوت
├── requirements.txt   ← المكتبات (flask, requests, gunicorn)
├── Procfile           ← أمر التشغيل على Railway
├── railway.json       ← إعدادات Railway
├── .gitignore         ← الملفات المستثناة من GitHub
└── DEPLOY_GUIDE.md    ← هذا الملف
```

---

## ══════════════════════════════════════
## الجزء الأول — إعداد GitHub
## ══════════════════════════════════════

### الخطوة 1 — إنشاء حساب GitHub (إذا لم يكن لديك)
```
https://github.com/signup
```

---

### الخطوة 2 — إنشاء Repository جديد

1. بعد تسجيل الدخول اضغط على زر **"+"** في أعلى اليمين
2. اختر **"New repository"**
3. اضبط الإعدادات:
   - **Repository name:** `tradingview-telegram-bot`
   - **Visibility:** اختر **Private** ⬅️ مهم لحماية كودك
   - **لا تضع علامة** على "Add a README file"
4. اضغط **"Create repository"**

---

### الخطوة 3 — رفع الملفات على GitHub

**الطريقة الأولى (أسهل) — عبر واجهة الموقع:**

1. افتح الـ Repository الذي أنشأته
2. اضغط **"uploading an existing file"** أو **"Add file → Upload files"**
3. اسحب وأفلت الملفات الأربعة:
   - `main.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`
4. في الأسفل اكتب في Commit message: `Initial commit - TradingView Bot`
5. اضغط **"Commit changes"**

---

**الطريقة الثانية — عبر Terminal (للمتقدمين):**

```bash
# 1. افتح Terminal أو Command Prompt في مجلد المشروع
cd tradingview_bot

# 2. هيّئ Git
git init
git add .
git commit -m "Initial commit - TradingView Bot"

# 3. اربط بـ GitHub (استبدل YOUR_USERNAME باسم حسابك)
git remote add origin https://github.com/YOUR_USERNAME/tradingview-telegram-bot.git
git branch -M main
git push -u origin main
```

✅ **الآن كودك موجود على GitHub بأمان.**

---

## ══════════════════════════════════════
## الجزء الثاني — النشر على Railway
## ══════════════════════════════════════

### الخطوة 4 — إنشاء حساب Railway

1. افتح: `https://railway.app`
2. اضغط **"Login"**
3. اختر **"Login with GitHub"** ← سيطلب ربط حسابك بـ GitHub
4. وافق على الصلاحيات

> 💡 Railway يمنحك **$5 رصيد مجاني** كل شهر — كافٍ تماماً لتشغيل البوت.

---

### الخطوة 5 — إنشاء مشروع جديد على Railway

1. من Dashboard اضغط **"New Project"**
2. اختر **"Deploy from GitHub repo"**
3. إذا طلب منك تفويض GitHub اضغط **"Configure GitHub App"** ووافق
4. ابحث عن `tradingview-telegram-bot` واضغط عليه
5. اضغط **"Deploy Now"**

> سيبدأ Railway في بناء المشروع تلقائياً من ملف `requirements.txt` و `Procfile`

---

### الخطوة 6 — إضافة المتغيرات السرية في Railway ⬅️ الأهم

**هذه الخطوة أساسية — البوت لن يعمل بدونها!**

1. من داخل مشروعك على Railway اضغط على الـ **Service** (المربع)
2. اضغط تبويب **"Variables"**
3. اضغط **"New Variable"** وأضف المتغيرات الثلاثة:

| Variable Name          | Value (القيمة)                              |
|------------------------|---------------------------------------------|
| `TELEGRAM_BOT_TOKEN`   | التوكن من BotFather مثال: `1234567890:ABC...` |
| `TELEGRAM_CHANNEL_ID`  | مثال: `@mychannel` أو `-1001234567890`       |
| `WEBHOOK_SECRET_KEY`   | كلمة سر اخترها مثال: `tv_secret_2025`       |

4. بعد إضافة كل متغير اضغط **Enter** أو زر الحفظ ✓
5. Railway سيُعيد نشر التطبيق تلقائياً

---

### الخطوة 7 — الحصول على رابط البوت العام

1. في مشروعك على Railway اضغط تبويب **"Settings"**
2. انزل إلى قسم **"Networking"**
3. اضغط **"Generate Domain"**
4. ستحصل على رابط مثل:
   ```
   https://tradingview-bot-production-xxxx.up.railway.app
   ```
5. **احفظ هذا الرابط** — ستحتاجه في TradingView

---

### الخطوة 8 — التحقق من أن البوت يعمل

افتح هذا الرابط في المتصفح:
```
https://YOUR-RAILWAY-DOMAIN.up.railway.app/
```

يجب أن ترى هذا الرد:
```json
{
  "status": "running 🚀",
  "bot_token_set": true,
  "channel_id_set": true,
  "secret_key_set": true,
  "webhook_endpoint": "POST /webhook"
}
```

---

### الخطوة 9 — إرسال إشارة تجريبية

افتح هذا الرابط:
```
https://YOUR-RAILWAY-DOMAIN.up.railway.app/test
```

✅ **يجب أن تصلك رسالة في قناتك على تلغرام فوراً!**

---

## ══════════════════════════════════════
## الجزء الثالث — ربط TradingView
## ══════════════════════════════════════

### الخطوة 10 — إعداد Alert في TradingView

1. افتح `https://tradingview.com` وسجّل دخولك
2. افتح الرسم البياني لأي أداة مالية
3. اضغط على أيقونة الجرس 🔔 **"Alerts"** في الشريط الجانبي
4. اضغط **"+ Create Alert"**

---

### إعدادات Alert:

**في تبويب "Settings":**
- اضبط شرط التنبيه حسب استراتيجيتك

**في تبويب "Notifications":**
- ضع علامة ✓ على **"Webhook URL"**
- في حقل الـ URL أدخل:

```
https://YOUR-RAILWAY-DOMAIN.up.railway.app/webhook?secret=tv_secret_2025
```
> ⚠️ استبدل `tv_secret_2025` بالقيمة التي وضعتها في `WEBHOOK_SECRET_KEY`

---

**في حقل "Message" أدخل هذا JSON:**

```json
{
  "symbol": "{{ticker}}",
  "action": "BUY",
  "timeframe": "{{interval}}",
  "entry": "{{close}}",
  "stop_loss": "0",
  "tp1": "0",
  "tp2": "0"
}
```

> 💡 **للإشارات التلقائية من Pine Script:**
> استبدل `"BUY"` بـ `"{{strategy.order.action}}"` إذا كنت تستخدم strategy

---

### مثال JSON لإشارة بيع يدوية:

```json
{
  "symbol": "{{ticker}}",
  "action": "SELL",
  "timeframe": "{{interval}}",
  "entry": "{{close}}",
  "stop_loss": "{{plot_0}}",
  "tp1": "{{plot_1}}",
  "tp2": "{{plot_2}}"
}
```

---

## ══════════════════════════════════════
## الجزء الرابع — الصيانة والمراقبة
## ══════════════════════════════════════

### مشاهدة الـ Logs في Railway

1. افتح مشروعك على Railway
2. اضغط على الـ Service
3. اضغط تبويب **"Logs"**
4. ستجد سجلاً كاملاً لكل إشارة واردة

---

### التحديث التلقائي عند تعديل الكود

عند تعديل أي ملف ورفعه على GitHub:
- Railway سيكتشف التغيير **تلقائياً**
- سيُعيد البناء والنشر خلال دقيقة واحدة
- **صفر توقف** — Zero Downtime Deployment

---

## 🛡️ نصائح الأمان

| ✅ افعل | ❌ لا تفعل |
|---------|-----------|
| استخدم WEBHOOK_SECRET_KEY دائماً | لا تضع التوكن في main.py |
| اجعل Repository على GitHub خاصاً (Private) | لا تشارك رابط الـ Webhook علناً |
| راجع Logs دورياً | لا تنشر متغيرات .env على GitHub |

---

## 🔧 حل المشكلات الشائعة

| المشكلة | الحل |
|---------|------|
| البوت لا يرسل رسائل | تحقق من Variables في Railway — هل التوكن صحيح؟ |
| خطأ 401 في Logs | تحقق من WEBHOOK_SECRET_KEY في TradingView |
| خطأ 400 | تحقق من صيغة JSON في حقل Message بـ TradingView |
| Application failed to respond | انظر Logs في Railway — عادةً خطأ في Procfile |
| البوت لا يستقبل من القناة | تأكد أنك أضفت البوت كمشرف Admin في القناة |

---

## 📋 ملخص الروابط المهمة

| الرابط | الوصف |
|--------|-------|
| `https://YOUR-DOMAIN/` | التحقق من حالة البوت |
| `https://YOUR-DOMAIN/test` | إرسال إشارة تجريبية |
| `https://YOUR-DOMAIN/webhook?secret=KEY` | نقطة استقبال TradingView |
| `https://railway.app/dashboard` | لوحة تحكم Railway |
| `https://github.com/YOUR_USERNAME/tradingview-telegram-bot` | مستودع الكود |

---

*✨ بالتوفيق! البوت الآن يعمل 24/7 على Railway بدون توقف.*
