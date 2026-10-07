# -*- coding: utf-8 -*-
"""
Generates the three documents the review asks for, from the ontology itself.

  reports/data-dictionary.md    every class and property, with its definition,
                                its placement, its domain and range, and the
                                number of individuals or assertions that use it
  reports/ontology-metrics.md   the counts and the profile a reviewer needs to
                                check reproducibility
  reports/source-manifest.md    every assertion about a case, traced to the
                                decision that states it

Written from the files rather than by hand, so that they cannot drift from what
the ontology actually contains.
"""
import os, sys, collections, rdflib
from rdflib import RDF, RDFS, OWL, URIRef, Literal

NS = "https://w3id.org/adro/"
OBO = "http://purl.obolibrary.org/obo/"
DEF = URIRef(OBO + "IAO_0000115")
SRC = URIRef(OBO + "IAO_0000119")
DCT = URIRef("http://purl.org/dc/terms/title")

MODULES = ["doping-ontology-core.ttl", "doping-ontology-designations.ttl",
           "doping-ontology-substances.ttl", "doping-ontology-analytes.ttl",
           "doping-ontology-cases-cas.ttl", "doping-ontology-cases-national.ttl",
           "doping-ontology-procedure.ttl"]

def short(u):
    s = str(u)
    return s.replace(NS, "adro:").replace(OBO, "obo:").replace(
        "http://www.w3.org/2001/XMLSchema#", "xsd:").replace(
        "http://www.w3.org/2000/01/rdf-schema#", "rdfs:")

def load(root):
    core = rdflib.Graph(); core.parse(os.path.join(root, MODULES[0]), format="turtle")
    g = rdflib.Graph()
    per = {}
    for m in MODULES:
        h = rdflib.Graph(); h.parse(os.path.join(root, m), format="turtle")
        per[m] = len(h)
        for t in h: g.add(t)
    return core, g, per

def one(g, s, p):
    for o in g.objects(s, p):
        if not isinstance(o, Literal) or o.language in (None, "en"):
            return str(o)
    return ""

def dictionary(core, g, out):
    classes = sorted([s for s in core.subjects(RDF.type, OWL.Class) if str(s).startswith(NS)], key=str)
    obj = sorted(core.subjects(RDF.type, OWL.ObjectProperty), key=str)
    dat = sorted(core.subjects(RDF.type, OWL.DatatypeProperty), key=str)
    inst = collections.Counter(str(o) for _, _, o in g.triples((None, RDF.type, None)))
    used = collections.Counter(str(p) for _, p, _ in g)
    r = ["# Data dictionary\n\n",
         "Every term the ontology declares, with its definition, where it sits under the "
         "upper ontology, and how much use it gets. Generated from the files by "
         "`scripts/build_documentation.py`, so it cannot drift from them.\n\n",
         "## Classes\n\n| class | label | placed under | individuals | definition |\n|---|---|---|---|---|\n"]
    for c in classes:
        parents = ", ".join(sorted(short(o) for o in core.objects(c, RDFS.subClassOf) if isinstance(o, URIRef)))
        r.append(f"| `{short(c)}` | {one(core,c,RDFS.label)} | {parents} | {inst.get(str(c),0)} | {one(core,c,DEF)} |\n")
    for title, props, extra in (("Object properties", obj, True), ("Data properties", dat, True)):
        r.append(f"\n## {title}\n\n| property | label | domain | range | assertions | definition |\n|---|---|---|---|---|---|\n")
        for p in props:
            dom = ", ".join(sorted(short(o) for o in core.objects(p, RDFS.domain) if isinstance(o, URIRef))) or "—"
            rng = ", ".join(sorted(short(o) for o in core.objects(p, RDFS.range) if isinstance(o, URIRef))) or "—"
            r.append(f"| `{short(p)}` | {one(core,p,RDFS.label)} | {dom} | {rng} | {used.get(str(p),0)} | {one(core,p,DEF)} |\n")
    r.append("\nA property with no domain or range has none asserted, because its subjects or "
             "values belong to more than one category. A property with no assertions is "
             "inferred rather than stated; the competency question report says which.\n")
    open(out, "w", encoding="utf-8").write("".join(r))

def dist_triples(root):
    """The count a reviewer gets by opening the merged release.

    It is lower than the sum over the modules: a triple stated in two modules is
    one triple once merged, and the release carries one ontology header in place
    of the seven the modules carry. Both figures are reported so that neither is
    quoted for the other."""
    p = os.path.join(root, "dist", "adro-full.ttl")
    if not os.path.exists(p):
        return "not built"
    h = rdflib.Graph(); h.parse(p, format="turtle")
    return len(h)

def metrics(core, g, per, root, out):
    cls = [s for s in core.subjects(RDF.type, OWL.Class) if str(s).startswith(NS)]
    obj = list(core.subjects(RDF.type, OWL.ObjectProperty))
    dat = list(core.subjects(RDF.type, OWL.DatatypeProperty))
    ind = {s for s, _, o in g.triples((None, RDF.type, None)) if str(o).startswith(NS)}
    dec = {s for s, _, o in g.triples((None, RDF.type, None))
           if str(o) in (NS+"Decision", NS+"FirstInstanceDecision", NS+"AppealDecision", NS+"TUEDecision")}
    r = ["# Ontology metrics and reproducibility\n\n",
         "Generated from the files by `scripts/build_documentation.py`.\n\n",
         "## Size\n\n| measure | count |\n|---|---|\n",
         f"| classes | {len(cls)} |\n| object properties | {len(obj)} |\n",
         f"| data properties | {len(dat)} |\n| named individuals | {len(ind)} |\n",
         f"| decisions | {len(dec)} |\n| triples, summed over the modules | {sum(per.values())} |\n",
         f"| triples, `dist/adro-full.ttl` | {dist_triples(root)} |\n",
         f"| classes with a definition | {len([c for c in cls if (c,DEF,None) in core])} of {len(cls)} |\n",
         f"| properties with a definition | {len([p for p in obj+dat if (p,DEF,None) in core])} of {len(obj)+len(dat)} |\n",
         "\n## Triples per module\n\n| module | triples |\n|---|---|\n"]
    for m, n in per.items():
        r.append(f"| `{m}` | {n} |\n")
    r.append("\nThe two totals differ. A triple stated in two modules is one triple once they are "
             "merged, and the release carries one ontology header in place of the seven the "
             "modules carry. The summed figure is what this table adds up to; the release figure "
             "is what a reviewer who opens `dist/adro-full.ttl` will count. Cite whichever is meant.\n")
    ax = dict(
        disjointness=len(list(core.subjects(RDF.type, OWL.AllDisjointClasses))),
        property_chains=len(list(core.subject_objects(OWL.propertyChainAxiom))),
        transitive=len(list(core.subjects(RDF.type, OWL.TransitiveProperty))),
        existential=len(list(core.subject_objects(OWL.someValuesFrom))),
        inverse=len(list(core.subject_objects(OWL.inverseOf))),
        subproperty=len(list(core.subject_objects(RDFS.subPropertyOf))),
        class_complement=len(list(g.subject_objects(OWL.complementOf))),
        equivalent_class=len(list(core.subject_objects(OWL.equivalentClass))),
    )
    r.append("\n## Axioms\n\n| kind | count |\n|---|---|\n")
    for k, v in ax.items():
        r.append(f"| {k.replace('_',' ')} | {v} |\n")
    r.append("\n## Profile and imports\n\n"
             "The constructs used are class and property declarations, subclass and subproperty "
             "axioms, domains and ranges, existential restrictions, equivalent-class axioms that "
             "state a necessary and sufficient condition for four classes, unions of two classes used "
             "as a domain or as a range, pairwise disjointness, inverse properties, one "
             "transitive property, two "
             "property chain axioms, one class complement on an individual, and typed data "
             "properties. These lie within OWL 2 DL. The ontology carries no cardinality "
             "restrictions, no nominals beyond one `owl:hasValue`, and no datatype outside the "
             "OWL 2 datatype map: `xsd:duration` and `xsd:date` are deliberately avoided, and "
             "periods are carried as `xsd:decimal` months and instants as `xsd:dateTime`.\n\n"
             "| imported | IRI |\n|---|---|\n"
             "| Basic Formal Ontology | `http://purl.obolibrary.org/obo/bfo.owl` |\n"
             "| Information Artifact Ontology | `http://purl.obolibrary.org/obo/iao.owl` |\n\n"
             "Both are resolved to the copies in this directory by `catalog-v001.xml`, so the "
             "set loads with no network access.\n\n"
             "## Reasoner\n\n"
             "HermiT, through owlready2, with property values inferred. The axiom suite in "
             "`tests/` loads the merged graph, runs the reasoner, and reports consistency and "
             "the entailments obtained. The competency questions are additionally run at three "
             "strengths of entailment; see `reports/competency-questions-report.md`.\n")
    open(out, "w", encoding="utf-8").write("".join(r))

def manifest(g, out):
    rows = []
    for s in sorted(set(g.subjects(SRC, None)), key=str):
        src = one(g, s, SRC)
        lab = one(g, s, RDFS.label)
        kinds = ", ".join(sorted(short(o) for o in g.objects(s, RDF.type) if str(o).startswith(NS)))
        n = len(list(g.triples((s, None, None))))
        rows.append((src, short(s), kinds, lab, n))
    dec = []
    for s in sorted(set(g.subjects(URIRef(NS+"hasCaseIdentifier"), None)), key=str):
        ident = one(g, s, URIRef(NS+"hasCaseIdentifier"))
        body = ""
        for o in g.objects(s, URIRef(NS+"issuedBy")):
            body = one(g, o, RDFS.label)
        url = one(g, s, URIRef(NS+"hasSourceURL"))
        ret = one(g, s, URIRef(NS+"hasRetrievalDate"))
        dec.append((ident, body, short(s), url, ret))
    r = ["# Source manifest\n\n",
         "Every assertion about a case is traceable to the decision that states it. This "
         "manifest lists the trace in two directions: each decision with the body that issued "
         "it, and each individual with the decision it was taken from.\n\n",
         "Generated from the files by `scripts/build_documentation.py`.\n\n",
         f"## Decisions ({len(dec)})\n\n| identifier | issuing body | individual | published at | retrieved |\n|---|---|---|---|---|\n"]
    for ident, body, iri, url, ret in dec:
        r.append(f"| {ident} | {body} | `{iri}` | {url or '—'} | {ret[:10] if ret else '—'} |\n")
    r.append(f"\n## Individuals citing the decision they come from ({len(rows)})\n\n"
             "| source decision | individual | kind | label | triples |\n|---|---|---|---|---|\n")
    for src, iri, kinds, lab, n in rows:
        r.append(f"| {src} | `{iri}` | {kinds} | {lab} | {n} |\n")
    r.append("\nA decision with no published address is one obtained from a register that does "
             "not give a stable per-decision address; the issuing body and its own identifier "
             "are what retrieve it. Substances and designations are not listed here: each cites "
             "the edition of the Prohibited List or the article of the instrument that states "
             "it, through `adro:statedIn` and `adro:definedIn`.\n")
    open(out, "w", encoding="utf-8").write("".join(r))

def main(root):
    core, g, per = load(root)
    os.makedirs(os.path.join(root, "reports"), exist_ok=True)
    dictionary(core, g, os.path.join(root, "reports", "data-dictionary.md"))
    metrics(core, g, per, root, os.path.join(root, "reports", "ontology-metrics.md"))
    manifest(g, os.path.join(root, "reports", "source-manifest.md"))
    print("wrote data-dictionary.md, ontology-metrics.md, source-manifest.md")

main(sys.argv[1] if len(sys.argv) > 1 else ".")
