# -*- coding: utf-8 -*-
"""
Maps the substances of the Prohibited List to ChEBI identifiers.

The mapping is not written by hand and is not taken from anyone's recollection.
Every identifier in the output comes from a ChEBI record obtained by this script,
and every substance falls into exactly one of three outcomes, all of them listed
in the report: matched, ambiguous, or not found.

Matching rule
-------------
A substance is matched only where its name equals a ChEBI name or synonym
exactly, ignoring case and the punctuation the two sources write differently.
Where more than one ChEBI record matches exactly, the substance is recorded as
ambiguous and nothing is asserted for it: two records that both claim the name
are a question for a chemist, not for a string comparison. A near match is never
accepted, because a wrong identifier is worse than no identifier.

Two sources of ChEBI data
-------------------------
Preferred, and deterministic:

    the ChEBI flat files `names.tsv` and `compounds.tsv`, published by the
    European Bioinformatics Institute. Download them once, then

        python3 scripts/map_external_identifiers.py \
            doping-ontology-substances.ttl \
            doping-ontology-xrefs.ttl \
            reports/external-identifier-report.md \
            --names names.tsv --compounds compounds.tsv

Fallback, where the files are not to hand and the network reaches the service:

        python3 scripts/map_external_identifiers.py \
            doping-ontology-substances.ttl \
            doping-ontology-xrefs.ttl \
            reports/external-identifier-report.md --api

The flat files are preferred because the result is then reproducible: the same
files give the same mapping on any day, and the report records which release
they came from.
"""
import argparse, collections, csv, os, re, sys, unicodedata, json, urllib.parse, urllib.request
import rdflib
from rdflib import RDF, RDFS, URIRef

NS = "https://w3id.org/adro/"

def norm(s):
    """Fold the differences the two sources write differently, and nothing else.

    Case, spaces, hyphens and the Greek and stereochemistry marks the Prohibited
    List writes with characters ChEBI spells out. Nothing that could change which
    compound is meant: digits, locants and the order of the name are untouched."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = s.replace("ɑ", "alpha").replace("ß", "beta")
    s = s.replace("α", "alpha").replace("β", "beta").replace("γ", "gamma")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)

def substances(path):
    g = rdflib.Graph(); g.parse(path, format="turtle")
    out = []
    for s in g.subjects(RDF.type, URIRef(NS + "ChemicalSubstance")):
        labels = [str(l) for l in g.objects(s, RDFS.label)]
        if labels:
            out.append((str(s).replace(NS, ""), labels))
    return sorted(out)

def index_from_files(names_tsv, compounds_tsv):
    """Build name -> {ChEBI id} from the ChEBI flat files."""
    idx = collections.defaultdict(set)
    release = []
    for path, namecol, idcol in ((names_tsv, "NAME", "COMPOUND_ID"),
                                 (compounds_tsv, "NAME", "CHEBI_ACCESSION")):
        if not path or not os.path.exists(path):
            continue
        release.append(os.path.basename(path))
        with open(path, newline="", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                nm = (row.get(namecol) or "").strip()
                cid = (row.get(idcol) or "").strip()
                if not nm or not cid:
                    continue
                if not cid.upper().startswith("CHEBI:"):
                    cid = "CHEBI:" + cid
                idx[norm(nm)].add(cid.upper())
    return idx, release

def lookup_api(name, timeout=25):
    """Ask the ChEBI service for records whose name matches exactly.

    Returns the set of identifiers whose name or synonym equals the name given.
    An empty set means the service answered and nothing matched; None means the
    service could not be reached, which is not the same thing and is reported
    differently."""
    url = ("https://www.ebi.ac.uk/webservices/chebi/2.0/test/getLiteEntity?"
           + urllib.parse.urlencode({"search": name, "searchCategory": "ALL",
                                     "maximumResults": "50", "stars": "ALL"}))
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
    except Exception:
        return None
    hits = set()
    for m in re.finditer(r"<chebiId>(CHEBI:\d+)</chebiId>\s*<chebiAsciiName>(.*?)</chebiAsciiName>",
                         body, re.S):
        if norm(m.group(2)) == norm(name):
            hits.add(m.group(1))
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("substances_ttl"); ap.add_argument("out_ttl"); ap.add_argument("out_report")
    ap.add_argument("--names"); ap.add_argument("--compounds"); ap.add_argument("--api", action="store_true")
    a = ap.parse_args()

    subs = substances(a.substances_ttl)
    idx, release = ({}, [])
    if a.names or a.compounds:
        idx, release = index_from_files(a.names, a.compounds)
    elif not a.api:
        sys.exit("give --names and --compounds, or --api")

    matched, ambiguous, absent, unreachable = [], [], [], []
    for local, labels in subs:
        hits = set()
        reached = True
        for lab in labels:
            if idx:
                hits |= idx.get(norm(lab), set())
            else:
                h = lookup_api(lab)
                if h is None:
                    reached = False
                else:
                    hits |= h
        if not reached and not hits:
            unreachable.append((local, labels[0])); continue
        if len(hits) == 1:
            matched.append((local, labels[0], hits.pop()))
        elif len(hits) > 1:
            ambiguous.append((local, labels[0], sorted(hits)))
        else:
            absent.append((local, labels[0]))

    src = ("the ChEBI flat files " + ", ".join(release)) if release else "the ChEBI web service"
    o = ["""@prefix adro: <https://w3id.org/adro/> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/adro/xrefs> a owl:Ontology ;
    owl:imports <https://w3id.org/adro/substances> ;
    dcterms:title "Anti-Doping Regulation Ontology: identifiers in external resources"@en ;
    rdfs:comment "Generated by scripts/map_external_identifiers.py. An identifier is asserted only where the substance name equals a ChEBI name or synonym exactly. Where more than one record matches, nothing is asserted and the substance is listed as ambiguous in reports/external-identifier-report.md."@en .

"""]
    for local, lab, cid in matched:
        o.append(f'adro:{local} adro:hasExternalIdentifier "{cid}" ;\n'
                 f'    obo:IAO_0000119 "{src}" .\n\n')
    open(a.out_ttl, "w", encoding="utf-8").write("".join(o))

    n = len(subs)
    r = ["# Identifiers in external resources\n\n",
         f"Source: {src}.\n\n",
         "An identifier is asserted only where the substance name equals a ChEBI name or "
         "synonym exactly, ignoring case and the punctuation the two sources write "
         "differently. A near match is never accepted. Where more than one record matches "
         "exactly, nothing is asserted: two records that both claim the name are a question "
         "for a chemist, not for a string comparison.\n\n",
         "| outcome | substances |\n|---|---|\n",
         f"| matched | {len(matched)} of {n} |\n",
         f"| more than one record matched | {len(ambiguous)} |\n",
         f"| no record matched | {len(absent)} |\n"]
    if unreachable:
        r.append(f"| service could not be reached | {len(unreachable)} |\n")
    r.append("\n## Matched\n\n| substance | name | identifier |\n|---|---|---|\n")
    for local, lab, cid in matched:
        r.append(f"| `{local}` | {lab} | {cid} |\n")
    r.append("\n## More than one record matched, so nothing was asserted\n\n"
             "| substance | name | records |\n|---|---|---|\n")
    for local, lab, ids in ambiguous:
        r.append(f"| `{local}` | {lab} | {', '.join(ids)} |\n")
    r.append("\n## No record matched\n\n"
             "Most of these are class headings rather than single compounds, or names the "
             "List writes in a form the external resource does not carry.\n\n"
             "| substance | name |\n|---|---|\n")
    for local, lab in absent:
        r.append(f"| `{local}` | {lab} |\n")
    if unreachable:
        r.append("\n## The service could not be reached for these\n\n"
                 "| substance | name |\n|---|---|\n")
        for local, lab in unreachable:
            r.append(f"| `{local}` | {lab} |\n")
    open(a.out_report, "w", encoding="utf-8").write("".join(r))
    print(f"substances {n}, matched {len(matched)}, ambiguous {len(ambiguous)}, "
          f"absent {len(absent)}, unreachable {len(unreachable)}")

main()
