# Anti-Doping Regulation Ontology

An ontology of anti-doping regulation: the World Anti-Doping Code and the
instruments that restate it, the Prohibited List, and the decisions that apply
them. Built on the Basic Formal Ontology (ISO/IEC 21838-2) and the Information
Artifact Ontology.

- Base IRI: `https://w3id.org/adro/`
- Licence: [CC BY 4.0](LICENSE)
- Authors: Minjeong Kwak, Jun-Phil Uhm, Minkyu Kim

## What is here

| file | what it holds |
|---|---|
| `doping-ontology-core.ttl` | the classes, properties and axioms |
| `doping-ontology-designations.ttl` | regulatory designations: violation types, categories, sanction types, contexts, routes, sports |
| `doping-ontology-substances.ttl` | the substances of the 2026 Prohibited List and their prohibition applicabilities |
| `doping-ontology-analytes.ttl` | metabolites named in the case corpus, each with the decision that names its parent |
| `doping-ontology-cases-cas.ttl` | a register of 212 Court of Arbitration for Sport decisions |
| `doping-ontology-cases-national.ttl` | eight decisions of national bodies, included as examples |
| `doping-ontology-procedure.ttl` | the course of a matter as first instance decisions record it |
| `dist/` | the modules merged into one file, in Turtle and RDF/XML |
| `competency-questions.sparql` | the questions the ontology is built to answer |
| `scripts/` | the programs that build every generated file from its source documents |
| `tests/` | the axiom test suite |
| `reports/` | extraction and validation reports, listing what was asserted and what was not |
| `catalog-v001.xml` | an OASIS catalog, so the whole set loads with no network access |

## Opening it

Open `doping-ontology-procedure.ttl` and the imports pull in every other
module, then the Basic Formal Ontology and the Information Artifact Ontology.
The catalog in this directory resolves all of them to the local copies, so
nothing is fetched over the network. To read one file instead, open
`dist/adro-full.ttl`.

The modules are the source. The files in `dist/` are built from them by
`scripts/build_release.py` and should not be edited.

## Rebuilding

Every generated file is produced from a published source document by a script
in `scripts/`. The scripts assert only what their sources state, and each
writes a report listing what it excluded and why.

```
python3 scripts/build_designations.py doping-ontology-designations.ttl
python3 scripts/build_substances.py <2026 Prohibited List PDF> doping-ontology-substances.ttl reports/substance-extraction-report.md
python3 scripts/extract_cas.py <directory of award digests> cas.json
python3 scripts/build_cases.py cas.json doping-ontology-substances.ttl doping-ontology-cases-cas.ttl reports/cas-extraction-report.md
python3 scripts/build_analytes.py doping-ontology-analytes.ttl
python3 scripts/build_cases_national.py doping-ontology-cases-national.ttl reports/national-examples-report.md
python3 scripts/build_procedure.py doping-ontology-procedure.ttl reports/procedure-extraction-report.md
python3 scripts/build_release.py . <release date>
```

Identifiers in an external chemical resource are mapped by a separate script,
because it needs a source this repository does not carry:

```
python3 scripts/map_external_identifiers.py doping-ontology-substances.ttl \
    doping-ontology-xrefs.ttl reports/external-identifier-report.md \
    --names names.tsv --compounds compounds.tsv
```

`names.tsv` and `compounds.tsv` are the ChEBI flat files. The script asserts an
identifier only where a substance name equals a ChEBI name or synonym exactly,
lists every substance under one of matched, ambiguous or not found, and asserts
nothing where more than one record matches.

The source documents are published by the World Anti-Doping Agency, the Court
of Arbitration for Sport and the national bodies named in the reports. They are
not redistributed here.

## Checking it

```
python3 tests/test_axioms.py                       # axioms, with the HermiT reasoner
python3 scripts/run_competency_questions.py . competency-questions.sparql reports/competency-questions-report.md
python3 scripts/check_cq_coverage.py . competency-questions.sparql dist/adro-inferred.ttl reports/cq-class-coverage.md
```

The axiom suite checks that the property chains produce the entailments they
are meant to, and that each defect pattern the design rules out is rejected as
inconsistent. The coverage check enforces the rule that a class stays only if a
competency question uses it.

Requires `rdflib`, `owlready2` and a Java runtime.

## What the corpus is, and what it is not

The register of decisions is not exhaustive. Decisions that were never
published, or that could not be obtained, are absent, and there is no
denominator. Nothing here supports a statement about how often anything
occurs, which sport carries the most risk, or how violations are distributed.
The decisions of national bodies are examples chosen to exercise structures the
appeal register does not exercise, and are not a sample of anything.

Every assertion about a case carries the decision that states it, identified by
the issuing institution and that institution's own reference, so that a reader
can retrieve the original.
