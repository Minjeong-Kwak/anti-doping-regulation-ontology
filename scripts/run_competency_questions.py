# -*- coding: utf-8 -*-
"""
Runs every competency question and reports what each returns.

A question that returns nothing is a finding, not a failure of the runner: it
says the ontology cannot answer a question it was written to answer. Those are
listed separately at the end.

Questions marked "inference: required" are run against the graph after the
reasoner has materialised the property chains. The rest run against the
asserted triples alone. The difference between the two is reported.
"""
import os, re, sys, rdflib
from rdflib import RDF, RDFS, OWL, URIRef

PREFIX = """PREFIX adro: <https://w3id.org/adro/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

def parse(path):
    qs, cur = [], None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"#CQ ([A-E]\d+) \| (.*?) \| entailment: (none|subclass|chain)\s*$", line)
        if m:
            if cur: qs.append(cur)
            cur = dict(id=m.group(1), text=m.group(2), level=m.group(3), body="")
        elif cur is not None and not line.startswith("#"):
            cur["body"] += line
    if cur: qs.append(cur)
    for q in qs:
        q["body"] = q["body"].strip()
    return qs

def asserted_graph(root):
    g = rdflib.Graph()
    for f in ["doping-ontology-core.ttl", "doping-ontology-designations.ttl",
              "doping-ontology-substances.ttl", "doping-ontology-analytes.ttl",
              "doping-ontology-cases-cas.ttl", "doping-ontology-cases-national.ttl",
              "doping-ontology-procedure.ttl"]:
        g.parse(os.path.join(root, f), format="turtle")
    return g

def subclass_closed(root):
    """RDFS subclass closure alone.

    Without it a query for a decision misses the first instance and appeal
    decisions, which are subclasses of it. A triple store with RDFS entailment
    does this; rdflib does not."""
    g = asserted_graph(root)
    core = rdflib.Graph(); core.parse(os.path.join(root, "doping-ontology-core.ttl"), format="turtle")
    sup = {}
    for c, p in core.subject_objects(RDFS.subClassOf):
        if isinstance(p, URIRef):
            sup.setdefault(c, set()).add(p)
    def ancestors(c, seen=None):
        seen = seen if seen is not None else set()
        for p in sup.get(c, ()):
            if p not in seen:
                seen.add(p); ancestors(p, seen)
        return seen
    for s_, o in list(g.subject_objects(RDF.type)):
        for a in ancestors(o):
            g.add((s_, RDF.type, a))
    return g

def inferred_graph(root, cache):
    """Materialise the two property chains and the transitive category relation.

    The chains are stated in the core file and are read from it rather than
    restated here, so that a change to a chain is reflected without editing
    this script."""
    if os.path.exists(cache):
        g = rdflib.Graph(); g.parse(cache, format="turtle"); return g
    g = subclass_closed(root)
    core = rdflib.Graph(); core.parse(os.path.join(root, "doping-ontology-core.ttl"), format="turtle")
    added = 1
    while added:
        added = 0
        for prop, chain in core.subject_objects(OWL.propertyChainAxiom):
            steps = list(rdflib.collection.Collection(core, chain))
            if len(steps) != 2: continue
            p1, p2 = steps
            # p1 may be declared only as the inverse of another property
            def pairs(p):
                out = set(g.subject_objects(p))
                for inv in core.objects(p, OWL.inverseOf):
                    out |= {(o, s) for s, o in g.subject_objects(inv)}
                for inv in core.subjects(OWL.inverseOf, p):
                    out |= {(o, s) for s, o in g.subject_objects(inv)}
                return out
            first, second = pairs(p1), pairs(p2)
            idx = {}
            for s, o in second: idx.setdefault(s, []).append(o)
            for s, mid in first:
                for o in idx.get(mid, []):
                    if (s, prop, o) not in g:
                        g.add((s, prop, o)); added += 1
        for p in core.subjects(RDF.type, OWL.TransitiveProperty):
            edges = list(g.subject_objects(p))
            idx = {}
            for s, o in edges: idx.setdefault(s, []).append(o)
            for s, o in edges:
                for o2 in idx.get(o, []):
                    if (s, p, o2) not in g:
                        g.add((s, p, o2)); added += 1
    g.serialize(cache, format="turtle")
    return g

ROLE = {
 "A1": ("an analyst reading the regulation", "find the article that defines a violation type"),
 "A2": ("an analyst or a results manager", "establish under what terms a substance is prohibited"),
 "A3": ("an analyst", "roll a narrow category up to the one that governs it"),
 "A4": ("a laboratory or a results manager", "find the threshold a finding must exceed"),
 "A5": ("a physician or a results manager", "find whether a route of administration is exempt"),
 "A6": ("a results manager working under a national rule", "map a national provision to the Code"),
 "A7": ("a results manager", "find which rules a governing body has taken over"),
 "A8": ("an analyst", "enumerate the prohibited methods and their categories"),
 "A9": ("a physician or an athlete", "find what an exemption requires and what a decision on one must state"),
 "A10": ("a results manager", "establish which instrument binds a person and where"),
 "A11": ("a deciding body", "enumerate the grounds that alter a period of ineligibility"),
 "A12": ("a laboratory or a deciding body", "establish what Article 2.1 covers besides the parent substance"),
 "B1": ("a researcher or a deciding body", "find the decisions that determined a given violation type"),
 "B2": ("a deciding body or a researcher", "trace an appeal to the decision below and compare the sanctions"),
 "B3": ("a laboratory or a deciding body", "trace an analyte to the substance it derives from"),
 "B4": ("a researcher", "find matters that rest on more than one listed substance"),
 "B5": ("a deciding body", "find matters in which one sample supported more than one violation"),
 "B6": ("an athlete, a federation or a researcher", "establish what consequence was imposed and over what interval"),
 "B7": ("a researcher", "establish which body managed the results of a matter"),
 "B8": ("a federation or a researcher", "gather the matters in a sport, including its disciplines"),
 "B9": ("a federation or a researcher", "establish the stage a matter has reached"),
 "B10": ("a researcher", "see how the register is spread across sports"),
 "B11": ("a deciding body", "find the violation types that reach a person other than the athlete"),
 "B12": ("a deciding body or a researcher", "establish who a decision treated as support personnel"),
 "B13": ("a deciding body", "see which grounds were raised and which were established"),
 "B14": ("a reviewer checking provenance", "establish the jurisdiction of a matter and retrieve the decision"),
 "C1": ("a results manager or a reviewer", "reconstruct the order of events in a matter"),
 "C2": ("a results manager", "establish from whom a sample was taken"),
 "C3": ("a results manager", "establish whom an analytical finding concerns"),
 "C4": ("a reviewer checking an analysis", "establish which laboratory analysed a sample and how"),
 "C5": ("an athlete or a federation", "check whether ineligibility runs from the provisional suspension"),
 "C6": ("a reviewer", "establish the document on which a proceeding was opened"),
 "C7": ("a reviewer checking an analysis", "establish which portion of a sample was analysed"),
 "D1": ("a reviewer", "retrieve the decision behind any assertion"),
 "D2": ("a reviewer or a curator", "find the matters that turn on conduct rather than a substance"),
 "D3": ("a deciding body", "establish whether an exemption was recorded as absent"),
 "D4": ("a reviewer", "see which kinds of analytical report the ontology holds"),
 "E1": ("a deciding body or a researcher", "trace a determination from the substance to the Code article"),
 "E2": ("a results manager", "find determinations made under an instrument other than the Code"),
}

def main(root, cq_path, out_path):
    qs = parse(cq_path)
    g0 = asserted_graph(root)
    g1 = subclass_closed(root)
    g2 = inferred_graph(root, os.path.join(root, "dist", "adro-inferred.ttl"))
    LEVELS = [("none", g0), ("subclass", g1), ("chain", g2)]
    WORDS = {24: "Twenty-four", 39: "Thirty-nine", 40: "Forty"}
    n_q = WORDS.get(len(qs), str(len(qs)))
    rep = ["# Competency questions and what they return\n\n",
           f"{n_q} questions, run at three strengths of entailment: over the "
           "asserted triples alone, after subclass closure, and after the property "
           "chains and the transitive category relation are also materialised. The "
           "level recorded for each question is the weakest at which it gives its full "
           "answer. That a question needs more than the asserted triples is the point "
           "of the axioms; that most need none is what keeps the ontology usable in a "
           "store without a reasoner.\n\n",
           "The corpus of decisions is not exhaustive, so no question asks what is most "
           "frequent or how anything is distributed. A row count is the number of "
           "answers found in the material held. It is not a measurement of the world.\n\n",
           "| question | asserted | + subclass | + chains | needs |\n|---|---|---|---|---|\n"]
    empty, mismatch, details = [], [], []
    for q in qs:
        counts = {}
        for name, g in LEVELS:
            try:
                counts[name] = len(list(g.query(PREFIX + q["body"])))
            except Exception as e:
                counts[name] = f"error: {e}"
        nums = [counts[n] for n, _ in LEVELS]
        rep.append(f"| **{q['id']}** {q['text']} | {nums[0]} | {nums[1]} | {nums[2]} | {q['level']} |\n")
        if nums[2] == 0:
            empty.append((q["id"], q["text"]))
        # the weakest level that already gives the full answer
        if all(isinstance(n, int) for n in nums):
            full = nums[2]
            actual = "none" if nums[0] == full else ("subclass" if nums[1] == full else "chain")
            if actual != q["level"]:
                mismatch.append((q["id"], f"declared {q['level']}, but its full answer first appears at {actual}"))
        rows = list(g2.query(PREFIX + q["body"]))[:3]
        if rows:
            details.append(f"\n### {q['id']}\n\n{q['text']}\n\n")
            for r in rows:
                details.append("- " + " \u00b7 ".join(str(x) for x in r) + "\n")
    rep.append("\n## Questions that return nothing\n\n")
    rep += ([f"- **{i}** {t}\n" for i, t in empty] or ["None.\n"])
    rep.append("\n## Questions whose declared entailment level is wrong\n\n")
    rep += ([f"- **{i}** {t}\n" for i, t in mismatch] or ["None.\n"])
    # the table the review asks for: one row per question, with who asks it, the
    # task it serves, the terms it uses, and whether it needs a reasoner.
    tbl = ["\n## Every question, with its purpose and what it uses\n\n",
           "| id | who asks | task it serves | terms used | rows | entailment |\n|---|---|---|---|---|---|\n"]
    import re as _re
    for q in qs:
        terms = sorted(set(_re.findall(r"adro:([A-Za-z0-9_]+)", q["body"])))
        terms = [t for t in terms if not t.startswith(("Substance_", "Category_", "Sport_",
                                                       "ADRVType_", "Context_", "Route_",
                                                       "Person_", "Decision_", "Entry_"))]
        who, task = ROLE.get(q["id"], ("—", "—"))
        n = len(list(g2.query(PREFIX + q["body"])))
        tbl.append(f"| **{q['id']}** | {who} | {task} | " +
                   ", ".join(f"`{t}`" for t in terms[:8]) +
                   (" …" if len(terms) > 8 else "") +
                   f" | {n} | {q['level']} |\n")
    rep += tbl
    rep.append("\nThe expected answer for each question is the one recorded in the section below, "
               "taken from the run that produced this report. A question whose row count changes "
               "after an edit to the ontology is a question to re-read, not a number to update.\n")
    rep.append("\n## First answers to each question\n")
    rep += details
    open(out_path, "w", encoding="utf-8").write("".join(rep))
    print("questions", len(qs), "empty", len(empty), "mismatched", len(mismatch))

main(sys.argv[1], sys.argv[2], sys.argv[3])
