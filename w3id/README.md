# adro

Anti-Doping Regulation Ontology. An ontology of the World Anti-Doping Code, the
Prohibited List, and the decisions that apply them, built on the Basic Formal
Ontology and the Information Artifact Ontology.

- Base IRI: `https://w3id.org/adro/`
- Source and releases: https://github.com/Minjeong-Kwak/anti-doping-regulation-ontology

## Contact

Minjeong Kwak — cynicalrei@gmail.com — GitHub: Minjeong-Kwak

## What the identifiers resolve to

| identifier | resolves to |
|---|---|
| `https://w3id.org/adro/` | the core module, which declares the classes and properties |
| `https://w3id.org/adro/designations` | the regulatory designations |
| `https://w3id.org/adro/substances` | the substances of the Prohibited List |
| `https://w3id.org/adro/analytes` | metabolites named in the case corpus |
| `https://w3id.org/adro/cases-cas` | the register of Court of Arbitration for Sport decisions |
| `https://w3id.org/adro/cases-national` | decisions of national bodies, as examples |
| `https://w3id.org/adro/procedure` | the course of a matter as first instance decisions record it |
| `https://w3id.org/adro/full` | every module merged into one file |
| `https://w3id.org/adro/tbox` | the vocabulary alone |
| `https://w3id.org/adro/YYYY-MM-DD/FILE` | that file as it stood in the release of that date |

A request that states it accepts HTML is sent to the documentation. Every other
request is sent to the ontology file itself, so that a reasoner following
`owl:imports` resolves each module without a browser.
