# -*- coding: utf-8 -*-
"""
Turns the CAS case register into ontology individuals.

Only Tier 1 fields are asserted: case identifier, award date, parties, sport,
and, where the subject line names a substance present in the Prohibited List
layer, a link to that substance. Rule provisions and sanctions are carried as
candidates in the report and are not asserted.
"""
import json, re, sys, os, unicodedata, collections, difflib
import rdflib
from rdflib import RDF, RDFS, URIRef

NS = "https://w3id.org/adro/"

def slug(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")

def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("ph", "f")          # INN spelling: amphetamine -> amfetamine
    return re.sub(r"[^a-z0-9]", "", s)

# Abbreviations and alternative names used in the awards. Each is grounded in the
# wording of the 2026 Prohibited List unless noted.
ALIASES = {
 "thg": ("Tetrahydrogestrinone", "List S1.1 names Tetrahydrogestrinone; THG is the abbreviation used in the award"),
 "dhea": ("Prasterone", "List S1.1: Prasterone (dehydroepiandrosterone, DHEA)"),
 "epo": ("Erythropoietins (EPO)", "List S2.1 heading: Erythropoietins (EPO)"),
 "repo": ("Erythropoietins (EPO)", "recombinant erythropoietin; List S2.1"),
 "recombinantepo": ("Erythropoietins (EPO)", "List S2.1"),
 "hgh": ("Growth hormone (GH)", "List S2.2.3: Growth hormone (GH)"),
 "humangrowthhormone": ("Growth hormone (GH)", "List S2.2.3"),
 "somatotrofin": ("Growth hormone (GH)", "somatotrophin is the alternative name of growth hormone; List S2.2.3"),
 "fg4592": ("Roxadustat", "List S2.1.2: roxadustat (FG-4592)"),
 "sarm": ("Selective androgen receptor modulators (SARMs)", "List S1.2"),
 "sarms": ("Selective androgen receptor modulators (SARMs)", "List S1.2"),
 "mha": ("Methylhexaneamine", "List S6.B names Methylhexaneamine"),
 "dmba": ("1,3-Dimethylbutylamine", "List S6.B: 4-Methylpentan-2-amine (1,3-dimethylbutylamine)"),
 "thymosinbeta4": ("Thymosin-\u00df4", "List S2.3: Thymosin-\u00df4"),
}


# ---------------------------------------------------------------------------
# Sports as the headnotes write them
#
# A headnote writes the sport, and where it names a discipline it writes the
# discipline in parentheses after the sport: "Athletics (sprint)". That is the
# headnotes' own convention, so the ontology follows it: the sport is one
# designation, the discipline another, and the discipline falls under the sport
# through the transitive broaderCategory relation. A question about athletics
# then reaches the sprint cases without naming them.
#
# Beyond that convention only two kinds of variation are merged: a spelling or
# casing difference, and a name given in another language. Two strings that
# could name different sports are never merged. Rugby league stays apart from
# rugby, and wheelchair rugby from both, because they are different sports and
# not different spellings.
# ---------------------------------------------------------------------------

# headnote string (lowercased, trimmed) -> canonical sport name
SPORT_MERGE = {
 "athlétisme": "Athletics",            # French
 "athletisme": "Athletics",
 "boxe": "Boxing",                     # French
 "canoe": "Canoeing",                  # the sport is canoeing; the headnote writes both
 "table tennis": "Table tennis",       # casing only
 "paralympics shooting": "Paralympic shooting",
 "shooting sport": "Shooting",
 "cross-country skiing": "Skiing (cross-country skiing)",
}

# discipline string under a sport -> canonical discipline, where the headnotes
# write the same discipline two ways
DISCIPLINE_MERGE = {
 ("Athletics", "discus"): "discus throw",
 ("Athletics", "marathon race"): "marathon",
 ("Athletics", "middle-distance running"): "middle-distance",
}

def split_sport(raw):
    """Return (sport, discipline or None) from a headnote sport line.

    The headnote convention is "Sport (discipline)". Anything else is taken
    whole, because guessing at a division would invent one."""
    raw = re.sub(r"\s+", " ", raw).strip().rstrip(".")
    raw = SPORT_MERGE.get(raw.lower(), raw)
    m = re.fullmatch(r"([^()]+?)\s*\(([^()]+)\)", raw)
    if not m:
        return raw, None
    sport = m.group(1).strip()
    sport = SPORT_MERGE.get(sport.lower(), sport)
    disc = m.group(2).strip()
    disc = DISCIPLINE_MERGE.get((sport, disc), disc)
    return sport, disc


# ---------------------------------------------------------------------------
# Violation types named in the headnote subject line
#
# Most subject lines name the substance found. Where the matter turns on conduct
# rather than on a substance, the line names the violation itself, and that name
# is a Tier 1 statement of the headnote. Only names that identify one violation
# type are mapped; a word that could mean several things is left alone.
# ---------------------------------------------------------------------------
SUBJECT_ADRV = [
 (r"\btrafficking\b",        "ADRVType_Trafficking"),
 (r"\btamper",                "ADRVType_Tampering"),
 (r"\bcomplicit",             "ADRVType_Complicity"),
 (r"prohibited association",  "ADRVType_ProhibitedAssociation"),
 (r"refus|evad|fail(?:ure|ing)? to (?:submit|comply)", "ADRVType_EvadingRefusingFailing"),
 (r"whereabouts",             "ADRVType_WhereaboutsFailures"),
]

# Persons whom the award identifies as athlete support personnel, with the wording.
# The headnote or the opening statement of facts names the role; nothing is inferred
# from a party's name alone.
SUPPORT_PERSONNEL = {
 "CAS 2007/A/1311": ("Sevdalin_Marinov", "Sevdalin Marinov",
   "Sevdalin Marinov (the Appellant), a head coach of an Australian weightlifting team"),
 "CAS 2016/A/4700": ("Lyudmila_Fedoriva", "Lyudmila Vladimirvma Fedoriva",
   "Doping (tampering or attempted tampering with any part of doping control by a coach)"),
 "CAS 2018/A/6047": ("Andrei_Eremenko", "Andrei Valerievich Eremenko",
   "Doping (tampering/attempted tampering and complicity of coach)"),
}

def load_substances(path):
    g = rdflib.Graph(); g.parse(path, format="turtle")
    out = {}
    for s in g.subjects(RDF.type, URIRef(NS + "ChemicalSubstance")):
        for l in g.objects(s, RDFS.label):
            k = norm(str(l))
            if len(k) >= 5:
                out.setdefault(k, str(s).replace(NS, ""))
    return out

def main(register, substances_ttl, out_ttl, out_report):
    rows = json.load(open(register))
    subs = load_substances(substances_ttl)
    keys = sorted(subs, key=len, reverse=True)

    # metabolites carry their own file; load their labels too
    meta = {}
    try:
        mg = rdflib.Graph(); mg.parse("doping-ontology-analytes.ttl", format="turtle")
        for m in mg.subjects(RDF.type, URIRef(NS + "Metabolite")):
            for l in mg.objects(m, RDFS.label):
                meta[norm(str(l))] = str(m).replace(NS, "")
    except Exception:
        pass
    label_of = {}
    sg = rdflib.Graph(); sg.parse(substances_ttl, format="turtle")
    for sub in sg.subjects(RDF.type, URIRef(NS + "ChemicalSubstance")):
        for l in sg.objects(sub, RDFS.label):
            label_of[norm(str(l))] = str(sub).replace(NS, "")

    o, seen_sport, matched, unmatched = [], {}, 0, []
    alias_hits, fuzzy_hits, meta_hits, adrv_hits, asp_hits = [], [], [], [], []
    o.append("""@prefix adro: <https://w3id.org/adro/> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/adro/cases-cas> a owl:Ontology ;
    owl:imports <https://w3id.org/adro/substances> ;
    dcterms:title "Anti-Doping Regulation Ontology: Court of Arbitration for Sport case register"@en ;
    rdfs:comment "Generated by scripts/build_cases.py from award digests published by the Court of Arbitration for Sport. Case identifier, award date, parties and sport are asserted. Rule provisions and sanctions are not asserted; see reports/cas-extraction-report.md."@en .

adro:CAS a adro:Organization ;
    rdfs:label "Court of Arbitration for Sport"@en .

""")
    for r in rows:
        if not r["cases"]:
            continue
        cid = r["cases"][0]
        s = slug(cid)
        kind = ("adro:AppealDecision" if "/A/" in cid
                else "adro:FirstInstanceDecision" if "/O/" in cid
                else "adro:Decision")
        title = r["parties"].replace('"', "'")
        o.append(f'adro:Decision_{s} a {kind} ;\n')
        o.append(f'    rdfs:label "{cid}"@en ;\n')
        o.append(f'    dcterms:title "{title}"@en ;\n')
        o.append(f'    adro:issuedBy adro:CAS ;\n')
        o.append(f'    adro:hasCaseIdentifier "{cid}"')
        if r["award_date"]:
            o.append(f' ;\n    adro:hasDecisionDate "{r["award_date"]}"^^xsd:dateTime')
        # a consolidated proceeding carries more than one case number.
        # the additional numbers are further identifiers of the same decision,
        # not further labels: a second rdfs:label would leave the individual
        # with two competing display names.
        for extra in r["cases"][1:]:
            o.append(f' ;\n    adro:hasCaseIdentifier "{extra}"')
        if len(r["cases"]) > 1:
            joined = ", ".join(r["cases"])
            o.append(f' ;\n    rdfs:comment "Consolidated proceeding decided in a single award under case numbers {joined}."@en')
        # sport, split into sport and discipline by the headnote's own convention
        sp = (r["sport"] or "").strip()
        r["_sport_id"] = None
        if sp and len(sp) < 40:
            sport, disc = split_sport(sp)
            sid = "Sport_" + slug(sport)
            seen_sport.setdefault(sid, dict(label=sport, parent=None, raws=set()))
            seen_sport[sid]["raws"].add(sp)
            if disc:
                did = sid + "_" + slug(disc)
                seen_sport.setdefault(did, dict(label=f"{sport} ({disc})", parent=sid, raws=set()))
                seen_sport[did]["raws"].add(sp)
                r["_sport_id"] = did
            else:
                r["_sport_id"] = sid
        # violation type, where the subject line names one
        subj_raw = r["subject"] or ""
        for pat, adrv in SUBJECT_ADRV:
            if re.search(pat, subj_raw, re.I):
                o.append(f' ;\n    adro:assignsType adro:{adrv}')
                adrv_hits.append((cid, subj_raw, adrv))

        # substance link from the subject line
        subj = r["subject"] or ""
        hits = []          # list of (local name, how)
        if subj:
            n = norm(subj)
            phrases = [p.strip() for p in re.split(r"[;,/\u2013\u2014()\[\]]| and | et ", subj) if p.strip()]
            words = re.split(r"\s+", subj)
            pn = [norm(p) for p in phrases] + [norm(w) for w in words] + [n]
            pn = [x for x in pn if x]

            def add(local, how):
                if local and local not in [h for h, _ in hits]:
                    hits.append((local, how)); return True
                return False

            # 1 metabolites named in the corpus
            for k, v in meta.items():
                if k and any(k in x for x in pn):
                    if add(v, "metabolite"): meta_hits.append((cid, subj, v))
            # 2 abbreviations and alternative names, matched phrase by phrase
            for a, (target, why) in ALIASES.items():
                if any(x == a or re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", x)
                       for x in pn + [norm(p) for p in re.split(r"\s+", subj)]):
                    t = label_of.get(norm(target))
                    if add(t, "alias"): alias_hits.append((cid, subj, a, target, why))
            # 3 every List name that appears in the subject line
            found = [k for k in keys if k in n]
            found = [k for k in found if not any(k != j and k in j for j in found)]
            for k in found:
                add(subs[k], "name")
            # 4 near match on a phrase, only where that phrase matched nothing
            if not hits:
                pool = [k for k in keys if len(k) >= 8]
                for x in sorted(set(pn), key=len, reverse=True):
                    if len(x) < 8:
                        continue
                    cand = difflib.get_close_matches(x, pool, n=1, cutoff=0.88)
                    if cand:
                        if add(subs[cand[0]], "near"):
                            fuzzy_hits.append((cid, subj, cand[0], subs[cand[0]],
                                round(difflib.SequenceMatcher(None, x, cand[0]).ratio(), 3)))
                        break
        for h, _ in hits:
            o.append(f' ;\n    adro:mentions adro:{h}')
        if hits:
            matched += 1
        elif subj:
            unmatched.append((cid, subj))
        if subj:
            o.append(f' ;\n    rdfs:comment "Subject as stated in the award headnote: {subj.replace(chr(34), chr(39))}"@en')
        o.append(" .\n\n")

        o.append(f'adro:CaseRecord_{s} a adro:CaseRecord ;\n')
        o.append(f'    rdfs:label "case record for {cid}"@en ;\n')
        o.append(f'    obo:IAO_0000136 adro:Decision_{s} ;\n')
        o.append(f'    adro:resultsManagementAuthority adro:CAS ;\n')
        o.append(f'    adro:caseStatus adro:CaseStatus_Final ;\n')
        if sp and len(sp) < 40:
            o.append(f'    adro:concernsSport adro:{r["_sport_id"]} ;\n')
        o.append(f'    adro:hasCaseIdentifier "{cid}" .\n\n')

    # persons the awards identify as athlete support personnel
    o.append("# Persons an award identifies as athlete support personnel, with the wording.\n\n")
    for cid, (pid, pname, wording) in SUPPORT_PERSONNEL.items():
        asp_hits.append((cid, pname, wording))
        o.append(f'adro:Person_{pid} a adro:Person ;\n'
                 f'    rdfs:label "{pname}"@en ;\n'
                 f'    adro:bearerOfRole adro:SupportRole_{pid} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{slug(cid)} ;\n'
                 f'    obo:IAO_0000119 "{cid}" .\n\n')
        o.append(f'adro:SupportRole_{pid} a adro:AthleteSupportPersonnelRole ;\n'
                 f'    rdfs:label "athlete support personnel role of {pname}"@en ;\n'
                 f'    obo:IAO_0000119 "{cid}" ;\n'
                 f'    rdfs:comment "As stated in {cid}: {wording}."@en .\n\n')

    o.append("# Sports and disciplines named in the award headnotes.\n"
             "# A discipline falls under its sport through broaderCategory, which is\n"
             "# transitive, so a question about the sport reaches the discipline's cases.\n\n")
    for sid, rec in sorted(seen_sport.items()):
        o.append(f'adro:{sid} a adro:Sport ;\n'
                 f'    rdfs:label "{rec["label"]}"@en ;\n')
        if rec["parent"]:
            o.append(f'    adro:broaderCategory adro:{rec["parent"]} ;\n')
        raws = ", ".join(sorted(rec["raws"]))
        o.append(f'    rdfs:comment "As stated in the award headnotes: {raws}."@en .\n\n')

    open(out_ttl, "w", encoding="utf-8").write("".join(o))

    n = len(rows)
    os.makedirs(os.path.dirname(out_report), exist_ok=True)
    rep = ["# CAS case extraction report\n",
           "Source: award digests published by the Court of Arbitration for Sport.\n",
           "Generated by `scripts/extract_cas.py` and `scripts/build_cases.py`.\n",
           "\n## Field extraction\n\n| field | tier | rate |\n|---|---|---|\n"]
    def rate(k): return sum(1 for r in rows if r[k]) / n * 100
    for k, t in [("cases", 1), ("award_date", 1), ("parties", 1), ("sport", 1), ("subject", 1)]:
        rep.append(f"| {k} | 1 asserted | {rate(k):.1f} per cent |\n")
    rep.append(f"| rule provision | 2 candidate only | {sum(1 for r in rows if r['candidate_articles'])/n*100:.1f} per cent |\n")
    rep.append(f"| sanction | 2 candidate only | {sum(1 for r in rows if r['candidate_sanctions'])/n*100:.1f} per cent |\n")
    rep.append(f"\nDocuments processed: {n}. Substance links asserted: {matched}.\n")
    rep.append("\nTier 1 fields come from the fixed headnote block of the award digest and are asserted. "
               "Tier 2 fields vary in wording between awards and between languages; they are listed here as "
               "candidates for verification and are not asserted in the ontology.\n")
    rep.append("\n## Substance links established by an abbreviation or alternative name\n\n")
    rep.append("| case | subject as stated | term | mapped to | grounding |\n|---|---|---|---|---|\n")
    for cid, subj, a, target, why in alias_hits:
        rep.append(f"| {cid} | {subj} | {a} | {target} | {why} |\n")
    rep.append("\n## Substance links established by a near match\n\n")
    rep.append("Spelling variants in the award text. Each is listed for verification.\n\n")
    rep.append("| case | subject as stated | matched name | ratio |\n|---|---|---|---|\n")
    for cid, subj, k, sid, ratio in fuzzy_hits:
        rep.append(f"| {cid} | {subj} | {sid.replace('Substance_','')} | {ratio} |\n")
    rep.append("\n## Links to a metabolite rather than to a listed substance\n\n")
    rep.append("| case | subject as stated | metabolite |\n|---|---|---|\n")
    for cid, subj, v in meta_hits:
        rep.append(f"| {cid} | {subj} | {v.replace('Substance_','')} |\n")
    rep.append("\n## Subject lines with no matching substance\n\n")
    rep.append("Most of these name a procedural violation rather than a substance: whereabouts "
               "failures, refusal or evasion of sample collection, tampering, trafficking, "
               "prohibited association, blood manipulation, and biological passport cases. "
               "Two need a note. Finasteride was a masking agent on earlier editions of the "
               "Prohibited List and is not on the 2026 edition, which is why no applicability "
               "is found for it; this is a consequence of anchoring the substance layer to a "
               "stated edition. The androstanediols named in one award are markers of the "
               "steroid profile, and no award in the corpus states the substance they derive "
               "from, so no relation is asserted.\n\n")
    rep.append("| case | subject as stated |\n|---|---|\n")
    for cid, subj in unmatched:
        rep.append(f"| {cid} | {subj} |\n")
    rep.append("\n## Violation types asserted from the subject line\n\n"
               "Most subject lines name the substance found. Where the matter turns on conduct, "
               "the line names the violation itself, and that name is asserted. A word that "
               "could mean more than one violation type is not mapped.\n\n"
               "| case | subject as stated | violation type |\n|---|---|---|\n")
    for cid, subj, adrv in adrv_hits:
        rep.append(f"| {cid} | {subj} | {adrv.replace('ADRVType_','')} |\n")

    rep.append("\n## Persons the awards identify as athlete support personnel\n\n"
               "A support personnel role is asserted only where the award says in so many words "
               "what the person was. Nothing is read off a party's name or off the fact that a "
               "violation type is one the regulation directs at a person other than the athlete.\n\n"
               "| case | person | wording |\n|---|---|---|\n")
    for cid, pname, wording in asp_hits:
        rep.append(f"| {cid} | {pname} | {wording} |\n")
    rep.append("\nThree further awards concern prohibited association between an athlete and a "
               "coach. They state that a coach was involved without naming one, so a violation "
               "type is asserted for those matters and no person is.\n")

    rep.append("\n## Rule provision and sanction candidates\n\n")
    rep.append("| case | article candidates | sanction candidates |\n|---|---|---|\n")
    for r in rows:
        if not r["cases"]: continue
        a = ", ".join(r["candidate_articles"]) or "-"
        sset = ", ".join(f"{x} {y}" for x, y in r["candidate_sanctions"]) or "-"
        rep.append(f"| {r['cases'][0]} | {a} | {sset} |\n")
    open(out_report, "w", encoding="utf-8").write("".join(rep))
    print(f"decisions {sum(1 for r in rows if r['cases'])}, sports {len(seen_sport)}, "
          f"substance links {matched}, unmatched subjects {len(unmatched)}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
