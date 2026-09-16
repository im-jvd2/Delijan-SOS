---
id: HOST-03
title: SOP آماده‌سازی سرور
status: approved
phase: 1
approved: 1405-06-25
---
<div dir="rtl" align="right">

# SOP — از خرید هاست تا آماده‌سازی کامل سرور

> **زمان تقریبی:** ۹۰ دقیقه
> **خروجی:** محیطی که وردپرس روی آن نصب می‌شود (فایل `../03-wordpress/01-install-baseline.md`)

---

## گام ۱ — دریافت اطلاعات و ورود (۱۰ دقیقه)

- [ ] دریافت ایمیل خوش‌آمدگویی: آدرس کنترل پنل، نام کاربری، رمز
- [ ] ورود به cPanel / DirectAdmin
- [ ] **تغییر فوری رمز عبور** کنترل پنل (رمز ≥ ۲۰ کاراکتر، ساخته‌شده با Password Manager)
- [ ] ذخیره در Vault:
  ```
  عنوان:  Delijan-SOS / cPanel
  کاربر:  …
  رمز:    …
  URL:     https://…:2083
  2FA:     فعال
  ```
- [ ] فعال‌سازی **2FA** روی کنترل پنل و ایمیل مرتبط

## گام ۲ — انتخاب نسخهٔ PHP (۵ دقیقه)

مسیر در cPanel: `Select PHP Version` یا `MultiPHP Manager`

- [ ] نسخه: **PHP 8.2** یا **8.3**
- [ ] اعمال مقادیر `01-hosting-requirements.md` بخش ۶:
  - `memory_limit = 512M`
  - `upload_max_filesize = 64M`
  - `post_max_size = 64M`
  - `max_execution_time = 300`
  - `max_input_vars = 3000` ← ⚠ حیاتی برای المنتور
  - `expose_php = Off`
- [ ] فعال‌سازی افزونه‌های PHP لازم:
  `mysqli`, `curl`, `gd`, `imagick` (یا `gd`), `mbstring`, `xml`, `zip`, `intl`, `openssl`, `fileinfo`, `exif`, `opcache`, `redis` (اگر موجود است)
- [ ] تأیید OPcache فعال است

## گام ۳ — ساخت پایگاه داده (۱۰ دقیقه)

- [ ] `MySQL Databases` → ساخت دیتابیس: `sosdelij_wp`
- [ ] ساخت کاربر: `sosdelij_dbu` با رمز تصادفی ۳۲ کاراکتری
- [ ] افزودن کاربر به دیتابیس با دسترسی **All Privileges**
- [ ] ذخیرهٔ نام دیتابیس/کاربر/رمز در Vault
- [ ] Collation: `utf8mb4_unicode_520_ci` (یا `utf8mb4_unicode_ci`)

> ⚠ **هرگز** از `utf8` استفاده نکنید؛ برای ایموجی و برخی حروف فارسی مشکل می‌سازد.

## گام ۴ — ساخت پوشه‌ها و دسترسی (۵ دقیقه)

- [ ] در `public_html`، محتوای پیش‌فرض هاستینگ (فایل‌های نمونه، `cgi-bin` خالی، `index.html` پیش‌فرض) پاک شود
- [ ] ساخت `staging.sos-delijan.ir` → پوشهٔ `staging_html` (Addon یا Subdomain)
- [ ] مجوزها:
  - پوشه‌ها: `755`
  - فایل‌ها: `644`
  - `wp-config.php`: `600` یا `400`
  - `wp-content/uploads`: `755`

## گام ۵ — SSL (۱۰ دقیقه)

- [ ] `SSL/TLS Status` → **Run AutoSSL** برای هر دو هاست
- [ ] تأیید صدور گواهی
- [ ] اگر AutoSSL موجود نیست → Let's Encrypt از طریق cPanel یا `certbot`
- [ ] اعمال قواعد `../01-domain/03-dns-and-ssl.md` بخش ۲ و ۳

## گام ۶ — SSH و WP-CLI (۱۵ دقیقه)

- [ ] فعال‌سازی SSH Access در کنترل پنل
- [ ] ساخت کلید SSH (نه رمز عبور) و آپلود کلید عمومی
- [ ] اتصال تست: `ssh user@sos-delijan.ir`
- [ ] بررسی WP-CLI: `wp --info` → اگر نبود:
  ```bash
  curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
  chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp
  ```
  (اگر دسترسی `sudo` نیست، در `~/bin` قرار دهید و به `PATH` اضافه کنید)

## گام ۷ — ایمیل (۱۵ دقیقه)

- [ ] ⛔ صندوق ایمیل ساخته **نشود** — کارفرما ایمیل سازمانی نمی‌خواهد (Q-20 / D-018)
- [ ] غیرفعال‌کردن ارسال ایمیل وردپرس (`pre_wp_mail → false`) تا از دامنه اسپم نشود
- [ ] تست ارسال به Gmail → باید به Inbox برود
- [ ] تست با `mail-tester.com` → هدف: ۱۰/۱۰
- [ ] فعال‌سازی Webmail و Forward به ایمیل کارفرما (اختیاری)

## گام ۸ — بکاپ و پایش (۱۰ دقیقه)

- [ ] بررسی تنظیمات بکاپ خودکار هاستینگ (زمان، تعداد نسخه، محل ذخیره)
- [ ] اگر بکاپ خارج از سرور نیست → برنامه‌ریزی برای UpdraftPlus (`../03-wordpress/05-security-and-backup.md`)
- [ ] ساخت مانیتور در **UptimeRobot** (رایگان):
  - `https://sos-delijan.ir` — هر ۵ دقیقه
  - اطلاع‌رسانی به ایمیل + پیام‌رسان
- [ ] ساخت مانیتور گواهی SSL (انقضا < ۱۴ روز → هشدار)

## گام ۹ — سخت‌کردن اولیه (۱۰ دقیقه)

- [ ] فعال‌سازی ModSecurity (اگر موجود)
- [ ] بررسی وضعیت Imunify360
- [ ] غیرفعال‌سازی `Directory Listing`
- [ ] ایجاد `.htaccess` پایه با قواعد `../01-domain/03-dns-and-ssl.md`
- [ ] بررسی `php.ini` → `display_errors = Off`, `log_errors = On`

---

## تست پذیرش این مرحله

| # | تست | انتظار |
|---|---|---|
| ۱ | `php -v` از طریق SSH | ۸.۲ یا ۸.۳ |
| ۲ | `php -i \| grep memory_limit` | ۵۱۲M |
| ۳ | `php -i \| grep max_input_vars` | ۳۰۰۰ |
| ۴ | اتصال به MySQL با اعتبارنامه‌های ساخته‌شده | موفق |
| ۵ | `wp --info` | خروجی صحیح |
| ۶ | `https://sos-delijan.ir` | گواهی معتبر |
| ۷ | تلاش سایت برای ارسال ایمیل | ⛔ هیچ ایمیلی ارسال نشود |
| ۸ | UptimeRobot | وضعیت Up |

پس از تیک‌خوردن همه → ادامه در `../03-wordpress/01-install-baseline.md`.

</div>
