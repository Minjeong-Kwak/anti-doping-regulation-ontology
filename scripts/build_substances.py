# -*- coding: utf-8 -*-
"""
Generates doping-ontology-substances.ttl and reports/substance-extraction-report.md

Extraction protocol
  1. Names are taken from the alphabetical index of the 2026 Prohibited List
     (pages 21-25), which lists every substance with the page on which it appears.
     The index is used rather than the body because the body is typeset in two to
     four columns whose continuation lines overlap the horizontal span of the
     neighbouring column, so column-aware parsing of the body interleaves names.
  2. Line-break artefacts are repaired: a hyphen followed by a space, and a comma
     followed by a space and a digit, are rejoined.
  3. Entries that still show signs of corruption are excluded and listed in the
     report for manual entry. Nothing is guessed.
  4. The page number fixes the category. Four pages carry two subcategories; for
     those, the vertical position of the name in the body is compared with the
     vertical position of the subsection headings.
  5. Names the body match could not locate are resolved from a manual table whose
     entries were each checked against the printed List.

Run from the directory holding the PDF path configured below.
"""
import pdfplumber, re, json, collections, unicodedata, os, sys

PDF = sys.argv[1] if len(sys.argv) > 1 else "2026list_en_final_clean_september_2025.pdf"
OUT_TTL = "doping-ontology-substances.ttl"
OUT_REPORT = os.path.join("reports", "substance-extraction-report.md")

INDEX_PAGES = range(20, 25)
INDEX_COLS = [(110, 274), (274, 431), (431, 600)]

# page of the 2026 List -> category, for pages carrying a single subcategory
PAGE_CAT = {4:"S0", 5:"S1_1", 7:"S2_1", 9:"S3", 12:"S5",
            15:"S6_A", 16:"S6_B", 17:"S7", 18:"S8", 19:"S9", 20:"P1"}
# pages carrying two subcategories: (heading y, category), ascending
AMBIGUOUS = {6:[(116,"S1_1"),(574,"S1_2")],
             8:[(182,"S2_2"),(540,"S2_3")],
             10:[(266,"S4_1"),(492,"S4_2")],
             11:[(152,"S4_3"),(364,"S4_4")]}
# method pages: index terms here name methods and procedures, not substances
METHOD_PAGES = {13, 14}

# names the body match cannot locate, each checked against the printed List
MANUAL = {"Gestrinone":"S1_1", "Oxandrolone":"S1_1", "Stanozolol":"S1_1",
          "hGH 176-191":"S2_2"}

SUBSTANCES_OF_ABUSE = {"cocaine", "diamorphine", "methylenedioxymethamphetamine",
                       "tetrahydrocannabinol"}

# Urinary thresholds stated in the 2026 List. The unit and the matrix are carried
# as designations, not as strings: the sources spell the same unit in more than one
# way, and a threshold is comparable with a measured value only in the same matrix.
# The designation individuals are emitted by build_designations.py.
THRESHOLDS = [
 ("Cathine",         5,    "MicrogramPerMillilitre", "Urine", "Entry_2026_S6_B"),
 ("Ephedrine",       10,   "MicrogramPerMillilitre", "Urine", "Entry_2026_S6_B"),
 ("Methylephedrine", 10,   "MicrogramPerMillilitre", "Urine", "Entry_2026_S6_B"),
 ("Pseudoephedrine", 150,  "MicrogramPerMillilitre", "Urine", "Entry_2026_S6_B"),
 ("Salbutamol",      1000, "NanogramPerMillilitre",  "Urine", "Entry_2026_S3"),
 ("Formoterol",      40,   "NanogramPerMillilitre",  "Urine", "Entry_2026_S3"),
]
UNIT_LABEL = {"MicrogramPerMillilitre":"microgram per millilitre",
              "NanogramPerMillilitre":"nanogram per millilitre"}
MATRIX_LABEL = {"Urine":"urine"}

def norm(s):
    s = unicodedata.normalize("NFKD", s).lower()
    return re.sub(r"[^a-z0-9]", "", s)


# The List states the competition context in the running header of each section,
# and states it once for the whole section rather than per substance. The mapping
# below reproduces those headers verbatim.
CONTEXT_BY_SECTION = {
 "S0": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "S1": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "S2": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "S3": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "S4": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "S5": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "M1": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "M2": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "M3": ("Context_AtAllTimes",      "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)"),
 "S6": ("Context_InCompetition",   "PROHIBITED IN-COMPETITION"),
 "S7": ("Context_InCompetition",   "PROHIBITED IN-COMPETITION"),
 "S8": ("Context_InCompetition",   "PROHIBITED IN-COMPETITION"),
 "S9": ("Context_InCompetition",   "PROHIBITED IN-COMPETITION"),
 "P1": ("Context_InParticularSports", "PROHIBITED IN PARTICULAR SPORTS"),
}

# Section S9 confines the prohibition to stated routes. The List states this once
# for the whole class, so every substance of the class carries the same routes.
ROUTES_BY_SECTION = {
 "S9": (["Route_Injectable", "Route_Oral", "Route_Oromucosal", "Route_Rectal"],
        "All glucocorticoids are prohibited when administered by any injectable, oral "
        "[including oromucosal (e.g. buccal, gingival, sublingual)] or rectal route."),
}

def section_of(cat):
    """The section a category slug belongs to: S1_1 -> S1, S6_B -> S6."""
    return cat.split("_")[0]

# The List writes stereochemistry with two characters that are not Latin letters:
# U+0251 for alpha and U+00DF for beta. Stripping them, as an accent-folding
# normalisation does, makes 7alpha-Hydroxy-DHEA and 7beta-Hydroxy-DHEA into one
# identifier and silently loses a substance. They are transliterated instead.
STEREO = {"\u0251": "alpha", "\u00df": "beta"}

def slug(s):
    for ch, word in STEREO.items():
        s = s.replace(ch, word)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s or "unnamed"

def repair(n):
    n = re.sub(r"(?<=\S)-\s+(?=[a-z\[\(])", "-", n)      # hyphen line break
    n = re.sub(r"(?<=\S)-\s+(?=[A-Z]-)", "-", n)          # locant prefix after break
    n = re.sub(r"(?<=\S)-\s+(?=[A-Z][a-z])", "-", n)      # word continued after break
    n = re.sub(r",\s+(?=\d+(?:[a-z\u00df\u0251]|-[a-z]|,))", ",", n)  # locant line break
    return re.sub(r"\s+", " ", n).strip()

def defects(n):
    d = []
    if re.match(r"^[\)\]]", n): d.append("starts mid-word")
    elif re.match(r"^[a-z]", n) and not re.match(r"^(?:[a-z]-[A-Za-z0-9]|h[A-Z])", n):
        d.append("starts mid-word")
    if n.endswith((",", "-", "[", "(")): d.append("truncated")
    if re.search(r"-\s", n): d.append("unrepaired line break")
    if re.search(r",\s+[A-Z(\[]", n) or re.search(r",\s+\d+-[A-Z]", n): d.append("two names merged")
    if re.match(r"^[\d\s]+$", n): d.append("digits only")
    if len(n) > 75: d.append("overlong")
    return d

def read_index(pdf):
    out = []
    for pi in INDEX_PAGES:
        p = pdf.pages[pi]
        for lo, hi in INDEX_COLS:
            ws = [w for w in p.extract_words() if lo <= w["x0"] < hi]
            lines = collections.defaultdict(list)
            for w in ws:
                lines[round(w["top"] / 2) * 2].append(w)
            text = " ".join(
                " ".join(x["text"] for x in sorted(lines[k], key=lambda a: a["x0"]))
                for k in sorted(lines))
            text = re.sub(r"^INDEX\s*", "", text).strip()
            # a substance may be indexed against several pages, e.g. "Salbutamol, 9, 12";
            # the first page is the class it belongs to, later ones are cross references
            parts = re.split(r",\s(\d{1,2}(?:,\s*\d{1,2})*)(?=\s|$)", text)
            i = 0
            while i + 1 < len(parts):
                name = parts[i].strip()
                pages = [int(x) for x in re.findall(r"\d{1,2}", parts[i + 1])]
                page = pages[0]
                if 4 <= page <= 20:
                    name = re.sub(r"^[A-Z]\s+(?=[A-Z0-9(\[])", "", name).strip()
                    if name:
                        out.append((re.sub(r"\s+", " ", name), page))
                    i += 2
                else:
                    if i + 2 < len(parts):
                        parts[i + 2] = parts[i] + ", " + parts[i + 1] + parts[i + 2]
                    i += 2
    return out

def resolve_ambiguous(pdf):
    table = {}
    for pg, heads in AMBIGUOUS.items():
        ws = pdf.pages[pg - 1].extract_words()
        table[pg] = ([(norm(w["text"]), w["top"]) for w in ws if norm(w["text"])], heads)
    return table

missing_context = []

def main():
    with pdfplumber.open(PDF) as pdf:
        raw = read_index(pdf)
        amb = resolve_ambiguous(pdf)

        total = len(raw)
        substances, excluded, method_terms, unresolved = [], [], [], []

        for name0, page in raw:
            name = repair(name0)
            if page in METHOD_PAGES:
                method_terms.append((name, page)); continue
            d = defects(name)
            if d:
                excluded.append((name0, page, d)); continue
            if page in PAGE_CAT:
                cat = PAGE_CAT[page]
            elif name in MANUAL:
                cat = MANUAL[name]
            else:
                toks, heads = amb[page]
                key = norm(name.split("(")[0])[:14] or norm(name)[:14]
                ys = [y for k, y in toks if len(key) >= 8 and k.startswith(key[:8])] \
                     or [y for k, y in toks if key and k.startswith(key[:5])]
                if not ys:
                    unresolved.append((name, page)); continue
                y = min(ys); cat = heads[0][1]
                for hy, hc in heads:
                    if y >= hy: cat = hc
            substances.append((name, page, cat))

    # One identifier per substance. A name repeated in the index is the same
    # substance and is kept as an alternative spelling; two different names that
    # fall on the same identifier are two substances the identifier cannot tell
    # apart, and that is an error rather than a duplicate, so it is reported.
    byslug = collections.OrderedDict()
    collisions = []
    for name, page, cat in substances:
        s = slug(name)
        byslug.setdefault(s, {"name": name, "page": page, "cat": cat, "alt": []})
        if byslug[s]["name"] != name:
            if name.lower() == byslug[s]["name"].lower():
                byslug[s]["alt"].append(name)
            else:
                collisions.append((s, byslug[s]["name"], name))
    if collisions:
        print("IDENTIFIER COLLISIONS, two names on one identifier:")
        for s_, a, b in collisions:
            print(f"  {s_}: {a!r} and {b!r}")
        raise SystemExit("refusing to write a file in which two substances share an identifier")

    o = []
    w = o.append
    w("""@prefix adro: <https://w3id.org/adro/> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/adro/substances> a owl:Ontology ;
    owl:imports <https://w3id.org/adro/designations> ;
    dcterms:title "Anti-Doping Regulation Ontology: substances of the 2026 Prohibited List"@en ;
    rdfs:comment "Generated by scripts/build_substances.py. Every substance is linked to a category by a prohibition applicability that cites the List entry it derives from. See reports/substance-extraction-report.md for the extraction protocol and the excluded entries."@en .

""")
    for s, rec in byslug.items():
        esc = rec["name"].replace('"', '\\"')
        w(f'adro:Substance_{s} a adro:ChemicalSubstance ;\n    rdfs:label "{esc}"@en')
        for a in dict.fromkeys(rec["alt"]):
            w(f' ;\n    rdfs:label "{a.replace(chr(34), chr(92)+chr(34))}"@en')
        if norm(rec["name"]).startswith(tuple(norm(x) for x in SUBSTANCES_OF_ABUSE)):
            w(' ;\n    rdfs:comment "Designated a Substance of Abuse under Code Article 4.2.3."@en')
        w(" .\n\n")
        sec = section_of(rec["cat"])
        w(f"""adro:App_2026_{s} a adro:ProhibitionApplicability ;
    rdfs:label "applicability of {esc} under the 2026 Prohibited List"@en ;
    adro:appliesTo adro:Substance_{s} ;
    adro:hasCategory adro:Category_{rec['cat']} ;
    adro:statedIn adro:Entry_2026_{rec['cat']} ;
    adro:validFrom "2026-01-01T00:00:00"^^xsd:dateTime ;
    adro:validTo   "2026-12-31T00:00:00"^^xsd:dateTime""")
        ctx = CONTEXT_BY_SECTION.get(sec)
        if ctx:
            w(f' ;\n    adro:competitionContext adro:{ctx[0]}')
            w(f' ;\n    rdfs:comment "Context as stated in the running header of section {sec}: {ctx[1]}"@en')
        else:
            missing_context.append(rec["name"])
        rts = ROUTES_BY_SECTION.get(sec)
        if rts:
            for r in rts[0]:
                w(f' ;\n    adro:routeOfAdministration adro:{r}')
            w(f' ;\n    rdfs:comment "Routes as stated for section {sec}: {rts[1]}"@en')
        w(" .\n\n")

    if missing_context:
        print("no context for", len(missing_context), "substances:", missing_context[:10])
    w("# Urinary decision limits stated in the 2026 Prohibited List.\n\n")
    for nm, val, unit, matrix, entry in THRESHOLDS:
        s = slug(nm)
        w(f"""adro:DecisionLimit_2026_{s} a adro:DecisionLimit ;
    rdfs:label "reporting threshold for {nm} in {MATRIX_LABEL[matrix]}, 2026 Prohibited List"@en ;
    adro:hasThresholdValue "{val}"^^xsd:decimal ;
    adro:hasMeasurementUnit adro:Unit_{unit} ;
    adro:hasSpecimenMatrix adro:Matrix_{matrix} ;
    obo:IAO_0000119 "WADA, The 2026 Prohibited List (International Standard), section {entry.replace('Entry_2026_','').replace('_','.')}" .

""")
        if s in byslug:
            w(f"adro:App_2026_{s} adro:hasDecisionLimit adro:DecisionLimit_2026_{s} .\n\n")

    open(OUT_TTL, "w", encoding="utf-8").write("".join(o))

    os.makedirs("reports", exist_ok=True)
    r = []
    r.append("# Substance extraction report\n")
    r.append("Source: WADA, The 2026 Prohibited List (International Standard), effective 1 January 2026.\n")
    r.append("Generated by `scripts/build_substances.py`.\n")
    r.append("\n## Counts\n")
    r.append("| stage | count |\n|---|---|\n")
    r.append(f"| index entries read | {total} |\n")
    r.append(f"| method and procedure terms (pages 13-14), not substances | {len(method_terms)} |\n")
    r.append(f"| excluded as corrupted | {len(excluded)} |\n")
    r.append(f"| subcategory unresolved | {len(unresolved)} |\n")
    r.append(f"| substances emitted | {len(byslug)} |\n")
    kept = len(byslug)
    r.append(f"\nRetention of substance-page entries: {100*kept/(total-len(method_terms)):.1f} per cent.\n")
    r.append("\n## Substances by category\n\n| category | substances |\n|---|---|\n")
    cc = collections.Counter(v["cat"] for v in byslug.values())
    for k in sorted(cc): r.append(f"| {k.replace('_','.')} | {cc[k]} |\n")
    r.append("\n## Entries excluded as corrupted\n\n")
    r.append("Each is a defect of the printed layout, not of the regulation. "
             "They are listed so that they can be entered by hand against the printed List.\n\n")
    r.append("| page | reason | text as extracted |\n|---|---|---|\n")
    for n, p, d in excluded:
        r.append(f"| {p} | {', '.join(d)} | `{n}` |\n")
    if unresolved:
        r.append("\n## Subcategory unresolved\n\n| page | name |\n|---|---|\n")
        for n, p in unresolved: r.append(f"| {p} | {n} |\n")
    r.append("\n## Method and procedure terms\n\n")
    r.append("Index terms on the method pages. These name methods, procedures or materials "
             "used in them and are not emitted as substances.\n\n")
    r.append(", ".join(n for n, _ in method_terms) + "\n")
    r.append("\n## Manual resolutions\n\n| name | category | reason |\n|---|---|---|\n")
    for n, c in MANUAL.items():
        r.append(f"| {n} | {c.replace('_','.')} | body text renders the name with intra-word spacing |\n")
    open(OUT_REPORT, "w", encoding="utf-8").write("".join(r))
    print(f"substances {len(byslug)}, excluded {len(excluded)}, method terms {len(method_terms)}, unresolved {len(unresolved)}")

main()
