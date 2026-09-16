---
id: DOM-03
title: معماری DNS و SSL
status: approved
phase: 1
approved: 1405-06-25
---
<div dir="rtl" align="right">

# معماری DNS، گواهی SSL و سیاست دامنهٔ رسمی

> نام‌های زیر با فرض دامنهٔ اصلی `sos-delijan.ir` نوشته شده‌اند (تصمیم D-001). اگر دامنه عوض شد، جایگزین شود.

---

## ۱. رکوردهای DNS

### ۱.۱ رکوردهای اجباری

| نوع | نام | مقدار | TTL | کاربرد |
|---|---|---|---|---|
| `A` | `@` | `<IP هاست>` | ۳۶۰۰ | صفحهٔ اصلی روی هاست |
| `CNAME` | `www` | `sos-delijan.ir` | ۳۶۰۰ | یکسان‌سازی → بعداً ۳۰۱ |
| `AAAA` | `@` | `<IPv6 هاست>` | ۳۶۰۰ | فقط اگر هاست IPv6 دارد |

> 💡 اگر از CDN استفاده می‌کنید، رکورد `A`/`CNAME` به سمت CDN می‌رود و CDN با Origin هاست صحبت می‌کند.

### ۱.۲ رکوردهای ایمیل — ⛔ لازم نیستند (Q-20 = خیر / D-018)

کارفرما ایمیل سازمانی روی دامنه **نمی‌خواهد** و هیچ ایمیلی در سایت نمایش داده نمی‌شود. در نتیجه:

| رکورد | وضعیت |
|---|---|
| `MX` / `A mail` | ⛔ ساخته نمی‌شود |
| `TXT` SPF | ⛔ ساخته نمی‌شود |
| `TXT` DKIM / DMARC | ⛔ ساخته نمی‌شود |

> ✅ **تنها اقدام امنیتی لازم در نبود ایمیل:** در پنل هاست، قابلیت ارسال ایمیل وردپرس غیرفعال یا محدود شود تا از دامنه برای اسپم استفاده نشود:
> ```php
> // wp-config.php — جلوگیری از ارسال هر ایمیل از سمت سایت
> add_filter( 'pre_wp_mail', '__return_false' );
> ```
>
> 💡 اگر در آینده کارفرما ایمیل سازمانی خواست، این بخش بازنویسی می‌شود و MX/SPF/DKIM/DMARC **به‌طور کامل و یکجا** اضافه می‌گردند (SPF ناقص از نبودِ آن بدتر است).

### ۱.۳ رکوردهای تأیید و امنیتی

| نوع | نام | مقدار | کاربرد |
|---|---|---|---|
| `TXT` | `@` | `google-site-verification=...` | تأیید در Google Search Console |
| `TXT` | `@` | `BingSiteAuth=...` | تأیید در Bing Webmaster |
| `CAA` | `@` | `0 issue "letsencrypt.org"` | فقط Let's Encrypt بتواند گواهی صادر کند |
| `TXT` | `_acme-challenge` | (موقت) | فقط در زمان صدور گواهی |

### ۱.۴ رکوردهای محیط توسعه

| نوع | نام | مقدار | نکته |
|---|---|---|---|
| `A` | `staging` | `<IP هاست>` | **حتماً** با Basic Auth محافظت شود |

> 🚫 **هرگز** زیردامنهٔ `test` یا `dev` بدون محافظت و بدون `noindex` رها نکنید — محتوای تکراری ایندکس می‌شود.

---

## ۲. سیاست دامنهٔ رسمی و ریدایرکت‌ها

### ۲.۱ چهار حالت ورودی کاربر

| ورودی | خروجی | کد |
|---|---|---|
| `http://sos-delijan.ir/x` | `https://sos-delijan.ir/x` | ۳۰۱ |
| `https://www.sos-delijan.ir/x` | `https://sos-delijan.ir/x` | ۳۰۱ |
| `http://www.sos-delijan.ir/x` | `https://sos-delijan.ir/x` | ۳۰۱ |
| `https://emdadkhodrodelijan.ir/x` | `https://sos-delijan.ir/x` | ۳۰۱ |

### ۲.۲ پیاده‌سازی در `.htaccess` (Apache / LiteSpeed)

```apache
# --- Canonical: HTTPS + non-www ---
<IfModule mod_rewrite.c>
  RewriteEngine On

  # 1) HTTP -> HTTPS
  RewriteCond %{HTTPS} !=on
  RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

  # 2) www -> non-www
  RewriteCond %{HTTP_HOST} ^www\.sos-delijan\.ir$ [NC]
  RewriteRule ^(.*)$ https://sos-delijan.ir/$1 [R=301,L]
</IfModule>
```

برای دامنهٔ دوم (`emdadkhodrodelijan.ir`) روی همان هاست به‌عنوان **Alias/Parked Domain** تعریف شود و:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTP_HOST} ^(www\.)?emdadkhodrodelijan\.ir$ [NC]
  RewriteRule ^(.*)$ https://sos-delijan.ir/$1 [R=301,L]
</IfModule>
```

> ✅ **تست:** پس از اعمال، با `curl -I` باید `301` و `Location` درست برگردد. اگر وردپرس ریدایرکت را بازنویسی کرد، پلاگین **Redirection** نصب شود و ریدایرکت‌ها آنجا مدیریت شوند.

### ۲.۳ تنظیمات وردپرس
در `wp-config.php` یا پیشخوان → تنظیمات:
```php
define('WP_HOME', 'https://sos-delijan.ir');
define('WP_SITEURL', 'https://sos-delijan.ir');
```

---

## ۳. گواهی SSL

### ۳.۱ گزینه‌ها

| گزینه | هزینه | تجدید | توصیه |
|---|---|---|---|
| **Let's Encrypt** (رایگان) | ۰ | خودکار ۹۰ روزه | ✅ **پیشنهاد اصلی** — کاملاً کافی است |
| گواهی تجاری (DV) | ~۵۰۰ هزار تا ۲ میلیون تومان | سالانه | فقط اگر کارفرما اصرار دارد |
| SSL رایگان CDN (آروان‌کلاد) | ۰ | خودکار | اگر CDN استفاده می‌شود |

> 💡 برای یک سایت خدماتی محلی، **Let's Encrypt با تجدید خودکار** بهترین انتخاب است. گواهی پولی هیچ اثر رتبه‌ای اضافه‌ای ندارد.

### ۳.۲ چک‌لیست پیکربندی

- [ ] صدور گواهی برای **هر دو** هاست: `sos-delijan.ir` و `www.sos-delijan.ir` (SAN)
- [ ] فعال‌سازی **تجدید خودکار** (AutoSSL در cPanel یا cron در LiteSpeed)
- [ ] پروتکل‌ها: فقط **TLS 1.2 و TLS 1.3** (غیرفعال‌سازی SSLv3/TLS1.0/TLS1.1)
- [ ] رمزنگاری‌ها (Cipher Suites): مجموعهٔ مدرن، بدون RC4/3DES
- [ ] فعال‌سازی **HSTS** — ⚠ **فقط پس از ۳۰ روز پایداری کامل**:
  ```apache
  Header always set Strict-Transport-Security "max-age=15552000; includeSubDomains"
  ```
  > HSTS برگشت‌ناپذیر است؛ اگر قبل از پایدارشدن ریدایرکت‌ها فعال شود، کاربران را قفل می‌کند.
- [ ] حذف **محتوای ترکیبی (Mixed Content)**: همهٔ منابع با `https://` یا مسیر نسبی
- [ ] تست در `ssllabs.com/ssltest` → هدف: گرید **A** یا بالاتر

### ۳.۳ هدرهای امنیتی پیشنهادی

```apache
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(self), camera=(), microphone=()"
</IfModule>
```

> ⚠ `Content-Security-Policy` برای سایت المنتوری پیچیده است (inline style/JS زیاد). در فاز لانچ اضافه **نشود**؛ در فاز بهینه‌سازی و با گزارش‌گیری `Report-Only` بررسی شود.

---

## ۴. برنامهٔ TTL و مهاجرت DNS

### سناریوی مهاجرت از سایت قدیمی یا دامنهٔ موقت

| گام | اقدام | TTL |
|---|---|---|
| ۱ | ۴۸ ساعت پیش از سوییچ، TTL را به **۳۰۰** کاهش دهید | ۳۰۰ |
| ۲ | سایت را روی هاست جدید بالا بیاورید و با `Host` header تست کنید | ۳۰۰ |
| ۳ | رکوردها را سوییچ کنید | ۳۰۰ |
| ۴ | ۲۴ ساعت صبر کنید، خطاهای GSC و لاگ را پایش کنید | ۳۰۰ |
| ۵ | TTL را به **۳۶۰۰** برگردانید | ۳۶۰۰ |

### پایش انتشار DNS
پس از تغییر رکوردها، با ابزارهایی مانند `whatsmydns.net` انتشار در چند نقطه بررسی شود. در ایران به‌طور معمول ۱ تا ۲۴ ساعت طول می‌کشد.

---

## ۵. تست‌های پذیرش DNS

| # | تست | انتظار |
|---|---|---|
| ۱ | `curl -I http://sos-delijan.ir` | `301` → `https://sos-delijan.ir/` |
| ۲ | `curl -I https://www.sos-delijan.ir` | `301` → `https://sos-delijan.ir/` |
| ۳ | `curl -I https://emdadkhodrodelijan.ir/مناطق/نراق/` | `301` → `https://sos-delijan.ir/مناطق/نراق/` |
| ۴ | بازکردن `https://sos-delijan.ir` در مرورگر | بدون هشدار گواهی، نام صحیح |
| ۵ | تلاش برای ارسال ایمیل از سمت سایت | ⛔ **نباید** ایمیلی ارسال شود (`pre_wp_mail` غیرفعال است) |
| ۶ | SSL Labs | گرید A |

</div>
