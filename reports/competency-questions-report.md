# Competency questions and what they return

Thirty-nine questions, run at three strengths of entailment: over the asserted triples alone, after subclass closure, and after the property chains and the transitive category relation are also materialised. The level recorded for each question is the weakest at which it gives its full answer. That a question needs more than the asserted triples is the point of the axioms; that most need none is what keeps the ontology usable in a store without a reasoner.

The corpus of decisions is not exhaustive, so no question asks what is most frequent or how anything is distributed. A row count is the number of answers found in the material held. It is not a measurement of the world.

| question | asserted | + subclass | + chains | needs |
|---|---|---|---|---|
| **A1** Which Code article defines a given anti-doping rule violation type, and what does the article direct? | 11 | 11 | 11 | none |
| **A2** Under which Prohibited List entry is a given substance prohibited, in which competition context, and under what category? | 1 | 1 | 1 | none |
| **A3** Which categories does a given category fall under, directly or through an intervening category? | 1 | 1 | 2 | chain |
| **A4** Which substances does the List prohibit only above a stated decision limit, in what unit and in which specimen is that limit stated? | 6 | 6 | 6 | none |
| **A5** For which substances does the List confine the prohibition to a stated route of administration? | 64 | 64 | 64 | none |
| **A6** Which provisions of instruments other than the Code restate a given Code article, and in which instrument does each sit? | 3 | 3 | 3 | none |
| **A7** Which governing body takes over another instrument in place of stating its own rules? | 2 | 2 | 2 | none |
| **A8** Which prohibited methods does the List state, and under which method category does each sit? | 11 | 11 | 11 | none |
| **A9** What do the instruments provide about an exemption, and which exemption decisions does the ontology hold? | 3 | 3 | 3 | none |
| **A10** Within which jurisdiction does a given instrument bind, and on what scope provision? | 5 | 5 | 5 | none |
| **A11** Which grounds may lengthen or shorten a period of ineligibility, and in which provision is each defined? | 4 | 4 | 4 | none |
| **A12** What does Article 2.1 cover besides the substance itself, and which such analytes does the ontology hold? | 10 | 10 | 10 | none |
| **B1** Which decisions determine a given violation type, and under which provision was it determined? | 40 | 40 | 40 | none |
| **B2** Which decision does a given appeal reconsider, which body issued each, and did the appeal change the period of ineligibility? | 5 | 5 | 5 | none |
| **B3** Which decisions name an analyte that is a metabolite rather than a listed substance, and what substance does it derive from? | 50 | 50 | 50 | none |
| **B4** Which decisions rest on more than one listed substance? | 7 | 17 | 17 | subclass |
| **B5** Which decisions determine more than one violation type on the same matter? | 3 | 3 | 3 | none |
| **B6** For a given matter, what consequence was established, for how long, and over which interval? | 13 | 13 | 13 | none |
| **B7** Which body managed the results of a given matter, and what kind of body is it? | 220 | 224 | 224 | subclass |
| **B8** Which matters concern athletics, whether the headnote names the sport or one of its disciplines? | 54 | 54 | 54 | none |
| **B10** Which sports does the register name, counting a discipline under its sport? | 52 | 52 | 52 | none |
| **B9** What is the recorded status of a given matter, and does a decision reconsidering it exist? | 221 | 221 | 221 | none |
| **B11** Which violation types does the regulation direct at a person other than the athlete, and which matters in the register determine one? | 6 | 6 | 6 | none |
| **B12** Which persons does a decision identify as athlete support personnel, and on what wording? | 3 | 3 | 3 | none |
| **B13** Which grounds did a decision record as raised, and did it establish them? | 4 | 4 | 4 | none |
| **B14** Which matters fell under a given jurisdiction, and where was the decision obtained? | 4 | 4 | 4 | none |
| **C1** For a given matter, what is the order of events from collection to decision, with the dates the decision states? | 16 | 16 | 16 | none |
| **C2** From whom was a given sample collected? | 0 | 0 | 6 | chain |
| **C3** Which person does a given adverse analytical finding concern? | 0 | 0 | 4 | chain |
| **C4** Which laboratory analysed the sample in a given matter, and by what method? | 3 | 3 | 3 | none |
| **C5** Which matters record a provisional suspension, and does the period of ineligibility run from that date? | 2 | 2 | 2 | none |
| **C6** Which document opened a given proceeding, and when? | 4 | 4 | 4 | none |
| **C7** What portions does a sample have, what reference does each carry, and which portion was analysed? | 6 | 6 | 6 | none |
| **D1** For a given individual in the procedural layer, which decision states it, and by what identifier can that decision be retrieved? | 86 | 86 | 86 | none |
| **D2** Which decisions in the register carry no link to a substance? | 6 | 75 | 75 | subclass |
| **D3** Is there a decision stating that a given person held no exemption for a named substance, and which substance is it? | 1 | 1 | 1 | none |
| **D4** Which kinds of analytical report does the regulation distinguish, and which does the ontology hold? | 4 | 4 | 4 | none |
| **E1** Given a substance a decision names, which List entry, which category, which violation type and which Code article stand behind the determination? | 10 | 10 | 10 | none |
| **E2** Which violation types were determined under an instrument other than the Code, and under which instrument? | 16 | 16 | 16 | none |

## Questions that return nothing

None.

## Questions whose declared entailment level is wrong

None.

## Every question, with its purpose and what it uses

| id | who asks | task it serves | terms used | rows | entailment |
|---|---|---|---|---|---|
| **A1** | an analyst reading the regulation | find the article that defines a violation type | `ADRVType`, `definedIn` | 11 | none |
| **A2** | an analyst or a results manager | establish under what terms a substance is prohibited | `ProhibitionApplicability`, `appliesTo`, `competitionContext`, `hasCategory`, `statedIn` | 1 | none |
| **A3** | an analyst | roll a narrow category up to the one that governs it | `broaderCategory` | 2 | chain |
| **A4** | a laboratory or a results manager | find the threshold a finding must exceed | `appliesTo`, `hasDecisionLimit`, `hasMeasurementUnit`, `hasSpecimenMatrix`, `hasThresholdValue` | 6 | none |
| **A5** | a physician or a results manager | find whether a route of administration is exempt | `appliesTo`, `routeOfAdministration` | 64 | none |
| **A6** | a results manager working under a national rule | map a national provision to the Code | `implementsCodeArticle` | 3 | none |
| **A7** | a results manager | find which rules a governing body has taken over | `adoptsInstrument` | 2 | none |
| **A8** | an analyst | enumerate the prohibited methods and their categories | `ProhibitedMethodCategory`, `definedIn` | 11 | none |
| **A9** | a physician or an athlete | find what an exemption requires and what a decision on one must state | `InstrumentProvision`, `TUEDecision` | 3 | none |
| **A10** | a results manager | establish which instrument binds a person and where | `bindsWithin` | 5 | none |
| **A11** | a deciding body | enumerate the grounds that alter a period of ineligibility | `SanctionModifyingGround`, `definedIn` | 4 | none |
| **A12** | a laboratory or a deciding body | establish what Article 2.1 covers besides the parent substance | `Marker`, `Metabolite`, `indicatesUseOf`, `isMetaboliteOf` | 10 | none |
| **B1** | a researcher or a deciding body | find the decisions that determined a given violation type | `appliedProvision`, `assignsType`, `hasCaseIdentifier` | 40 | none |
| **B2** | a deciding body or a researcher | trace an appeal to the decision below and compare the sanctions | `appealsAgainst`, `establishes`, `hasCaseIdentifier`, `hasIneligibilityDurationInMonths`, `issuedBy` | 5 | none |
| **B3** | a laboratory or a deciding body | trace an analyte to the substance it derives from | `Metabolite`, `hasCaseIdentifier`, `isMetaboliteOf`, `mentions` | 50 | none |
| **B4** | a researcher | find matters that rest on more than one listed substance | `ChemicalSubstance`, `hasCaseIdentifier`, `mentions` | 17 | subclass |
| **B5** | a deciding body | find matters in which one sample supported more than one violation | `assignsType`, `hasCaseIdentifier` | 3 | none |
| **B6** | an athlete, a federation or a researcher | establish what consequence was imposed and over what interval | `establishes`, `hasCaseIdentifier`, `hasEffectiveFrom`, `hasEffectiveTo`, `hasIneligibilityDurationInMonths`, `hasSanctionType` | 13 | none |
| **B7** | a researcher | establish which body managed the results of a matter | `AntiDopingOrganization`, `CaseRecord`, `NationalAntiDopingOrganization`, `Organization`, `hasCaseIdentifier`, `resultsManagementAuthority` | 224 | subclass |
| **B8** | a federation or a researcher | gather the matters in a sport, including its disciplines | `CaseRecord`, `broaderCategory`, `concernsSport`, `hasCaseIdentifier` | 54 | none |
| **B10** | a researcher | see how the register is spread across sports | `CaseRecord`, `broaderCategory`, `concernsSport` | 52 | none |
| **B9** | a federation or a researcher | establish the stage a matter has reached | `CaseRecord`, `appealsAgainst`, `caseStatus`, `hasCaseIdentifier` | 221 | none |
| **B11** | a deciding body | find the violation types that reach a person other than the athlete | `assignsType`, `definedIn`, `hasCaseIdentifier` | 6 | none |
| **B12** | a deciding body or a researcher | establish who a decision treated as support personnel | `AthleteSupportPersonnelRole`, `Person`, `bearerOfRole` | 3 | none |
| **B13** | a deciding body | see which grounds were raised and which were established | `acceptsGround`, `hasCaseIdentifier`, `raisesGround` | 4 | none |
| **B14** | a reviewer checking provenance | establish the jurisdiction of a matter and retrieve the decision | `CaseRecord`, `concernsJurisdiction`, `hasCaseIdentifier`, `hasRetrievalDate`, `hasSourceURL` | 4 | none |
| **C1** | a results manager or a reviewer | reconstruct the order of events in a matter | `Hearing`, `LaboratoryAnalysis`, `NotificationOfCharge`, `SampleCollection`, `concernsCase`, `hasAnalysisDateTime`, `hasCaseIdentifier`, `hasCollectionDateTime` … | 16 | none |
| **C2** | a results manager | establish from whom a sample was taken | `UrineSample`, `collectedFrom`, `hasPortion`, `hasSampleIdentifier` | 6 | chain |
| **C3** | a results manager | establish whom an analytical finding concerns | `AdverseAnalyticalFinding`, `concernsPerson` | 4 | chain |
| **C4** | a reviewer checking an analysis | establish which laboratory analysed a sample and how | `Laboratory`, `LaboratoryAnalysis`, `concernsCase`, `hasAnalyticalMethod`, `hasCaseIdentifier` | 3 | none |
| **C5** | an athlete or a federation | check whether ineligibility runs from the provisional suspension | `IneligibilityStatus`, `ProvisionalSuspensionStatus`, `concernsCase`, `establishes`, `hasCaseIdentifier`, `hasEffectiveFrom` | 2 | none |
| **C6** | a reviewer | establish the document on which a proceeding was opened | `hasIssueDateTime`, `initiatedBy` | 4 | none |
| **C7** | a reviewer checking an analysis | establish which portion of a sample was analysed | `LaboratoryAnalysis`, `UrineSample`, `concernsCase`, `hasCaseIdentifier`, `hasPortion`, `hasSampleIdentifier`, `hasSpecifiedInput` | 6 | none |
| **D1** | a reviewer | retrieve the decision behind any assertion |  | 86 | none |
| **D2** | a reviewer or a curator | find the matters that turn on conduct rather than a substance | `Decision`, `hasCaseIdentifier`, `mentions` | 75 | subclass |
| **D3** | a deciding body | establish whether an exemption was recorded as absent | `ExemptionStatus`, `Person`, `bearerOfRole`, `exemptionFor` | 1 | none |
| **D4** | a reviewer | see which kinds of analytical report the ontology holds | `AdverseAnalyticalFinding`, `AtypicalFinding` | 4 | none |
| **E1** | a deciding body or a researcher | trace a determination from the substance to the Code article | `ChemicalSubstance`, `appliesTo`, `assignsType`, `definedIn`, `hasCaseIdentifier`, `hasCategory`, `mentions`, `statedIn` | 10 | none |
| **E2** | a results manager | find determinations made under an instrument other than the Code | `WorldAntiDopingCode`, `appliedProvision`, `assignsType`, `hasCaseIdentifier` | 16 | none |

The expected answer for each question is the one recorded in the section below, taken from the run that produced this report. A question whose row count changes after an edit to the ontology is a question to re-read, not a number to update.

## First answers to each question

### A1

Which Code article defines a given anti-doping rule violation type, and what does the article direct?

- https://w3id.org/adro/ADRVType_Administration · ADRV type: Administration or Attempted Administration to any Athlete of any Prohibited Substance or Prohibited Method · https://w3id.org/adro/Article_2021_Administration · Administration or Attempted Administration to any Athlete of any Prohibited Substance or Prohibited Method
- https://w3id.org/adro/ADRVType_Complicity · ADRV type: Complicity or Attempted Complicity · https://w3id.org/adro/Article_2021_Complicity · Complicity or Attempted Complicity
- https://w3id.org/adro/ADRVType_EvadingRefusingFailing · ADRV type: Evading, refusing or failing to submit to Sample collection · https://w3id.org/adro/Article_2021_EvadingRefusingFailing · Evading, refusing or failing to submit to Sample collection

### A2

Under which Prohibited List entry is a given substance prohibited, in which competition context, and under what category?

- Stanozolol · The 2026 Prohibited List, S1.1 · S1.1 Anabolic androgenic steroids (AAS) · prohibited at all times

### A3

Which categories does a given category fall under, directly or through an intervening category?

- S2.1.1 Erythropoietin receptor agonists · S2 Peptide hormones, growth factors, related substances, and mimetics
- S2.1.1 Erythropoietin receptor agonists · S2.1 Erythropoietins (EPO) and agents affecting erythropoiesis

### A4

Which substances does the List prohibit only above a stated decision limit, in what unit and in which specimen is that limit stated?

- Cathine · reporting threshold for Cathine in urine, 2026 Prohibited List · 5.0 · microgram per millilitre · urine
- Ephedrine · reporting threshold for Ephedrine in urine, 2026 Prohibited List · 10.0 · microgram per millilitre · urine
- Formoterol · reporting threshold for Formoterol in urine, 2026 Prohibited List · 40.0 · nanogram per millilitre · urine

### A5

For which substances does the List confine the prohibition to a stated route of administration?

- Beclometasone · injectable
- Beclometasone · oral
- Beclometasone · oromucosal

### A6

Which provisions of instruments other than the Code restate a given Code article, and in which instrument does each sit?

- UK Anti-Doping Rules 2021, Article 2.2 · UK Anti-Doping Rules, 1 January 2021 · World Anti-Doping Code 2021, Article 2.2
- UK Anti-Doping Rules 2021, Article 2.1 · UK Anti-Doping Rules, 1 January 2021 · World Anti-Doping Code 2021, Article 2.1
- Code du sport, article L. 232-9 · Code du sport (France) · World Anti-Doping Code 2021, Article 2.1

### A7

Which governing body takes over another instrument in place of stating its own rules?

- Anti-Doping Rules of the British Boxing Board of Control · UK Anti-Doping Rules, 1 January 2021
- Anti-Doping Rules of the Rugby Football League · UK Anti-Doping Rules, 1 January 2021

### A8

Which prohibited methods does the List state, and under which method category does each sit?

- M1 Manipulation of blood and blood components · The 2026 Prohibited List, M1
- M1.1 Administration or reintroduction of blood or red blood cell products · The 2026 Prohibited List, M1.1
- M1.2 Artificially enhancing the uptake, transport or delivery of oxygen · The 2026 Prohibited List, M1.2

### A9

What do the instruments provide about an exemption, and which exemption decisions does the ontology hold?

- UK Anti-Doping Rules 2021, Article 4.1 · Incorporation of the International Standard for Therapeutic Use Exemptions · The provision states that the standard sets out the circumstances in which Athletes may be granted permission to Use, for therapeutic purposes, substances or methods on the Prohibited List the Use of which would otherwise be prohibited. · None
- UK Anti-Doping Rules 2021, Article 4.2.1 · Scope and effect of therapeutic use exemptions · The provision states that the presence, Use or Attempted Use, Possession or Administration of a Prohibited Substance or Prohibited Method shall not be considered an Anti-Doping Rule Violation if it is consistent with the provisions of a TUE validly granted. This is why an exemption belongs in the ontology: it defeats the prohibition stated in the same instrument. · None
- UK Anti-Doping Rules 2021, Article 4.4 · Grant of a therapeutic use exemption · The provision states that a decision to grant must specify the dosage, frequency, route and duration of Administration permitted, and that a decision to deny must include the reasons for the denial. No correspondence to a Code article is asserted, because the instrument does not state which article it restates. · None

### A10

Within which jurisdiction does a given instrument bind, and on what scope provision?

- Code du sport (France) · France · As stated in Code du sport, article L. 230-3: For the purposes of the title on the fight against doping, an athlete is any person who takes part in or prepares for a sporting event organised by an approved federation or authorised by a delegated federation, a sporting event at which prizes are awarded, or an international sporting event or one within the competence of an anti-doping organisation that is a signatory of the World Anti-Doping Code.
- Anti-Doping Rules of the British Boxing Board of Control · United Kingdom · As stated in UK Anti-Doping Rules 2021, Article 1.2: These Rules apply to all Athletes and Athlete Support Personnel who are members of the NGB and/or of the NGB's members or affiliate organisations or licensees, or otherwise under the jurisdiction of the NGB.
- Anti-Doping Rules of the Rugby Football League · United Kingdom · As stated in UK Anti-Doping Rules 2021, Article 1.2: These Rules apply to all Athletes and Athlete Support Personnel who are members of the NGB and/or of the NGB's members or affiliate organisations or licensees, or otherwise under the jurisdiction of the NGB.

### A11

Which grounds may lengthen or shorten a period of ineligibility, and in which provision is each defined?

- Aggravating Circumstances · UK Anti-Doping Rules 2021, Article 10.4 · Aggravating Circumstances which may increase the period of Ineligibility
- No Fault or Negligence · UK Anti-Doping Rules 2021, Article 10.5 · Elimination of the period of Ineligibility where there is No Fault or Negligence
- No Significant Fault or Negligence · UK Anti-Doping Rules 2021, Article 10.6 · Reduction of the period of Ineligibility based on No Significant Fault or Negligence

### A12

What does Article 2.1 cover besides the substance itself, and which such analytes does the ontology hold?

- metabolite · 17a-hydroxymethyl-17β-methyl-18-nor-2-oxa-5a-androst-13-en-3-one · Oxandrolone
- metabolite · 17β-hydroxymethyl,17α-methyl-18-norandrost-1,4,13-trien-3-one · Metandienone
- metabolite · 18-nor-17β-hydroxymethyl-17α-methyl-2α-methyl-5α-androst-13-en-3-one · Methasterone

### B1

Which decisions determine a given violation type, and under which provision was it determined?

- AAA Case No. 30 190 00847 06 · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · UCI Anti-Doping Regulations, Article 15.1
- AAA Case No. 30 190 00847 06 · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · UCI Anti-Doping Regulations, Article 261
- AAA No. 30 190 00170 07 · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · None

### B2

Which decision does a given appeal reconsider, which body issued each, and did the appeal change the period of ineligibility?

- CAS 2007/A/1394 · Court of Arbitration for Sport · AAA Case No. 30 190 00847 06 · North American Court of Arbitration for Sport Panel of the American Arbitration Association · None · 24.0
- CAS 2008/A/1461 · Court of Arbitration for Sport · AAA No. 30 190 00170 07 · North American Court of Arbitration for Sport Panel of the American Arbitration Association · None · 48.0
- CAS 2008/A/1462 · Court of Arbitration for Sport · AAA No. 30 190 00170 07 · North American Court of Arbitration for Sport Panel of the American Arbitration Association · None · 48.0

### B3

Which decisions name an analyte that is a metabolite rather than a listed substance, and what substance does it derive from?

- CAS 2006/A/1130 · Methylecgonine · Cocaine
- CAS 2006/A/1130 · Benzoylecgonine · Cocaine
- CAS 2006/A/1153 · 19-Norandrosterone · Nandrolone

### B4

Which decisions rest on more than one listed substance?

- CAS 2006/A/1130 · 2
- CAS 2007/A/1284 · 2
- CAS 2007/A/1308 · 2

### B5

Which decisions determine more than one violation type on the same matter?

- SR/389/2024 · 2
- SR/007/2023 · 2
- CAS 2018/A/6047 · 2

### B6

For a given matter, what consequence was established, for how long, and over which interval?

- AAA Case No. 30 190 00847 06 · disqualification · 24.0 · 2007-01-30T00:00:00 · 2009-01-29T00:00:00
- AAA Case No. 30 190 00847 06 · period of ineligibility · 24.0 · 2007-01-30T00:00:00 · 2009-01-29T00:00:00
- AAA No. 30 190 00170 07 · disqualification · 48.0 · None · None

### B7

Which body managed the results of a given matter, and what kind of body is it?

- AAA Case No. 30 190 00847 06 · North American Court of Arbitration for Sport Panel of the American Arbitration Association · https://w3id.org/adro/Organization
- AAA No. 30 190 00170 07 · North American Court of Arbitration for Sport Panel of the American Arbitration Association · https://w3id.org/adro/Organization
- CAS (Oceania Registry) A1/2015 · Court of Arbitration for Sport · https://w3id.org/adro/Organization

### B8

Which matters concern athletics, whether the headnote names the sport or one of its disciplines?

- AAA No. 30 190 00170 07 · Athletics
- CAS (Oceania Registry) A4/2014 · Athletics (road walking)
- CAS 2004/O/645 · Athletics

### B10

Which sports does the register name, counting a discipline under its sport?

- Athletics · 54
- Football · 23
- Cycling · 19

### B9

What is the recorded status of a given matter, and does a decision reconsidering it exist?

- AAA Case No. 30 190 00847 06 · final · CAS 2007/A/1394
- AAA No. 30 190 00170 07 · final · CAS 2008/A/1461
- AAA No. 30 190 00170 07 · final · CAS 2008/A/1462

### B11

Which violation types does the regulation direct at a person other than the athlete, and which matters in the register determine one?

- ADRV type: Administration or Attempted Administration to any Athlete of any Prohibited Substance or Prohibited Method · Administration or Attempted Administration to any Athlete of any Prohibited Substance or Prohibited Method · None
- ADRV type: Complicity or Attempted Complicity · Complicity or Attempted Complicity · CAS 2018/A/6047
- ADRV type: Prohibited Association by an Athlete or other Person · Prohibited Association by an Athlete or other Person · CAS 2020/A/6986

### B12

Which persons does a decision identify as athlete support personnel, and on what wording?

- Sevdalin Marinov · CAS 2007/A/1311 · As stated in CAS 2007/A/1311: Sevdalin Marinov (the Appellant), a head coach of an Australian weightlifting team.
- Lyudmila Vladimirvma Fedoriva · CAS 2016/A/4700 · As stated in CAS 2016/A/4700: Doping (tampering or attempted tampering with any part of doping control by a coach).
- Andrei Valerievich Eremenko · CAS 2018/A/6047 · As stated in CAS 2018/A/6047: Doping (tampering/attempted tampering and complicity of coach).

### B13

Which grounds did a decision record as raised, and did it establish them?

- SR/015/2023 · No Fault or Negligence · false
- SR/015/2023 · No Significant Fault or Negligence · false
- SR/015/2023 · violation not intentional · false

### B14

Which matters fell under a given jurisdiction, and where was the decision obtained?

- AAA Case No. 30 190 00847 06 · international sport, under the instrument of a governing body · https://www.usada.org/results/arbitration-decisions/ · 2026-09-10T00:00:00
- AAA No. 30 190 00170 07 · international sport, under the instrument of a governing body · https://www.usada.org/results/arbitration-decisions/ · 2026-09-10T00:00:00
- SR/007/2023 · United Kingdom · https://www.sportresolutions.com/disputes/anti-doping · 2026-09-10T00:00:00

### C1

For a given matter, what is the order of events from collection to decision, with the dates the decision states?

- AAA Case No. 30 190 00847 06 · 1 sample collection · 2006-07-20T00:00:00
- AAA Case No. 30 190 00847 06 · 3 notification · 2006-09-19T00:00:00
- AAA Case No. 30 190 00847 06 · 4 hearing · 2007-05-14T00:00:00

### C2

From whom was a given sample collected?

- 496040 · Justin Gatlin
- 4960404 · Justin Gatlin
- 995474 · Floyd Landis

### C3

Which person does a given adverse analytical finding concern?

- adverse analytical finding in American Arbitration Association case 30 190 00170 07 · Justin Gatlin
- adverse analytical finding in American Arbitration Association case 30 190 00847 06 · Floyd Landis
- adverse analytical finding in National Anti-Doping Panel (United Kingdom) SR/007/2023 · Emir Ahmatovic

### C4

Which laboratory analysed the sample in a given matter, and by what method?

- AAA No. 30 190 00170 07 · World Anti-Doping Agency accredited laboratory at the University of California in Los Angeles · carbon isotope ratio analysis
- AAA Case No. 30 190 00847 06 · Laboratoire National de Dépistage du Dopage · carbon isotope ratio analysis
- SR/007/2023 · Drug Control Centre, King's College London · None

### C5

Which matters record a provisional suspension, and does the period of ineligibility run from that date?

- SR/007/2023 · 2023-08-09T00:00:00 · None
- SR/056/2022 · 2022-03-04T00:00:00 · None

### C6

Which document opened a given proceeding, and when?

- determination of the matter in American Arbitration Association case 30 190 00847 06 · charge letter in American Arbitration Association case 30 190 00847 06 · 2006-09-19T00:00:00
- appeal proceeding in National Anti-Doping Panel Appeal Tribunal (United Kingdom) SR/015/2023 · notice of appeal in National Anti-Doping Panel Appeal Tribunal (United Kingdom) SR/015/2023 · 2023-01-18T00:00:00
- determination of the matter in National Anti-Doping Panel (United Kingdom) SR/007/2023 · charge letter in National Anti-Doping Panel (United Kingdom) SR/007/2023 · 2023-11-01T00:00:00

### C7

What portions does a sample have, what reference does each carry, and which portion was analysed?

- AAA Case No. 30 190 00847 06 · 995474 · true
- AAA No. 30 190 00170 07 · 496040 · true
- AAA No. 30 190 00170 07 · 4960404 · true

### D1

For a given individual in the procedural layer, which decision states it, and by what identifier can that decision be retrieved?

- https://w3id.org/adro/Substance_Oxandrolone_LTM · Agence française de lutte contre le dopage D. 2025-01
- https://w3id.org/adro/LaboratoryAnalysis_AAA_30_190_00170_07 · American Arbitration Association case 30 190 00170 07
- https://w3id.org/adro/AthleteRole_Justin_Gatlin · American Arbitration Association case 30 190 00170 07

### D2

Which decisions in the register carry no link to a substance?

- CAS (Oceania Registry) A2/2015 · Subject as stated in the award headnote: prohibited method: intravenous infusion of grape syrup and vitamins
- CAS 2005/A/884 · Subject as stated in the award headnote: homologous blood transfusion, HBT
- CAS 2005/C/976 · None

### D3

Is there a decision stating that a given person held no exemption for a named substance, and which substance is it?

- Emir Ahmatovic · Metandienone · As stated in National Anti-Doping Panel (United Kingdom) SR/007/2023: The Athlete did not have a Therapeutic Use Exemption for metandienone. The statement is recorded as the absence of an exemption for that substance, and not as the absence of any exemption.

### D4

Which kinds of analytical report does the regulation distinguish, and which does the ontology hold?

- adverse analytical finding · 4
- atypical finding · 0
- 비정상분석결과 · 4

### E1

Given a substance a decision names, which List entry, which category, which violation type and which Code article stand behind the determination?

- D. 2025-15 · Methylenedioxyamphetamine · The 2026 Prohibited List, S6.B · S6.B Specified stimulants · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · World Anti-Doping Code 2021, Article 2.1
- D. 2025-15 · Methylenedioxymethamphetamine · The 2026 Prohibited List, S6.B · S6.B Specified stimulants · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · World Anti-Doping Code 2021, Article 2.1
- D. 2025-15 · Amfetamine · The 2026 Prohibited List, S6.A · S6.A Non-specified stimulants · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · World Anti-Doping Code 2021, Article 2.1

### E2

Which violation types were determined under an instrument other than the Code, and under which instrument?

- AAA Case No. 30 190 00847 06 · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · UCI Anti-Doping Regulations, Article 15.1 · UCI Anti-Doping Regulations
- AAA Case No. 30 190 00847 06 · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · UCI Anti-Doping Regulations, Article 261 · UCI Anti-Doping Regulations
- D. 2025-01 · ADRV type: Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample · Code du sport, article L. 232-9 · Code du sport (France)
