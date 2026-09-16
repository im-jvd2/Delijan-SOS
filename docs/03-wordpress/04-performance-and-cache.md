---
id: WP-04
title: پرفورمنس و Core Web Vitals
status: approved
phase: 1
approved: 1405-06-25
---
<div dir="rtl" align="right">

# پرفورمنس و Core Web Vitals

> **اصل:** کاربر ما در حاشیهٔ جاده، با اینترنت موبایل ۳G/4G ضعیف است. هر ثانیه = مشتریِ از دست رفته.
> **هدف سنجش:** موبایل، شبکهٔ شبیه‌سازی‌شدهٔ «Fast 4G» با CPU throttling 4x.

---

## ۱. اهداف عددی

| معیار | هدف | حد شکست |
|---|---|---|
| **LCP** (Largest Contentful Paint) | < ۲٫۰ ثانیه | > ۲٫۵ ثانیه |
| **INP** (Interaction to Next Paint) | < ۱۵۰ میلی‌ثانیه | > ۲۰۰ میلی‌ثانیه |
| **CLS** (Cumulative Layout Shift) | < ۰٫۰۵ | > ۰٫۱ |
| **TTFB** | < ۳۰۰ میلی‌ثانیه | > ۶۰۰ میلی‌ثانیه |
| **وزن کل صفحه** | < ۱٫۲ مگابایت | > ۲ مگابایت |
| **تعداد درخواست‌ها** | < ۶۰ | > ۱۰۰ |
| **PageSpeed موبایل** | ≥ ۹۰ | < ۸۰ |

---

## ۲. بودجهٔ پرفورمنس (Performance Budget) — صفحهٔ اصلی

| نوع دارایی | سقف |
|---|---|
| HTML | ≤ ۶۰ KB (فشرده) |
| CSS کل | ≤ ۱۲۰ KB |
| JavaScript کل | ≤ ۱۵۰ KB |
| فونت‌ها | ≤ ۱۲۰ KB (یک فایل woff2 زیرمجموعه‌شده) |
| تصویر LCP (Hero) | ≤ ۱۵۰ KB (WebP/AVIF) |
| سایر تصاویر (lazy) | ≤ ۶۰۰ KB |
| **جمع** | **≤ ۱٫۲ MB** |

> 📌 اگر از بودجه عبور شد، **قبل از انتشار** اصلاح شود — نه بعداً.

---

## ۳. لایه‌های کش

```
مرورگر کاربر
   ↓  (Cache-Control، ۱ سال برای دارایی‌های نسخه‌دار)
CDN داخلی (اختیاری)
   ↓
LiteSpeed Cache  ← لایهٔ اصلی؛ صفحهٔ کامل HTML کش می‌شود
   ↓
Object Cache (Redis)  ← کش کوئری‌های دیتابیس
   ↓
OPcache  ← کش کد PHP کامپایل‌شده
   ↓
MySQL
```

### ۳.۱ هدرهای کش دارایی‌های ایستا
```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png  "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/css   "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
</IfModule>
```

> ⚠ LiteSpeed با «فایل‌های نسخه‌دار» (`?ver=`) این کار را خودکار انجام می‌دهد. اگر دستی نسخه‌گذاری نمی‌کنید، هنگام به‌روزرسانی باید Purge بزنید.

---

## ۴. فونت فارسی

### ۴.۱ روش صحیح
1. دانلود وزیرمتن نسخهٔ **Variable** یا وزن‌های جدا
2. **زیرمجموعه‌سازی (subsetting)** برای حروف فارسی + ارقام فارسی + لاتین پایه:
   ```bash
   pyftsubset Vazirmatn.ttf \
     --unicodes=U+0600-06FF,U+FB50-FDFF,U+FE70-FEFF,U+0030-0039,U+0020-007E \
     --layout-features='*' --flavor=woff2 \
     --output-file=vazirmatn-subset.woff2
   ```
3. بارگذاری به‌عنوان **Custom Font** در المنتور (`Site Settings → Custom Fonts`)
4. `font-display: swap`
5. **`preload`** فایل فونت:
   ```html
   <link rel="preload" href="/wp-content/uploads/fonts/vazirmatn-subset.woff2"
         as="font" type="font/woff2" crossorigin>
   ```

### ۴.۲ ممنوع
- ❌ Google Fonts (درخواست خارجی، تأخیر، احتمال فیلتر)
- ❌ بارگذاری ۶ وزن فونت (هر وزن یک فایل = ۶ درخواست)
- ❌ فونت چندبخشی بدون `unicode-range`

> 📌 **قاعده:** حداکثر **۲ فایل فونت** (یک Variable یا دو وزن).

---

## ۵. تصاویر

| قاعده | جزئیات |
|---|---|
| فرمت | **WebP** (و AVIF اگر پشتیبانی شود) |
| ابعاد صریح | `width` و `height` همیشه → جلوگیری از CLS |
| تصویر Hero (LCP) | ❌ lazy نشود؛ `fetchpriority="high"` و `preload` |
| تصاویر زیر خط | `loading="lazy"` و `decoding="async"` |
| نام فایل | توصیفی و انگلیسی: `yadak-kesh-delijan-nissan.webp` |
| `alt` | فارسی و توصیفی (نه تکرار کلیدواژه) |
| ابعاد منبع | حداکثر ۱۹۲۰px عرض؛ هرگز ۴۰۰۰px آپلود نکنید |
| پس‌زمینه‌های CSS | برای گرادینت‌ها به‌جای تصویر |

### دستور بهینه‌سازی دسته‌ای
```bash
# نصب
apt install webp
# تبدیل
for f in *.jpg *.png; do cwebp -q 82 -m 6 "$f" -o "${f%.*}.webp"; done
```

---

## ۶. JavaScript و CSS

| اقدام | وضعیت |
|---|---|
| حذف jQuery Migrate | ✅ (LSCache) |
| defer کردن اسکریپت‌های غیربحرانی | ✅ |
| حذف CSS ویجت‌های استفاده‌نشده | ✅ (Improved CSS Loading) |
| Minify | ✅ |
| Combine CSS/JS | ⚠ **تست شود** — گاهی به دلیل FOUC و مسدودشدن رندر، نتیجه بدتر است |
| Critical CSS | فقط اگر ابزار مطمئن داریم؛ وگرنه رها شود |
| حذف اسکریپت‌های ردیابی غیرضروری | ✅ |
| حذف اسکریپت‌های شخص ثالث (چت، نقشهٔ سنگین) | ✅ |

> ⚠ **نقشه:** هرگز Google Maps را به‌صورت iframe سنگین بارگذاری نکنید. جایگزین: یک **تصویر ایستای نقشه** با لینک به نقشهٔ خارجی، یا نقشهٔ سبک «نشان» با بارگذاری تنبل.

---

## ۷. الگوهای طراحی که سرعت را می‌کشند

| ❌ نکنید | ✅ بکنید |
|---|---|
| ویدیوی پس‌زمینه در Hero | تصویر WebP سبک + گرادینت |
| اسلایدر با ۸ اسلاید | یک تصویر ثابت یا حداکثر ۳ اسلاید |
| انیمیشن‌های زیاد هنگام اسکرول | انیمیشن ساده و کم؛ `prefers-reduced-motion` رعایت شود |
| آیکون‌های FontAwesome فونتی | SVG (تنظیم المنتور) |
| پارالاکس | حذف |
| فونت آیکون اختصاصی | SVG inline |
| بخش‌های تودرتو (Inner Section) | Container تودرتو با حداقل عمق |

---

## ۸. CDN

| گزینه | نکته |
|---|---|
| **آروان‌کلاد (ArvanCloud)** | ایرانی، PoP در شهرهای ایران، پلن رایگان دارد ✅ پیشنهاد |
| CDN خود هاستینگ | ساده‌ترین گزینه، معمولاً کافی |
| Cloudflare | ⚠ در ایران تجربهٔ ناپایداری دارد (مسیریابی و latency متغیر) — توصیه نمی‌شود برای مخاطب صرفاً ایرانی |

**پیکربندی CDN:**
- [ ] کش فقط برای دارایی‌های ایستا (تصویر/CSS/JS/فونت) — **نه** HTML داینامیک (تا کش LSCache تداخل نکند)
- [ ] حذف کش برای `/wp-admin/` و `/wp-login.php`
- [ ] فعال‌سازی HTTPS و HSTS روی CDN
- [ ] تست پس از فعال‌سازی: همهٔ منابع از دامنهٔ CDN می‌آیند و Mixed Content نیست

---

## ۹. روش اندازه‌گیری (استاندارد پروژه)

### ۹.۱ ابزارها
| ابزار | کاربرد |
|---|---|
| **PageSpeed Insights** | CWV میدانی + آزمایشگاهی |
| **GTmetrix** | Waterfall دقیق |
| **WebPageTest** | تست با لوکیشن و اتصال دلخواه |
| **CrUX / GSC → Core Web Vitals** | دادهٔ واقعی کاربران پس از لانچ |
| **Chrome DevTools → Lighthouse** | تست سریع محلی |

### ۹.۲ پروتکل تست (اجباری پیش از انتشار هر صفحه)
1. پاک‌کردن کش سایت
2. اجرا در حالت **Incognito** (بدون افزونه)
3. دستگاه: Moto G Power / شبکه: Fast 4G / CPU: 4x throttle
4. **۳ اجرا** و ثبت **میانه** (نه بهترین)
5. ثبت در `../04-seo/09-kpi-and-reporting.md`

### ۹.۳ قالب ثبت
```
صفحه: /مناطق/نراق/
تاریخ: ۱۴۰۵/۰۶/۲۵
LCP: 1.8s | INP: 120ms | CLS: 0.02 | TTFB: 210ms
وزن: 890 KB | درخواست‌ها: 42
PageSpeed Mobile: 94 / Desktop: 99
ابزار: PSI
```

---

## ۱۰. عیب‌یابی رایج

| نشانه | علت احتمالی | راه‌حل |
|---|---|---|
| LCP بالا، TTFB خوب | تصویر Hero سنگین یا lazy شده | `fetchpriority="high"` + WebP + حذف lazy |
| TTFB بالا | کش غیرفعال یا سرور ضعیف | بررسی هدر `x-litespeed-cache`؛ اگر `miss` ماند، Crawler/Purge |
| CLS غیرصفر | تصویر/فونت بدون ابعاد، بنر چسبان | ابعاد صریح + `font-display: swap` + رزرو فضا |
| INP بالا | JS زیاد، انیمیشن‌ها | حذف اسلایدر و انیمیشن، defer |
| صفحهٔ المنتور ذخیره نمی‌شود | `max_input_vars` پایین | افزایش به ۳۰۰۰ (فایل `HOST-01`) |
| خطای ۵۰۰ در ویرایشگر | `memory_limit` پایین | افزایش به ۵۱۲M |
| فونت فارسی پرش می‌کند (FOUT) | نبود preload | افزودن `preload` |

</div>
