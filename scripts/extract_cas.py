# -*- coding: utf-8 -*-
"""
Extracts a case register from CAS award digests.

Tier 1 fields come from the fixed headnote block on the first page and are taken
as asserted: case number, award date, parties, sport, subject matter.
Tier 2 fields (rule provision, sanction) are collected as candidates only and are
never asserted without verification, because their wording varies between awards.
"""
import pdfplumber, re, os, sys, json, glob, unicodedata

MONTHS = {m.lower(): i+1 for i, m in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"])}
MOIS = {m: i+1 for i, m in enumerate(
    ["janvier","février","mars","avril","mai","juin","juillet","août",
     "septembre","octobre","novembre","décembre"])}

CASE = re.compile(
    r'\b(CAS|TAS)\s+(?:ad hoc Division \(OG [A-Za-z ]+\)\s*)?'
    r'(\d{4}/[A-Z]/\d+|\(Oceania [Rr]egistry\)\s*[A-Z]\d/\d{4}|OG\s*\d{2}/\d{3}|\d{2}/\d{3}|[A-Z]\d/\d{4})')
DATE = re.compile(r'(?:award of|sentence du|sentence rendue le)\s+(\d{1,2})(?:er)?\s+([A-Za-zéûî]+)\s+(\d{4})', re.I)
PANEL = re.compile(r'^(Panel|Formation)\s*:')
# An arbitrator line ends with the arbitrator's country in parentheses. The last
# line of the panel block may close with a full stop, so the stop is allowed here;
# without it the closing line of a two-line panel block is read as the sport.
ARBIT = re.compile(r'\((?:[A-Z][A-Za-zÀ-ÿ .\-]+)\)\s*[;,.]?\s*$')
DOPING = re.compile(r'^(?:Doping|Dopage)\s*\((.*)\)\s*$')
# Some awards state no sport and go straight to the subject line. A bare subject
# line must not be taken as the name of a sport.
DOPING_BARE = re.compile(r'^(?:Doping|Dopage)\s*$')

def iso(d, mon, y):
    m = MONTHS.get(mon.lower()) or MOIS.get(mon.lower())
    return f"{y}-{m:02d}-{int(d):02d}T00:00:00" if m else None

def extract(path):
    with pdfplumber.open(path) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    first, full = pages[0], "\n".join(pages)
    lines = [l.strip() for l in first.split("\n") if l.strip()]
    lines = [l for l in lines if not l.startswith("Tribunal Arbitral du Sport")]

    pi = next((i for i, l in enumerate(lines) if PANEL.match(l)), None)
    header = " ".join(lines[:pi]) if pi is not None else " ".join(lines[:4])

    cases = []
    adhoc = 'ad hoc Division' in header
    for a, b in CASE.findall(header):
        b = b.strip()
        if re.fullmatch(r'\d{2}/\d{3}', b):
            b = 'OG ' + b if adhoc else b
        cases.append(f"{a} {b}")
    m = DATE.search(header)
    date = iso(*m.groups()) if m else None

    parties = re.sub(r'^\s*(Arbitration|Arbitrage|Advisory opinion)\s+', '', header)
    parties = CASE.sub('', parties)
    parties = re.split(r',\s*(?:award of|sentence du|sentence rendue le)', parties)[0]
    parties = re.sub(r'\s+', ' ', parties).strip(' ,&')

    # after the panel block: skip arbitrator continuation lines
    rest, j = [], (pi + 1 if pi is not None else 0)
    while j < len(lines) and (ARBIT.search(lines[j]) or ';' in lines[j]):
        j += 1
    rest = lines[j:]
    sport = (rest[0] if rest and not DOPING.match(rest[0])
             and not DOPING_BARE.match(rest[0]) else None)
    dop = next((l for l in rest[:6] if DOPING.match(l)), None)
    subject = DOPING.match(dop).group(1) if dop else None

    # tier 2 candidates, never asserted
    arts = sorted(set(re.findall(r'\bArticle\s+(2\.\d{1,2})\b', full)))
    sanction = re.findall(
        r'(?:period of ineligibility|ineligible|declared ineligible|suspension)'
        r'[^.;]{0,90}?\b(one|two|three|four|five|six|eight|lifetime|\d{1,2})\b'
        r'[\s\(\)\d]{0,6}(years?|months?|ans?|mois)', full, re.I)
    return dict(file=os.path.basename(path), pages=len(pages), cases=cases,
                award_date=date, parties=parties, sport=sport, subject=subject,
                candidate_articles=arts, candidate_sanctions=sanction[:5])

if __name__ == "__main__":
    root = sys.argv[1]
    files = sorted(os.path.join(root, x) for x in os.listdir(root) if x.lower().endswith(".pdf"))
    out = [extract(f) for f in files]
    json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    n = len(out)
    def rate(k): return sum(1 for r in out if r[k]) / n * 100
    print(f"documents {n}")
    for k in ["cases", "award_date", "parties", "sport", "subject"]:
        print(f"  {k:14s} {rate(k):5.1f}%")
    print(f"  {'articles':14s} {sum(1 for r in out if r['candidate_articles'])/n*100:5.1f}% (candidates)")
    print(f"  {'sanctions':14s} {sum(1 for r in out if r['candidate_sanctions'])/n*100:5.1f}% (candidates)")
