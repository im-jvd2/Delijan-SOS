#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
راستی‌آزمایی خودکار مستندات پروژهٔ Delijan-SOS
=================================================
این اسکریپت همهٔ ادعاهای عددی و ساختاری مستندات را با خودِ فایل‌ها می‌سنجد.

    python3 tools/verify.py

خروجی: فهرست PASS/FAIL و در پایان «ALL PASS» یا تعداد FAIL.
هر بررسی که FAIL شود یعنی جایی در مستندات با منبع حقیقت نمی‌خواند.

وابستگی: PyYAML  (pip3 install --break-system-packages pyyaml)
"""
from __future__ import annotations

import collections
import glob
import json
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML لازم است:  pip3 install --break-system-packages pyyaml")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OPEN_TAG = '<div dir="rtl" align="right">'

# ---------------------------------------------------------------- utilities
FA_MAP = {chr(0x06F0 + i): str(i) for i in range(10)}
FA_MAP.update({chr(0x0660 + i): str(i) for i in range(10)})


def fa(s: str) -> str:
    """ارقام فارسی/عربی را به لاتین تبدیل می‌کند (فقط برای مقایسهٔ عددی)."""
    return "".join(FA_MAP.get(c, c) for c in s)


oks, fails = [], []


def check(label: str, ok: bool, detail: str = "") -> None:
    (oks if ok else fails).append(f"{label} {detail}".strip())


# ---------------------------------------------------------------- load docs
docs = {}
for f in sorted(glob.glob("docs/**/*.md", recursive=True)) + ["README.md"]:
    with open(f, encoding="utf-8") as fh:
        docs[f] = fh.read()

inv = docs["docs/05-content/02-page-inventory.md"]
plan = docs["docs/05-content/03-content-production-plan.md"]
mp = docs["docs/00-charter/05-master-action-plan.md"]
dec = docs["docs/00-charter/03-decisions-log.md"]
qa = docs["docs/00-charter/04-open-questions.md"]
rd = docs["README.md"]

# ------------------------------------------------- 1. فهرست صفحات = ۹۶
rows = re.findall(r"^\| ((?:S|V|R|C|M|Q|E|B)\d\d) \|.*?\| (P[123]) \|", inv, re.M)
prio = collections.Counter(p for _, p in rows)
inv_ids = {i for i, _ in rows}
got = (len(rows), prio["P1"], prio["P2"], prio["P3"])
check("[1] فهرست صفحات ۹۶ = ۳۰/۳۰/۳۶", got == (96, 30, 30, 36), str(got))

# ------------------------------------------------- 2. موج‌ها
parts = re.split(r"^### .*موج\s+([\d۰-۹]+)", plan, flags=re.M)
waves = {
    int(fa(parts[i])): re.findall(r"^\| *[^|]*\| ((?:S|V|R|C|M|Q|E|B)\d\d)\b", parts[i + 1], re.M)
    for i in range(1, len(parts), 2)
}
alloc = [x for w in sorted(waves) for x in waves[w]]
hdrs = {
    int(fa(m.group(1))): int(fa(m.group(2)))
    for m in re.finditer(r"^### .*موج\s+([\d۰-۹]+).*?\(([\d۰-۹]+)\s", plan, re.M)
}
ok = (
    len(alloc) == 96
    and set(alloc) == inv_ids
    and len(alloc) == len(set(alloc))
    and all(hdrs.get(w) == len(waves[w]) for w in waves)
    and len(waves) == 6
)
check("[2] موج‌ها ۱:۱ با فهرست صفحات", ok, str([len(waves[w]) for w in sorted(waves)]))

# ------------------------------------------------- 3. نقشهٔ راه
st = {
    int(fa(n)): s
    for s, n in re.findall(r"^\| ([⬜✅⛔🔶🚪🔄]) *([\d۰-۹]+) \|", mp, re.M)
}
nums = sorted(st)
check("[3] نقشهٔ راه ۲۸۵ گام یکتا بدون شکاف", nums == list(range(1, 286)), f"n={len(nums)}")

# ------------------------------------------------- 4/5. داشبورد
cnt = collections.Counter(st.values())
# عددِ هر ردیف داشبورد را از خود جدول بخوان و با چک‌باکس‌ها بسنج
# ردیف‌های صفر (مثل 🚪 وقتی دروازه‌ای باز نیست) مجازند
dash = {
    m.group(1): int(m.group(2))
    for m in re.finditer(r"^\| ([✅🔄🔶⛔🚪⬜]) [^|]+\| (\d+) \|", mp, re.M)
}
mismatch = {k: (v, cnt.get(k, 0)) for k, v in dash.items() if v != cnt.get(k, 0)}
check(
    "[4] داشبورد با چک‌باکس‌ها می‌خواند",
    not mismatch and {k for k, v in dash.items() if v} == set(cnt) and sum(cnt.values()) == 285,
    f"{dict(cnt)} · mismatch={mismatch}",
)

# ------------------------------------------------- 6/7. لینک‌ها
bad = [
    f"{f}->{u}"
    for f, t in docs.items()
    if f.startswith("docs/")
    for u in re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", t)
    if not u.startswith(("http", "mailto:", "tel:"))
    and u.endswith((".md", ".yaml"))
    and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), u)))
]
check("[5] لینک‌های نسبی docs/ سالم", not bad, str(bad[:3]))

rbad = [
    u
    for u in re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", rd)
    if not u.startswith(("http", "mailto:", "tel:")) and not os.path.exists(u)
]
check("[6] لینک‌های README ریشه سالم", not rbad, str(rbad[:3]))

# ------------------------------------------------- 8. YAML
yb = []
for y in glob.glob("docs/**/*.yaml", recursive=True):
    try:
        yaml.safe_load(open(y, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        yb.append(f"{y}: {str(e)[:50]}")
check("[7] YAML پارس می‌شود", not yb, str(yb))

# ------------------------------------------------- 9. JSON-LD
jb, tot = [], 0
for f, t in docs.items():
    for b in re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', t, re.S):
        tot += 1
        try:
            json.loads(b)
        except Exception as e:  # noqa: BLE001
            jb.append(f"{f}: {str(e)[:40]}")
check("[8] JSON-LD پارس می‌شود", not jb, f"{tot} بلوک {jb[:2]}")

# ------------------------------------------------- 10. CJK
cjk = [
    (f, ch)
    for f, t in docs.items()
    for ch in set(t)
    if (0x4E00 <= ord(ch) <= 0x9FFF) or (0x3040 <= ord(ch) <= 0x30FF) or (0xAC00 <= ord(ch) <= 0xD7AF)
]
check("[9] بدون نویسهٔ CJK", not cjk, str(cjk[:3]))

# ------------------------------------------------- 11. ارجاع‌های بیات
NEG = ("❌", "ممنوع", "به‌جای", "نباید", "رد شد", "حذف", "⛔", "~~")


def stale(pat: str, skip_qa: bool = True) -> list[str]:
    out = []
    for f, t in docs.items():
        if skip_qa and f == "docs/00-charter/04-open-questions.md":
            continue
        for i, l in enumerate(t.split("\n"), 1):
            if re.search(pat, l) and not any(n in l for n in NEG):
                out.append(f"{f}:{i}")
    return out


for name, pat in [
    ("اسلاگ خدمات سیار", r"makanik-sayyar|batri-be-batri-delijan|panchergiri-sayyar|soukht-resani-sayyar|ghofl-o-suich"),
    ("/tarakhes/", r"/tarakhes/"),
    ("info@", r"info@sos-delijan\.ir"),
    ('"streetAddress"', r'"streetAddress"'),
    ('"email":', r'"email":'),
    ("۹۱ صفحه", r"۹۱ صفحه"),
    ("شمارهٔ placeholder", r"۰۹۱۲ ۰۰۰ ۰۰۰۰"),
]:
    h = stale(pat)
    check(f"[10] بیات نبودن «{name}»", not h, str(h[:3]))

# ------------------------------------------------- 12. ارقام در کد
EXEC = {"json", "html", "css", "php", "bash", "sh", "shell", "yaml",
        "javascript", "js", "apache", "htaccess", "sql", "nginx", "xml"}
pd = []
for f in glob.glob("docs/**/*.md", recursive=True):
    for m in re.finditer(r"```([a-zA-Z0-9]*)\n(.*?)```", open(f, encoding="utf-8").read(), re.S):
        if m.group(1).strip().lower() not in EXEC:
            continue
        for ln, line in enumerate(m.group(2).split("\n"), 1):
            if "grep -rnP" in line:
                continue
            if re.search(r"[۰-۹٠-٩]", line):
                pd.append(f"{f}:{ln}")
check("[11] بدون رقم فارسی در بلوک کد اجرایی", not pd, str(pd[:3]))

# ------------------------------------------------- 13. زمان رسیدن
wrong = [
    f"{f}:{i}"
    for f, t in docs.items()
    for i, l in enumerate(t.split("\n"), 1)
    if re.search(r"زیر ۳۰ دقیقه|زیر 30 دقیقه", l) and not any(n in l for n in NEG)
]
check("[12] زمان رسیدن ۱۰–۲۰ / ۲۵–۴۵", not wrong, str(wrong[:3]))

# ------------------------------------------------- 14. پرسش و پاسخ
qs = sorted({int(m) for m in re.findall(r"Q-(\d\d)", qa)})
check("[13] Q-01..Q-36 پوشش داده شد", qs == list(range(1, 37)), f"n={len(qs)}")

# ------------------------------------------------- 15. تصمیم‌ها
ds = sorted({int(m) for m in re.findall(r"^### D-(\d{3}) —", dec, re.M)})
xs = sorted({int(m) for m in re.findall(r"\|\s+\**X-(\d{3})\**\s+\|", dec)})
check("[14] D-001..D-026 · X-001..X-012", ds == list(range(1, 27)) and xs == list(range(1, 13)),
      f"D={len(ds)} X={len(xs)}")

# ------------------------------------------------- 16. NAP ↔ فهرست
nap = yaml.safe_load(open("docs/05-content/nap-master.yaml", encoding="utf-8"))
sr = {x["slug"] for x in nap["routes"]}
ir = set(re.findall(r"/جاده/([^/`]+)/", inv))
check("[15] محورهای NAP == صفحات جاده‌ای", sr == ir, f"{len(sr)} vs {len(ir)}")

# ------------------------------------------------- 17. نوارهای README
ranges = {0: (1, 22), 1: (23, 40), 2: (41, 68), 3: (69, 82), 4: (83, 108),
          5: (109, 138), 6: (139, 172), 7: (173, 194), 8: (195, 228)}
bar_ok = True
for key, bar, dn, dt in re.findall(r"^مرحله\s+(\S+)\s+\S+.*?([█░]+)\s+(\d+) از (\d+)", rd, re.M):
    d_, t_ = int(dn), int(dt)
    k = int(key.split("-")[0])
    if k in ranges:
        a, b = ranges[k]
        rd_ = sum(1 for i in range(a, b + 1) if st.get(i) == "✅")
        rt = b - a + 1
    else:
        rd_ = sum(1 for i in range(229, 286) if st.get(i) == "✅")
        rt = 57
    bar_ok &= d_ == rd_ and t_ == rt and len(bar) == 20 and bar.count("█") == round(rd_ / rt * 20)
check("[16] نوارهای پیشرفت README درست‌اند", bar_ok)

# ------------------------------------------------- 18–21. پوشش RTL
allmd = sorted(glob.glob("**/*.md", recursive=True))
wbad = []
for f in allmd:
    t = open(f, encoding="utf-8").read()
    if t.count(OPEN_TAG) != 1 or t.count("</div>") != 1:
        wbad.append(f)
        continue
    if t.startswith("---\n"):
        m = re.match(r"^---\n.*?\n---\n", t, re.S)
        if not (m and t[m.end():].startswith(OPEN_TAG + "\n\n")):
            wbad.append(f)
    elif not t.startswith(OPEN_TAG + "\n\n"):
        wbad.append(f)
    if not t.endswith("\n\n</div>\n"):
        wbad.append(f)
check(f"[17] هر {len(allmd)} فایل .md یک بار wrap شده", not wbad, str(wbad[:3]))
check("[18] تعداد فایل .md هنوز ۳۸", len(allmd) == 38, f"actual={len(allmd)}")

yt = open("docs/05-content/nap-master.yaml", encoding="utf-8").read()
check(
    "[19] nap-master.yaml پوشانده نشده و پارس می‌شود",
    OPEN_TAG not in yt and "</div>" not in yt and len(nap) >= 15 and len(nap["routes"]) == 18,
    f"{len(nap)} کلید، {len(nap['routes'])} محور",
)

fmn = sum(1 for f in allmd if open(f, encoding="utf-8").read().startswith("---\n"))
check("[20] ۳۶ فایل front matter دارند", fmn == 36, f"actual={fmn}")

fb = [f for f in allmd if open(f, encoding="utf-8").read().count("```") % 2 != 0]
check("[21] code fence ها جفت‌اند", not fb, str(fb[:3]))

# ------------------------------------------------- 22. پیام‌رسان حذف شده
NEG2 = ("⛔", "~~", "حذف", "نباشد", "نیست", "ندارد", "N/A", "رد شد", "خالی", "بازنگری", "بدون")
ms = []
for f, t in docs.items():
    if "04-open-questions" in f or "03-decisions-log" in f:
        continue
    for i, l in enumerate(t.split("\n"), 1):
        if re.search(r"واتساپ|واتس‌اپ|whatsapp|wa\.me|ایتا|eitaa|ble\.ir|بله\s*\(پیام‌رسان\)|تلگرام|telegram|سروش|روبیکا", l) \
                and not any(n in l for n in NEG2):
            ms.append(f"{f}:{i}")
check("[22] ارجاع فعال به پیام‌رسان نمانده (D-024)", not ms, str(ms[:4]))

# ------------------------------------------------- 23. شمارهٔ تماس
alltext = " ".join(docs.values())
check("[23] شمارهٔ واقعی در هر دو قالب",
      "0910 050 4113" in alltext and "+989100504113" in alltext)

# ------------------------------------------------- 24. آدرس‌های فارسی (D-025)
umap = yaml.safe_load(open("docs/05-content/url-map.yaml", encoding="utf-8"))
n_map = sum(len(umap[g]) for g in ("structural", "services", "roads", "cities_delijan",
                                   "cities_markazi", "cities_qom", "cities_esfahan", "blog"))
check("[24] url-map.yaml هر ۹۶ آدرس را دارد", n_map == 96, f"n={n_map}")

# هر آدرس فهرست صفحات باید فارسی باشد (بدون اسلاگ لاتین)
latin_urls = re.findall(r"`(/[a-z0-9][a-z0-9/-]*/)`", inv)
latin_urls = [u for u in latin_urls if u != "/"]
check("[25] هیچ آدرس لاتینی در فهرست صفحات نمانده", not latin_urls, str(latin_urls[:4]))

# همهٔ آدرس‌های new در url-map باید با فهرست صفحات بخوانند
new_urls = {v["new"] for g in ("services", "roads", "cities_delijan", "cities_markazi",
                               "cities_qom", "cities_esfahan", "structural")
            for v in umap[g].values() if v["new"].startswith("/")}
inv_urls = {u for u in re.findall(r"`(/[^`]*/)`", inv)} | {"/"}
missing = sorted(u for u in new_urls if u not in inv_urls)
check("[26] url-map ↔ فهرست صفحات هم‌خوان‌اند", not missing, str(missing[:4]))

# نیم‌فاصله در اسلاگ ممنوع
zwnj = [f"{f}:{i}" for f, t in docs.items()
        for i, l in enumerate(t.split("\n"), 1)
        for m in re.finditer(r"`(/[^`]*)`", l) if "\u200c" in m.group(1)]
check("[27] نیم‌فاصله در هیچ اسلاگی نیست", not zwnj, str(zwnj[:4]))

# ------------------------------------- 28. placeholder و ادعای ممنوع در محتوای سایت
NEG = ("⛔", "~~", "حذف", "بدون", "N/A", "بازنگری", "placeholder", "نباید", "نه ", "غلط")
ph_hits = []
for f, t in docs.items():
    if f.endswith("04-open-questions.md"):
        continue
    for i, l in enumerate(t.split("\n"), 1):
        if any(w in l for w in NEG):
            continue
        # الگوهای عنوان با {متغیر} و سطرهای مقایسه‌ای «درست/غلط» مجازند
        if "{" in l and "}" in l:
            continue
        if "0910 050 4113" in l:      # سطر مقایسهٔ قالب درست با قالب غلط
            continue
        for pat, why in (("[برند]", "placeholder برند"),
                         ("+989120000000", "شمارهٔ placeholder"),
                         ("09120000000", "شمارهٔ placeholder")):
            if pat in l:
                ph_hits.append(f"{f}:{i} {why}")
check("[28] placeholder در محتوای سایت نمانده", not ph_hits, str(ph_hits[:4]))

# ------------------------------------- 29. NAP داخل md == nap-master.yaml
nap = yaml.safe_load(open("docs/05-content/nap-master.yaml", encoding="utf-8"))
loc = docs["docs/04-seo/05-local-seo-and-nap.md"]
a = loc.find("```yaml")
a = loc.find("\n", a) + 1
b = loc.find("```", a)
nap_block = loc[a:b]
nap_y = yaml.safe_load(nap_block)
same = []
same.append(("تلفن", nap_y["phone"]["primary"]["e164"] == nap["phone"]["primary"]["e164"]))
same.append(("آدرس", nap_y["address"]["street"] is None and nap["address"]["street"] is None))
same.append(("نرخ", nap_y["price_range"] is None))
bad = [k for k, ok in same if not ok]
check("[29] NAP در md با nap-master.yaml هم‌خوان است", not bad, f"n={len(same)} بد={bad}")

# ------------------------------------- 30. تأیید مستندات (گام ۳۹)
appr = sum(1 for f in allmd if "approved: 1405-06-25" in open(f, encoding="utf-8").read()[:400])
fm_files = [f for f in allmd if open(f, encoding="utf-8").read().startswith("---\n")]
draft = [f for f in fm_files if "status: draft" in open(f, encoding="utf-8").read()[:400]]
check("[30] همهٔ مستندات status: approved دارند (گام ۳۹)",
      not draft and appr == len(fm_files), f"approved={appr}/{len(fm_files)} draft={len(draft)}")

# ---------------------------------------------------------------- report
print("=" * 78)
for o in oks:
    print(" PASS ", o)
print("-" * 78)
for x in fails:
    print(" FAIL ", x)
print("=" * 78)
print(f"{len(oks)} PASS · {len(fails)} FAIL")
print("RESULT:", "ALL PASS ✅" if not fails else "FAILED ❌")
sys.exit(0 if not fails else 1)
