# Ontology metrics and reproducibility

Generated from the files by `scripts/build_documentation.py`.

## Size

| measure | count |
|---|---|
| classes | 57 |
| object properties | 44 |
| data properties | 20 |
| named individuals | 1764 |
| decisions | 220 |
| triples, summed over the modules | 11264 |
| triples, `dist/adro-full.ttl` | 11231 |
| classes with a definition | 57 of 57 |
| properties with a definition | 64 of 64 |

## Triples per module

| module | triples |
|---|---|
| `doping-ontology-core.ttl` | 838 |
| `doping-ontology-designations.ttl` | 769 |
| `doping-ontology-substances.ttl` | 5399 |
| `doping-ontology-analytes.ttl` | 47 |
| `doping-ontology-cases-cas.ttl` | 3459 |
| `doping-ontology-cases-national.ttl` | 350 |
| `doping-ontology-procedure.ttl` | 402 |

The two totals differ. A triple stated in two modules is one triple once they are merged, and the release carries one ontology header in place of the seven the modules carry. The summed figure is what this table adds up to; the release figure is what a reviewer who opens `dist/adro-full.ttl` will count. Cite whichever is meant.

## Axioms

| kind | count |
|---|---|
| disjointness | 7 |
| property chains | 2 |
| transitive | 1 |
| existential | 9 |
| inverse | 2 |
| subproperty | 4 |
| class complement | 1 |
| equivalent class | 4 |

## Profile and imports

The constructs used are class and property declarations, subclass and subproperty axioms, domains and ranges, existential restrictions, equivalent-class axioms that state a necessary and sufficient condition for four classes, unions of two classes used as a domain or as a range, pairwise disjointness, inverse properties, one transitive property, two property chain axioms, one class complement on an individual, and typed data properties. These lie within OWL 2 DL. The ontology carries no cardinality restrictions, no nominals beyond one `owl:hasValue`, and no datatype outside the OWL 2 datatype map: `xsd:duration` and `xsd:date` are deliberately avoided, and periods are carried as `xsd:decimal` months and instants as `xsd:dateTime`.

| imported | IRI |
|---|---|
| Basic Formal Ontology | `http://purl.obolibrary.org/obo/bfo.owl` |
| Information Artifact Ontology | `http://purl.obolibrary.org/obo/iao.owl` |

Both are resolved to the copies in this directory by `catalog-v001.xml`, so the set loads with no network access.

## Reasoner

HermiT, through owlready2, with property values inferred. The axiom suite in `tests/` loads the merged graph, runs the reasoner, and reports consistency and the entailments obtained. The competency questions are additionally run at three strengths of entailment; see `reports/competency-questions-report.md`.
