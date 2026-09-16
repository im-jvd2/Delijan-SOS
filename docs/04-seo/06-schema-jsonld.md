---
id: SEO-06
title: دادهٔ ساخت‌یافته (JSON-LD)
status: approved
phase: 1
approved: 1405-06-25
---
<div dir="rtl" align="right">

# اسکیم‌ها و JSON-LD — کد آماده

> **روش اجرا:** کدهای زیر در یک **ویجت HTML المنتور** در پایین هر صفحه قرار می‌گیرند (یا از طریق Rank Math). مقادیر `{{…}}` با داده‌های `../05-content/nap-master.yaml` جایگزین شوند.
> **تست اجباری:** هر اسکیم‌ا پیش از انتشار در [Rich Results Test](https://search.google.com/test/rich-results) و [Schema Validator](https://validator.schema.org/) بدون خطا پاس شود.

---

## ۱. انتخاب نوع کسب‌وکار

| نوع | وضعیت |
|---|---|
| `AutoRepair` | ✅ **انتخاب اصلی** — زیرنوع رسمی `LocalBusiness` که گوگل برای نتایج غنی محلی می‌شناسد |
| `EmergencyService` | در schema.org موجود است اما در فهرست زیرانواع پشتیبانی‌شدهٔ گوگل برای LocalBusiness نیست |
| راه‌حل | `@type: ["AutoRepair", "EmergencyService"]` — گوگل `AutoRepair` را می‌شناسد و موتورهای دیگر هر دو را |
| `TowingService`? | ❌ در schema.org وجود ندارد — استفاده نشود |

---

## ۲. اسکیم‌ای سایت‌واید (Organization + WebSite)

در هدر سراسری یا تم‌بیلدر، یک بار:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://sos-delijan.ir/#organization",
      "name": "امداد خودرو دلیجان {{برند}}",
      "alternateName": "SOS دلیجان",
      "url": "https://sos-delijan.ir/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://sos-delijan.ir/wp-content/uploads/2026/09/logo.png",
        "width": 512,
        "height": 512
      },
      "description": "خدمات امداد خودرو، یدک‌کش، خودروبر و حمل خودرو به تعمیرگاه به‌صورت شبانه‌روزی در شهرستان دلیجان استان مرکزی و جاده‌های اطراف.",
      "telephone": "+989100504113",
      "areaServed": { "@id": "https://sos-delijan.ir/#service-area" },
      "sameAs": []
    },
    {
      "@type": "WebSite",
      "@id": "https://sos-delijan.ir/#website",
      "url": "https://sos-delijan.ir/",
      "name": "امداد خودرو دلیجان {{برند}}",
      "inLanguage": "fa-IR",
      "publisher": { "@id": "https://sos-delijan.ir/#organization" }
    }
  ]
}
</script>
```

---

## ۳. اسکیم‌ای صفحهٔ اصلی (AutoRepair + ServiceArea)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["AutoRepair", "EmergencyService"],
  "@id": "https://sos-delijan.ir/#localbusiness",
  "name": "امداد خودرو دلیجان {{برند}}",
  "image": "https://sos-delijan.ir/wp-content/uploads/2026/09/emdad-khodro-delijan.jpg",
  "url": "https://sos-delijan.ir/",
  "telephone": "+989100504113",
  "currenciesAccepted": "IRR",
  "paymentAccepted": "نقد، کارت به کارت",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "33.9906",
    "longitude": "50.6836"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  },
  "areaServed": {
    "@type": "Place",
    "@id": "https://sos-delijan.ir/#service-area",
    "name": "شهرستان دلیجان و جاده‌های اطراف",
    "containsPlace": [
      {"@type":"City","name":"دلیجان"},
      {"@type":"City","name":"نراق"},
      {"@type":"City","name":"محلات"},
      {"@type":"City","name":"نیم‌ور"},
      {"@type":"City","name":"سلفچگان"},
      {"@type":"City","name":"میمه"},
      {"@type":"City","name":"دودهک"},
      {"@type":"City","name":"جاسب"},
      {"@type":"City","name":"جوشق"},
      {"@type":"City","name":"هستیجان"}
    ]
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "خدمات امداد خودرو دلیجان",
    "itemListElement": [
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"یدک‌کش دلیجان"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"خودروبر کفی دلیجان"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"جرثقیل دلیجان"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"چرخگیر دلیجان"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"حمل خودرو به تعمیرگاه"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"حمل خودرو بین شهری"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"حمل خودرو تصادفی"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"حمل خودرو صفر کیلومتر"}}
    ]
  },
  "parentOrganization": { "@id": "https://sos-delijan.ir/#organization" }
}
</script>
```

> ⚠ `aggregateRating` **حذف شده است**. فقط اگر نظر واقعی و قابل استناد جمع شد، اضافه می‌شود:
> ```json
> "aggregateRating": {"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"27"}
> ```
> عدد جعلی = ریسک **Manual Action**. تصمیم **D-017 / X-006** — ساخت نظر جعلی رد شد.

### ۳.۱ چهار فیلدی که عمداً حذف شدند

| فیلد | چرا حذف شد | منبع |
|---|---|---|
| `"address"` / `streetAddress` | کسب‌وکار **سیار** است و دفتر فیزیکی ندارد؛ کارفرما هم آدرسی اعلام نکرد | Q-09 |
| `"email"` | هیچ ایمیل سازمانی وجود ندارد و در سایت نمایش داده نمی‌شود | Q-07 / D-018 |
| `"priceRange"` | کارفرما نرخ‌نامه ندارد و قیمت فقط با تماس اعلام می‌شود؛ نوشتن `$$` ادعای بی‌مدرک است | Q-21 / D-016 |
| `"aggregateRating"` / `"review"` | هیچ نظر واقعی وجود ندارد | Q-23 / D-017 |

### ۳.۲ دربارهٔ `geo`

مختصات `33.9906 / 50.6836` **مرکز شهر دلیجان** است (منبع: ویکی‌پدیا — `33°59′25″N 50°41′01″E`) و **موقعیت دفتر نیست**، چون دفتری وجود ندارد. این فیلد صرفاً به موتورهای جست‌وجو می‌گوید مرکز منطقهٔ خدمت کجاست. در Google Business Profile هم «Service-area business» انتخاب می‌شود، نه «Storefront».

---

## ۴. اسکیم‌ای صفحهٔ خدمت (Service)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "یدک‌کشی خودرو",
  "name": "یدک‌کش دلیجان",
  "description": "خدمات یدک‌کشی و حمل خودرو با نیسان یدک‌کش، چرخگیر و کفی خودروبر در دلیجان و جاده‌های اطراف، به‌صورت شبانه‌روزی.",
  "url": "https://sos-delijan.ir/خدمات/یدک-کش-دلیجان/",
  "provider": { "@id": "https://sos-delijan.ir/#localbusiness" },
  "areaServed": [
    {"@type":"City","name":"دلیجان"},
    {"@type":"City","name":"نراق"},
    {"@type":"City","name":"محلات"}
  ],
  "availableChannel": {
    "@type": "ServiceChannel",
    "servicePhone": {
      "@type": "ContactPoint",
      "telephone": "{{phone_e164}}",
      "contactType": "emergency",
      "areaServed": "IR",
      "availableLanguage": ["fa"]
    }
  },
  "termsOfService": "https://sos-delijan.ir/قوانین/"
}
</script>
```

---

## ۵. اسکیم‌ای FAQPage

برای بخش «پرسش‌های پرتکرار» هر صفحه:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "شماره امداد خودرو دلیجان چیست؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "برای درخواست امداد خودرو، یدک‌کش، خودروبر یا حمل به تعمیرگاه در دلیجان با شماره 0910 050 4113 تماس بگیرید. پاسخ‌گویی 24 ساعته و در همهٔ روزهای هفته انجام می‌شود."
      }
    },
    {
      "@type": "Question",
      "name": "امداد خودرو دلیجان شبانه‌روزی است؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "بله. خدمات امداد خودرو دلیجان در تمام ساعات شبانه‌روز و هفت روز هفته، شامل تعطیلات رسمی، ارائه می‌شود."
      }
    },
    {
      "@type": "Question",
      "name": "هزینه یدک‌کش در دلیجان چقدر است؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "هزینه به نوع خودرو، مسافت و نوع خدمت بستگی دارد. قیمت پیش از اعزام به‌صورت شفاف اعلام می‌شود. برای استعلام دقیق با {{phone_display}} تماس بگیرید."
      }
    },
    {
      "@type": "Question",
      "name": "مدت زمان رسیدن امدادگر در دلیجان چقدر است؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "در محدودهٔ شهری دلیجان معمولاً 10 تا 20 دقیقه و در جاده‌های اطراف 25 تا 45 دقیقه. زمان دقیق رسیدن هنگام تماس اعلام می‌شود."
      }
    },
    {
      "@type": "Question",
      "name": "آیا تعمیر خودرو در محل انجام می‌شود؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "خیر. ما تعمیر در محل انجام نمی‌دهیم. خودروی شما را با نیسان یدک‌کش، چرخگیر یا کفی خودروبر به نزدیک‌ترین تعمیرگاه معتبر منتقل می‌کنیم."
      }
    }
  ]
}
</script>
```

### قواعد FAQ
- متن سؤال و جواب باید **عیناً** در محتوای قابل‌مشاهدهٔ صفحه وجود داشته باشد
- حداکثر ۶ تا ۸ سؤال در هر صفحه
- سؤال‌ها واقعی و پرسیده‌شده باشند، نه ساختهٔ ما
- ⚠ گوگل از ۲۰۲۳ نمایش ریچ‌رزالت FAQ را محدود کرده؛ اسکیم‌ا همچنان به درک محتوا کمک می‌کند اما **روی ترافیک حساب نکنید**

---

## ۶. اسکیم‌ای BreadcrumbList

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"خانه","item":"https://sos-delijan.ir/"},
    {"@type":"ListItem","position":2,"name":"مناطق تحت پوشش","item":"https://sos-delijan.ir/مناطق/"},
    {"@type":"ListItem","position":3,"name":"امداد خودرو نراق","item":"https://sos-delijan.ir/مناطق/نراق/"}
  ]
}
</script>
```

> 💡 اگر Breadcrumb با Rank Math ساخته می‌شود، **اسکیم‌ای دستی اضافه نکنید** (تکرار اسکیم‌ا = خطا).

---

## ۷. اسکیم‌ای نوشتهٔ مجله (Article)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "عوامل تعیین هزینهٔ امداد خودرو و یدک‌کش در 1405",
  "description": "چه عواملی بر قیمت امداد خودرو، یدک‌کشی و خودروبر در دلیجان اثر می‌گذارد و چگونه قیمت پیش از اعزام اعلام می‌شود.",
  "image": "https://sos-delijan.ir/wp-content/uploads/2026/09/hazine-emdad.jpg",
  "datePublished": "2026-09-20",
  "dateModified": "2026-09-20",
  "inLanguage": "fa-IR",
  "author": { "@id": "https://sos-delijan.ir/#organization" },
  "publisher": { "@id": "https://sos-delijan.ir/#organization" },
  "mainEntityOfPage": "https://sos-delijan.ir/مجله/hazine-emdad-khodro/"
}
</script>
```

> ⚠ از `Person` به‌عنوان نویسنده استفاده نکنید مگر نویسندهٔ واقعی با پروفایل داشته باشید.

---

## ۸. ماتریس اسکیم‌ا به تفکیک صفحه

| صفحه | Organization | WebSite | AutoRepair | Service | FAQPage | Breadcrumb | Article |
|---|---|---|---|---|---|---|---|
| همه | ✅ (یک بار) | ✅ (یک بار) | — | — | — | ✅ | — |
| صفحهٔ اصلی | — | — | ✅ | — | ✅ | — | — |
| صفحهٔ خدمت | — | — | — | ✅ | ✅ | ✅ | — |
| صفحهٔ شهری | — | — | ✅ (با `areaServed` محلی) | — | ✅ | ✅ | — |
| صفحهٔ جاده‌ای | — | — | ✅ (با `areaServed` محلی) | — | ✅ | ✅ | — |
| نوشتهٔ مجله | — | — | — | — | اختیاری | ✅ | ✅ |

---

## ۹. خطاهای رایج

| خطا | پیامد |
|---|---|
| دو اسکیم‌ای `LocalBusiness` در یک صفحه | گیج‌شدن خزنده |
| اسکیم‌ای FAQ بدون محتوای قابل‌مشاهدهٔ متناظر | نقض دستورالعمل گوگل |
| `aggregateRating` بدون نظر واقعی | Manual Action |
| تلفن با فرمت متفاوت در اسکیم‌ا و سایت | ناسازگاری NAP |
| `@id` متفاوت در اسکیم‌اهای مختلف | از دست رفتن پیوند گراف |
| JSON نامعتبر (کامای اضافی) | کل اسکیم‌ا نادیده گرفته می‌شود |
| استفاده از `TowingService` | نوع نامعتبر |

---

## ۱۰. چک‌لیست پذیرش

- [ ] همهٔ اسکیم‌ها در Rich Results Test بدون خطا
- [ ] فقط یک `LocalBusiness` در هر صفحه
- [ ] NAP در اسکیم‌ا = NAP در سایت
- [ ] `aggregateRating` فقط با مدرک واقعی
- [ ] `@id`ها سازگار و یکتا
- [ ] اسکیم‌ای FAQ با محتوای قابل‌مشاهده مطابقت دارد
- [ ] JSON با ابزار اعتبارسنجی (نه چشمی) بررسی شده

</div>
