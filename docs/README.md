<div dir="rtl" align="right">

# مستندات پروژه «امداد خودرو و یدک‌کش دلیجان»

> **وضعیت فعلی: فاز ۱ — مستندسازی ✅ تکمیل شد**
>
> هر ۳۶ پرسش کارفرما (Q-01 تا Q-36) پاسخ داده و در مستندات اعمال شد.
> ۲۲ تصمیم (D-001 تا D-022) ثبت و ۸ گزینه رد شد (X-001 تا X-008).
>
> **خروجی:** ۹۶ صفحهٔ برنامه‌ریزی‌شده در ۶ موج، نقشهٔ راه ۲۸۵ گامی، سیستم طراحی و اسکیم‌ای کامل.
>
> ➡️ **گام بعدی:** تأیید صریح کارفرما روی این مستندات، سپس فاز ۲ (طراحی UI و پیاده‌سازی در وردپرس + المنتور پرو).

---

## ۱. این ریپازیتوری چیست

مخزن `Delijan-SOS` دو نقش دارد:

| نقش | محتوا | فاز |
|---|---|---|
| **۱) پایگاه دانش پروژه** | همهٔ مستندات از گام صفر (خرید دامنه و هاست) تا تحویل نهایی به کارفرما | فاز ۱ ← **هم‌اکنون** |
| **۲) کد رابط کاربری (UI)** | پروتوتایپ HTML/CSS و سپس پیاده‌سازی در وردپرس + المنتور پرو + قالب هلو المنتور | فاز ۲ |

سایت نهایی **وردپرس** است. این ریپو بک‌اند ندارد و نخواهد داشت؛ کدی که اینجا نوشته می‌شود صرفاً لایهٔ نمایش (فرانت) و پروتوتایپ است.

---

## ۲. سیاست ایزوله‌بودن (مهم)

- تمام کارها روی برنچ **`arena/01a0a8d8-delijan-sos`** انجام می‌شود. برنچ `main` دست‌نخورده است.
- هیچ `push` به `main`، هیچ merge و هیچ Pull Request بدون تأیید صریح کارفرما انجام نمی‌شود.
- همهٔ فایل‌های این فاز داخل پوشهٔ `docs/` قرار دارند (کاملاً افزودنی و قابل بازگشت). اگر ترجیح می‌دهید مستندات جای دیگری باشد، با یک دستور قابل جابه‌جایی است.
- برای بازبینی: `git diff main --stat` روی همین برنچ.

---

## ۳. نقشهٔ راه کل پروژه

| فاز | عنوان | خروجی اصلی | وابستگی |
|---|---|---|---|
| **۰** | کشف و تصمیم | منشور پروژه + تصمیم‌های بسته‌شده | — |
| **۱** | مستندسازی کامل | همین پوشه `docs/` | فاز ۰ |
| **۲** | طراحی UI | سیستم طراحی + وایرفریم + پروتوتایپ HTML | تأیید فاز ۱ |
| **۳** | زیرساخت | خرید دامنه، هاست، SSL، DNS | تصمیم D-001 / D-003 |
| **۴** | راه‌اندازی وردپرس | نصب، پلاگین‌ها، قالب، تم‌بیلدر | فاز ۳ |
| **۵** | تولید محتوا | صفحات خدماتی / شهری / جاده‌ای / بلاگ | فاز ۴ |
| **۶** | سئوی فنی و لانچ | اسکیم‌ها، GSC، CWV، چک‌لیست لانچ | فاز ۵ |
| **۷** | تحویل | بستهٔ تحویل، آموزش، SLA | فاز ۶ |

---

## ۴. فهرست مستندات

### ۰۰ — منشور و حکمرانی
| فایل | توضیح |
|---|---|
| ⭐ [`00-charter/05-master-action-plan.md`](00-charter/05-master-action-plan.md) | **برنامهٔ گام‌به‌گام کل پروژه — ۲۸۵ گام در ۱۲ مرحله** (نقطهٔ شروع اجرایی) |
| [`00-charter/01-project-charter.md`](00-charter/01-project-charter.md) | هدف، دامنه، محدودیت‌ها، شاخص‌های موفقیت (KPI) |
| [`00-charter/02-roles-and-milestones.md`](00-charter/02-roles-and-milestones.md) | نقش‌ها (RACI) و مایل‌ستون‌ها با معیار پذیرش |
| [`00-charter/03-decisions-log.md`](00-charter/03-decisions-log.md) | **لاگ تصمیم‌ها (ADR)** — منبع حقیقتِ تصمیم‌ها |
| [`00-charter/04-open-questions.md`](00-charter/04-open-questions.md) | **پرسش و پاسخ کارفرما** — هر ۳۶ پرسش پاسخ داده شد ✅ |

### ۰۱ — دامنه
| فایل | توضیح |
|---|---|
| [`01-domain/01-domain-strategy.md`](01-domain/01-domain-strategy.md) | مقایسهٔ `sos-delijan.ir` و `emdadkhodrodelijan.ir` + پیشنهاد |
| [`01-domain/02-irnic-registration-sop.md`](01-domain/02-irnic-registration-sop.md) | گام‌به‌گام ثبت دامنهٔ `.ir` در ایرنیک + احراز هویت هدا |
| [`01-domain/03-dns-and-ssl.md`](01-domain/03-dns-and-ssl.md) | معماری DNS، رکوردها، TLS، سیاست دامنهٔ رسمی |

### ۰۲ — هاست
| فایل | توضیح |
|---|---|
| [`02-hosting/01-hosting-requirements.md`](02-hosting/01-hosting-requirements.md) | مشخصات فنی اجباری و desiderata |
| [`02-hosting/02-vendor-shortlist.md`](02-hosting/02-vendor-shortlist.md) | فهرست کوتاه تأمین‌کنندگان + معیار امتیازدهی |
| [`02-hosting/03-hosting-setup-sop.md`](02-hosting/03-hosting-setup-sop.md) | SOP خرید تا آماده‌سازی سرور |

### ۰۳ — وردپرس
| فایل | توضیح |
|---|---|
| [`03-wordpress/01-install-baseline.md`](03-wordpress/01-install-baseline.md) | نصب و پیکربندی پایه |
| [`03-wordpress/02-plugin-stack.md`](03-wordpress/02-plugin-stack.md) | فهرست پلاگین‌ها (اجباری / اختیاری / ممنوع) |
| [`03-wordpress/03-hello-elementor-and-theme-builder.md`](03-wordpress/03-hello-elementor-and-theme-builder.md) | قالب هلو + تم‌بیلدر + استایل سراسری |
| [`03-wordpress/04-performance-and-cache.md`](03-wordpress/04-performance-and-cache.md) | Core Web Vitals، کش، CDN |
| [`03-wordpress/05-security-and-backup.md`](03-wordpress/05-security-and-backup.md) | امنیت، بکاپ، مدیریت رمزها |

### ۰۴ — سئو
| فایل | توضیح |
|---|---|
| [`04-seo/01-keyword-research.md`](04-seo/01-keyword-research.md) | **خوشه‌های کلیدواژه** (هسته، یدک‌کش، سیار، جاده‌ای، شهری، بلاگ) |
| [`04-seo/02-site-architecture.md`](04-seo/02-site-architecture.md) | معماری اطلاعات، الگوی URL، لینک داخلی |
| [`04-seo/03-on-page-standard.md`](04-seo/03-on-page-standard.md) | استاندارد تایتل/متا/H1/تعداد کلمه |
| [`04-seo/04-technical-seo.md`](04-seo/04-technical-seo.md) | sitemap، robots، canonical، CWV، کنسول‌ها |
| [`04-seo/05-local-seo-and-nap.md`](04-seo/05-local-seo-and-nap.md) | NAP، نقشه‌های ایرانی، سیگنال‌های محلی، ریویو |
| [`04-seo/06-schema-jsonld.md`](04-seo/06-schema-jsonld.md) | کد آمادهٔ JSON-LD |
| [`04-seo/07-competitor-analysis.md`](04-seo/07-competitor-analysis.md) | **تحلیل ۹ رقیب واقعی** + شکاف‌های قابل استفاده |
| [`04-seo/08-content-calendar-and-linkbuilding.md`](04-seo/08-content-calendar-and-linkbuilding.md) | تقویم ۱۲ هفته‌ای + لینک‌سازی |
| [`04-seo/09-kpi-and-reporting.md`](04-seo/09-kpi-and-reporting.md) | خط‌پایه، هدف‌ها، قالب گزارش |

### ۰۵ — محتوا
| فایل | توضیح |
|---|---|
| [`05-content/01-editorial-guidelines.md`](05-content/01-editorial-guidelines.md) | لحن، قواعد نگارش فارسی، خطوط قرمز |
| [`05-content/02-page-inventory.md`](05-content/02-page-inventory.md) | **فهرست کامل صفحات** با URL، تایتل، کلیدواژه، اولویت |
| ⭐ [`05-content/03-content-production-plan.md`](05-content/03-content-production-plan.md) | **برنامهٔ تولید همهٔ ۹۶ صفحه** در ۶ موج + کتابخانهٔ اسکلت محتوا |
| ⭐ [`05-content/url-map.yaml`](05-content/url-map.yaml) | **منبع حقیقت آدرس‌ها (D-025)** — نگاشت هر ۹۶ آدرس فارسی + قواعد اسلاگ |
| [`05-content/nap-master.yaml`](05-content/nap-master.yaml) | **منبع حقیقت NAP** — نام/آدرس/تلفن/پوشش/خدمات (machine-readable) |

### ۰۶ — طراحی
| فایل | توضیح |
|---|---|
| [`06-design/01-design-system.md`](06-design/01-design-system.md) | رنگ، تایپوگرافی، فاصله، دسترسی‌پذیری |
| [`06-design/02-wireframes-and-elementor-map.md`](06-design/02-wireframes-and-elementor-map.md) | وایرفریم صفحه‌خانه + نگاشت به ویجت‌های المنتور |

### ۰۷ — تحویل
| فایل | توضیح |
|---|---|
| [`07-delivery/01-launch-checklist.md`](07-delivery/01-launch-checklist.md) | چک‌لیست لانچ + روز انتشار + برنامهٔ بازگشت |
| [`07-delivery/02-handover-and-training.md`](07-delivery/02-handover-and-training.md) | بستهٔ تحویل + سرفصل آموزش کارفرما |
| [`07-delivery/03-maintenance-sla.md`](07-delivery/03-maintenance-sla.md) | سطوح پشتیبانی و تقویم تمدیدها |

### ۰۸ — حقوقی
| فایل | توضیح |
|---|---|
| [`08-legal/01-privacy-and-terms.md`](08-legal/01-privacy-and-terms.md) | الگوی حریم خصوصی و قوانین + الزامات قانونی صنعت |

### قالب‌ها
| فایل | توضیح |
|---|---|
| [`templates/page-brief.md`](templates/page-brief.md) | بریف تولید محتوای یک صفحه |
| [`templates/weekly-report.md`](templates/weekly-report.md) | قالب گزارش هفتگی سئو |

---

## ۵. قراردادهای این مخزن

- **زبان مستندات:** فارسی. واژه‌های فنی به شکل رایج فارسی + معادل لاتین در پرانتز، در نخستین استفاده.
- **نام فایل:** `NN-kebab-case.md`؛ شماره پیشرو ترتیب خواندن را می‌دهد.
- **لینک‌ها:** نسبی و داخل مخزن.
- **تاریخ:** شمسی در متن، میلادی در metadata (`date:`).
- **هر تصمیم** باید در `00-charter/03-decisions-log.md` ثبت شود؛ متن پراکنده در فایل‌ها منبع حقیقت نیست.
- **هر ادعای عددی** (قیمت، فاصله، حجم جست‌وجو) یا منبع‌دار است یا با برچسب `⚠ نیازمند تأیید` مشخص شده.

---

## ۶. چگونه بازبینی و تأیید کنید

1. ✅ **انجام شد** — هر ۳۶ پرسش در `00-charter/04-open-questions.md` پاسخ داده و ثبت شد.
2. ✅ **انجام شد** — همهٔ تصمیم‌ها در `00-charter/03-decisions-log.md` به وضعیت «پذیرفته‌شده» درآمدند.
3. 📖 **بازبینی نهایی:** سه فایل اجرایی را بخوانید:
   - `00-charter/05-master-action-plan.md` — نقشهٔ راه ۲۸۵ گامی
   - `05-content/02-page-inventory.md` — فهرست ۹۶ صفحه
   - `05-content/03-content-production-plan.md` — زمان‌بندی ۶ موج
4. 🚦 **تأیید شما** → شروع فاز ۲ (UI).

</div>
