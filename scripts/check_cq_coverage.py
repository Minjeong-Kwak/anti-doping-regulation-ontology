# -*- coding: utf-8 -*-
"""
Measures which classes the competency questions reach.

The first design principle for this ontology is that a class stays only if a
competency question uses it. This script is what makes that principle checkable.

A class counts as reached if a question names it, or if an individual of it is
bound by a question's solution. Binding, not projection, is what counts: a
question that joins through a case record reaches that class whether or not it
prints it.
"""
import os, re, sys, rdflib
from rdflib import RDF, OWL

NS = "https://w3id.org/adro/"
PREFIX = """PREFIX adro: <https://w3id.org/adro/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

def questions(path):
    qs, cur = [], None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"#CQ ([A-E]\d+) \| (.*?) \|", line)
        if m:
            if cur: qs.append(cur)
            cur = dict(id=m.group(1), text=m.group(2), body="")
        elif cur is not None and not line.startswith("#"):
            cur["body"] += line
    if cur: qs.append(cur)
    return qs

def main(root, cq_path, graph_path, out_path):
    core = rdflib.Graph(); core.parse(os.path.join(root, "doping-ontology-core.ttl"), format="turtle")
    classes = {str(s).replace(NS, "") for s in core.subjects(RDF.type, OWL.Class)
               if str(s).startswith(NS)}
    g = rdflib.Graph(); g.parse(graph_path, format="turtle")
    inst = {}
    for s, _, o in g.triples((None, RDF.type, None)):
        if str(o).startswith(NS):
            inst.setdefault(str(o).replace(NS, ""), set()).add(str(s))
    reach = {c: set() for c in classes}
    for q in questions(cq_path):
        for c in classes:
            if re.search(r"adro:" + c + r"\b", q["body"]):
                reach[c].add(q["id"])
        star = re.sub(r"SELECT\s+.*?\s+WHERE", "SELECT * WHERE", q["body"], count=1, flags=re.S)
        rows = []
        for b in (star, q["body"]):
            try:
                rows = list(g.query(PREFIX + b)); break
            except Exception:
                continue
        vals = {str(x) for r in rows for x in r}
        for c in classes:
            if vals & inst.get(c, set()):
                reach[c].add(q["id"])
    un = sorted(c for c in classes if not reach[c])
    rep = ["# Which classes the competency questions reach\n\n",
           "A class stays in this ontology only if a competency question uses it. "
           "This report is what makes that principle checkable rather than asserted.\n\n",
           f"Classes: {len(classes)}. Reached: {len(classes) - len(un)}. "
           f"Not reached: {len(un)}.\n\n",
           "A class counts as reached if a question names it, or if an individual of it "
           "is bound by a question's solution. Binding is what counts, not printing: a "
           "question that joins through a case record reaches that class whether or not "
           "it prints it.\n\n"]
    if un:
        rep.append("## Classes no question reaches\n\n")
        for c in un: rep.append(f"- `{c}`\n")
        rep.append("\nEach is a candidate for removal.\n")
    else:
        rep.append("Every class is reached.\n")
    rep.append("\n## Questions that reach each class\n\n| class | questions |\n|---|---|\n")
    for c in sorted(classes):
        rep.append(f"| `{c}` | {', '.join(sorted(reach[c])) or 'none'} |\n")
    open(out_path, "w", encoding="utf-8").write("".join(rep))
    print(f"classes {len(classes)} reached {len(classes)-len(un)} unreached {len(un)}")
    if un: print("  ", un)

main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
