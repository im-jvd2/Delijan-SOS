---
id: SEO-04
title: سئوی فنی
status: approved
phase: 1
approved: 1405-06-25
---
<div dir="rtl" align="right">

# سئوی فنی (Technical SEO)

---

## ۱. خزیدن و ایندکس

### ۱.۱ `robots.txt`
```
User-agent: *
Allow: /

Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /?s=
Disallow: /search/
Disallow: /staging/
Disallow: /*?replytocom=
Disallow: /*?share=
Disallow: /*?utm_

Sitemap: https://sos-delijan.ir/sitemap_index.xml
```

### ۱.۲ Sitemap XML
| تنظیم | مقدار |
|---|---|
| تولیدکننده | Rank Math |
| شامل | برگه‌ها، نوشته‌ها، (دسته‌بندی اصلی اگر محتوا دارد) |
| خارج | تگ‌ها، آرشیو نویسنده، صفحات utility، staging |
| پینگ خودکار به گوگل | ✅ |
| بررسی دستی | `https://sos-delijan.ir/sitemap_index.xml` باید باز شود |

### ۱.۳ Canonical
- هر صفحه `rel="canonical"` **خوداشاره** (self-referencing) دارد
- صفحات با پارامتر → canonical به نسخهٔ بدون پارامتر
- دامنه‌های ریدایرکت‌شده → canonical روی دامنهٔ اصلی

### ۱.۴ مدیریت ایندکس
| صفحه | دستور |
|---|---|
| جست‌وجوی داخلی | `noindex, follow` |
| آرشیو برچسب | `noindex, follow` |
| آرشیو نویسنده | `noindex, follow` |
| صفحهٔ ۴۰۴ | `noindex` (خودکار) |
| صفحات نازک/تکراری | `noindex` یا حذف + `301` |

---

## ۲. صفحهٔ ۴۰۴

صفحهٔ ۴۰۴ **سفارشی** ساخته شود (قالب تم‌بیلدر `E-404`):

```
[H1] صفحه‌ای که دنبالش بودید پیدا نشد
متن: ممکن است آدرس تغییر کرده باشد. در مواقع اضطراری همین حالا تماس بگیرید.
[دکمهٔ بزرگ تماس]  0910 050 4113
[لینک‌های سریع] صفحهٔ اصلی · خدمات · مناطق تحت پوشش · تعرفه · مجله
[جست‌وجو] (اختیاری)
```

- کد HTTP باید **۴۰۴** باشد (نه ۲۰۰ با محتوای «یافت نشد»)
- در `Redirection` لاگ شود تا ریدایرکت ساخته شود

---

## ۳. ریدایرکت‌ها

| قاعده | جزئیات |
|---|---|
| فقط `301` برای مهاجرت دائمی | هرگز `302` برای URL دائمی |
| بدون زنجیره | `A→B→C` ❌ — مستقیم `A→C` |
| بدون حلقه | تست شود |
| ثبت همه در پلاگین Redirection | قابل پایش |
| پایش ۴۰۴ | هفتگی، از `Redirection → 404s` |

### چک تست ریدایرکت
```bash
for u in "/" "/خدمات/" "/مناطق/نراق/" "/جاده/دلیجان-به-قم/" "/هزینه/"; do
  curl -sI -o /dev/null -w "%{http_code} %{url_effective} -> %{redirect_url}\n" \
    "https://sos-delijan.ir$u"
done
```

---

## ۴. داده‌های ساخت‌یافته

فهرست کامل و کد آماده در `06-schema-jsonld.md`.

| صفحه | اسکیم‌ها |
|---|---|
| همه | `Organization` یا `WebSite` |
| صفحهٔ اصلی | `AutoRepair` (LocalBusiness) + `FAQPage` |
| صفحهٔ خدمت | `Service` + `FAQPage` |
| صفحهٔ شهری | `AutoRepair` با `areaServed` محلی + `FAQPage` |
| نوشتهٔ مجله | `Article` + `BreadcrumbList` |
| همه | `BreadcrumbList` |

---

## ۵. Core Web Vitals

اهداد و پروتکل در `../03-wordpress/04-performance-and-cache.md`.

### نکات فنی سئویی
| معیار | اقدام کلیدی |
|---|---|
| LCP | تصویر Hero با `fetchpriority="high"`، WebP، بدون lazy |
| CLS | ابعاد صریح همهٔ تصاویر/iframeها، رزرو فضا برای نوار چسبان |
| INP | حذف JS غیرضروری، defer، حذف اسلایدر سنگین |

---

## ۶. کنسول‌ها و ابزارها

### ۶.۱ Google Search Console
- [ ] تأیید مالکیت (از طریق رکورد DNS یا فایل)
- [ ] ارسال sitemap
- [ ] بررسی «Pages» → خطای پوشش = ۰
- [ ] بررسی «Core Web Vitals»
- [ ] فعال‌سازی اعلان‌ها به ایمیل تیم
- [ ] **ثبت خط‌پایه** در روز لانچ

### ۶.۲ Bing Webmaster Tools
- [ ] تأیید + ارسال sitemap
- [ ] امکان ایمپورت از GSC
- [ ] **IndexNow** فعال (از طریق Rank Math) — ایندکس سریع‌تر

### ۶.۳ Google Analytics 4
- [ ] نصب با GTM یا مستقیم
- [ ] رویدادهای کلیدی:
  | رویداد | تریگر |
  |---|---|
  | `click_phone` | کلیک روی `tel:` |
  | ~~`click_whatsapp`~~ | ⛔ حذف شد — پیام‌رسانی در سایت نیست (Q-08) |
  | `scroll_75` | اسکرول ۷۵٪ |
  | `view_faq` | بازکردن آکاردئون FAQ |
- [ ] تعریف `click_phone` به‌عنوان **Conversion**
- [ ] گزارش «مسیر تماس» بر اساس صفحهٔ فرود

> 💡 **این مهم‌ترین KPI تجاری است:** کدام صفحه بیشترین تماس را می‌سازد. بدون آن، بهینه‌سازی محتوا کور است.

### ۶.۴ ابزارهای ایرانی
| ابزار | کاربرد |
|---|---|
| **نشان (neshan.org)** | ثبت کسب‌وکار + نقشه |
| **بلد (balad.ir)** | ثبت کسب‌وکار |
| گوگل مپ | در صورت امکان (محدودیت‌های ایران — بخش `05-local-seo-and-nap.md`) |

---

## ۷. موبایل و دسترسی‌پذیری فنی

- [ ] Viewport meta صحیح
- [ ] بدون سرریز افقی در ۳۶۰px
- [ ] همهٔ اهداف لمسی ≥ ۴۸×۴۸ پیکسل
- [ ] کنتراست متن ≥ 4.5:1
- [ ] `lang="fa-IR"` و `dir="rtl"` روی `<html>`
- [ ] `prefers-reduced-motion` رعایت شده
- [ ] تست با Mobile-Friendly Test

---

## ۸. نکات امنیتی با اثر سئویی

| مورد | اثر |
|---|---|
| HTTPS بدون Mixed Content | الزام |
| بدون بدافزار | Manual Action |
| زمان پاسخ سرور پایین | CWV |
| بدون ریدایرکت به سایت‌های سوم | هک = حذف از گوگل |

---

## ۹. چک‌لیست پذیرش سئوی فنی

| # | مورد | ابزار تأیید |
|---|---|---|
| ۱ | `robots.txt` درست و sitemap در آن آدرس‌دهی شده | مرورگر |
| ۲ | sitemap_index.xml باز می‌شود و همهٔ صفحات مهم را دارد | مرورگر |
| ۳ | هر صفحه canonical خوداشاره دارد | View Source |
| ۴ | هیچ صفحهٔ `noindex` ناخواسته‌ای وجود ندارد | `site:` در گوگل |
| ۵ | ۴۰۴ کد درست برمی‌گرداند و صفحهٔ سفارشی دارد | curl |
| ۶ | همهٔ ریدایرکت‌ها `301` و بدون زنجیره | curl |
| ۷ | اسکیم‌ها بدون خطا | Rich Results Test |
| ۸ | CWV در حد هدف | PageSpeed Insights |
| ۹ | GSC بدون خطای پوشش | Search Console |
| ۱۰ | GA4 رویدادهای تماس را ثبت می‌کند | DebugView |
| ۱۱ | تست موبایل پاس | Mobile-Friendly Test |
| ۱۲ | SSL Labs گرید A | SSL Labs |
| ۱۳ | `site:sos-delijan.ir` همهٔ صفحات را نشان می‌دهد | گوگل |
| ۱۴ | هیچ محتوای تکراری ایندکس‌شده نیست | گوگل |

</div>
