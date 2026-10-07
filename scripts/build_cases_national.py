# -*- coding: utf-8 -*-
"""
Generates doping-ontology-cases-national.ttl

Decisions of national anti-doping organizations and of the bodies that hear
their cases at first instance. These are examples, not a corpus: they are
selected to exercise structures the appeal register alone cannot exercise, and
they carry no frequency or distribution claim.

Selection is stated in reports/national-examples-report.md. Every field below
is taken from the wording of the decision itself. Where a decision does not
state a field, the field is omitted rather than supplied from elsewhere.

Provenance is by issuing institution and the identifier that institution
prints on the decision, so that a reader can retrieve the original.
"""
import sys

ORGS = [
 ("UKAD", "adro:NationalAntiDopingOrganization", "UK Anti-Doping", None),
 ("NADP", "adro:Organization", "National Anti-Doping Panel (United Kingdom)",
  "The tribunal that hears at first instance the charges UK Anti-Doping brings."),
 ("NADPAppealTribunal", "adro:Organization",
  "National Anti-Doping Panel Appeal Tribunal (United Kingdom)", None),
 ("AFLD", "adro:NationalAntiDopingOrganization",
  "Agence française de lutte contre le dopage", None),
 ("USADA", "adro:NationalAntiDopingOrganization", "United States Anti-Doping Agency", None),
 ("AAA_NACAS", "adro:Organization",
  "North American Court of Arbitration for Sport Panel of the American Arbitration Association",
  "The panel that hears at first instance the charges the United States Anti-Doping Agency brings."),
]

# (local, class, label, title, comment)
INSTRUMENTS = [
 ("ISTUE", "adro:InternationalStandard",
  "International Standard for Therapeutic Use Exemptions",
  None, "Incorporated into the UK Anti-Doping Rules by Article 4.1, which states that the standard is binding on all Athletes and other Persons in the same way as the Rules are binding on them."),
 ("UKADRules_2021", "adro:NationalAntiDopingRule", "UK Anti-Doping Rules, 1 January 2021",
  None, None),
 ("CodeDuSport", "adro:NationalLegislation", "Code du sport (France)",
  None, "The French state legislates on doping. A decision of the Agence française de lutte contre le dopage cites the statute, not the Code."),
 ("UCIADR", "adro:SportGoverningBodyRule", "UCI Anti-Doping Regulations",
  None, None),
 ("BBBofC_ADR", "adro:SportGoverningBodyRule",
  "Anti-Doping Rules of the British Boxing Board of Control", None, None),
 ("RFL_ADR", "adro:SportGoverningBodyRule",
  "Anti-Doping Rules of the Rugby Football League", None, None),
]

# instrument adoption, each grounded in the wording of a decision
ADOPTS = [
 ("RFL_ADR", "UKADRules_2021", "National Anti-Doping Panel (United Kingdom) SR/056/2022",
  "The Rugby Football League has delegated the conduct of its anti-doping programme to "
  "UK Anti-Doping Limited and has adopted the UK Anti-Doping Rules"),
 ("BBBofC_ADR", "UKADRules_2021", "National Anti-Doping Panel (United Kingdom) SR/007/2023",
  "proceedings brought under the anti-doping rules of the British Boxing Board of Control "
  "to determine an Anti-Doping Rule Violation under Article 8.1 of the UK Anti-Doping Rules "
  "dated 1 January 2021"),
]

# (local, label, title, parent instrument, Code article implemented or None, note)
PROVISIONS = [
 ("UKAD_ADR_4_1", "UK Anti-Doping Rules 2021, Article 4.1",
  "Incorporation of the International Standard for Therapeutic Use Exemptions",
  "UKADRules_2021", None,
  "The provision states that the standard sets out the circumstances in which Athletes may be granted permission to Use, for therapeutic purposes, substances or methods on the Prohibited List the Use of which would otherwise be prohibited."),
 ("UKAD_ADR_4_2_1", "UK Anti-Doping Rules 2021, Article 4.2.1",
  "Scope and effect of therapeutic use exemptions",
  "UKADRules_2021", None,
  "The provision states that the presence, Use or Attempted Use, Possession or Administration of a Prohibited Substance or Prohibited Method shall not be considered an Anti-Doping Rule Violation if it is consistent with the provisions of a TUE validly granted. This is why an exemption belongs in the ontology: it defeats the prohibition stated in the same instrument."),
 ("UKAD_ADR_4_4", "UK Anti-Doping Rules 2021, Article 4.4",
  "Grant of a therapeutic use exemption",
  "UKADRules_2021", None,
  "The provision states that a decision to grant must specify the dosage, frequency, route and duration of Administration permitted, and that a decision to deny must include the reasons for the denial. No correspondence to a Code article is asserted, because the instrument does not state which article it restates."),
 ("UKAD_ADR_2_1", "UK Anti-Doping Rules 2021, Article 2.1",
  "Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample",
  "UKADRules_2021", "Article_2021_Presence", None),
 ("UKAD_ADR_2_2", "UK Anti-Doping Rules 2021, Article 2.2",
  "Use or Attempted Use by an Athlete of a Prohibited Substance or a Prohibited Method",
  "UKADRules_2021", "Article_2021_Use", None),
 ("UKAD_ADR_10_2_3", "UK Anti-Doping Rules 2021, Article 10.2.3",
  "Period of Ineligibility where the violation is not intentional",
  "UKADRules_2021", None, None),
 ("UKAD_ADR_10_4", "UK Anti-Doping Rules 2021, Article 10.4",
  "Elimination of the period of Ineligibility, and aggravating circumstances",
  "UKADRules_2021", None, None),
 ("UKAD_ADR_10_5", "UK Anti-Doping Rules 2021, Article 10.5",
  "Reduction of the period of Ineligibility for No Significant Fault or Negligence",
  "UKADRules_2021", None, None),
 ("UKAD_ADR_10_2_1a", "UK Anti-Doping Rules 2021, Article 10.2.1(a)",
  "Period of Ineligibility where the violation does not involve a Specified Substance and is intentional",
  "UKADRules_2021", None, None),
 ("CodeDuSport_L232_9", "Code du sport, article L. 232-9",
  "Présence d'une ou plusieurs substances ou méthodes interdites dans l'échantillon",
  "CodeDuSport", "Article_2021_Presence",
  "The correspondence is asserted because the decisions themselves gloss the article in the "
  "wording of Code Article 2.1."),
 ("UCI_ADR_15_1", "UCI Anti-Doping Regulations, Article 15.1",
  "Anti-doping rule violation established by the presence of a prohibited substance",
  "UCIADR", None,
  "No correspondence to a Code article is asserted. The decision applying this provision "
  "predates the 2021 Code, and the Code articles in this ontology are parts of the 2021 "
  "edition. A correspondence holds only between an instrument and the Code edition it restates."),
 ("UCI_ADR_261", "UCI Anti-Doping Regulations, Article 261",
  "Period of ineligibility for a first violation", "UCIADR", None, None),
]


# Jurisdictions, each taken from the scope provision of the instrument that
# states it. A jurisdiction is a designation of who and where an instrument
# binds, not a place.
JURISDICTIONS = [
 ("Jurisdiction_UK", "United Kingdom",
  "UK Anti-Doping Rules 2021, Article 1.5",
  "These Rules apply to all Athletes and Athlete Support Personnel who are members of the NGB "
  "and/or of the NGB's members or affiliate organisations or licensees, or otherwise under the "
  "jurisdiction of the NGB."),
 ("Jurisdiction_France", "France",
  "Code du sport",
  "The code du sport is enacted by the French state and binds within its territory."),
 ("Jurisdiction_International", "international sport, under the instrument of a governing body",
  "UCI Anti-Doping Regulations",
  "The regulations of an international federation bind the persons under that federation "
  "wherever they are."),
]

INSTRUMENT_JURISDICTION = {
 "UKADRules_2021": "Jurisdiction_UK",
 "BBBofC_ADR": "Jurisdiction_UK",
 "RFL_ADR": "Jurisdiction_UK",
 "CodeDuSport": "Jurisdiction_France",
 "UCIADR": "Jurisdiction_International",
}

# Grounds that lengthen or shorten a sanction, in the wording of the instrument
# that defines them.
GROUNDS = [
 ("Ground_NoFault", "No Fault or Negligence", "UKAD_ADR_10_4",
  "The Athlete or other Person establishing that they did not know or suspect, and could not "
  "reasonably have known or suspected, even with the exercise of utmost caution, that they had "
  "Used or been administered the Prohibited Substance or Prohibited Method or otherwise violated "
  "an anti-doping rule."),
 ("Ground_NoSignificantFault", "No Significant Fault or Negligence", "UKAD_ADR_10_5",
  "The Athlete or other Person's establishing that any Fault or negligence, when viewed in the "
  "totality of the circumstances and taking into account the criteria for No Fault or Negligence, "
  "was not significant in relation to the Anti-Doping Rule Violation."),
 ("Ground_Aggravating", "Aggravating Circumstances", "UKAD_ADR_10_4",
  "Circumstances involving, or actions by, an Athlete or other Person which may justify the "
  "imposition of a period of Ineligibility greater than the standard sanction."),
 ("Ground_NotIntentional", "violation not intentional", "UKAD_ADR_10_2_3",
  "Where the Athlete or other Person establishes that the Anti-Doping Rule Violation was not "
  "intentional, the period of Ineligibility is two years rather than four."),
]

# Grounds a decision records as raised, and whether the deciding body accepted them.
GROUNDS_RAISED = [
 ("NADP_SR_389_2024", "Ground_NotIntentional", False,
  "the Appellant failed to discharge the burden of establishing on the balance of probability "
  "that his ADRVs were not intentional within the meaning of ADR Article 10.2.3"),
 ("NADP_SR_015_2023", "Ground_NoFault", False,
  "Mr Kaye does not contend before the Appeal Tribunal that the sanction should be eliminated "
  "or reduced by reason of No Fault or Negligence or No Significant Fault or Negligence"),
 ("NADP_SR_015_2023", "Ground_NoSignificantFault", False,
  "Mr Kaye does not contend before the Appeal Tribunal that the sanction should be eliminated "
  "or reduced by reason of No Fault or Negligence or No Significant Fault or Negligence"),
 ("NADP_SR_015_2023", "Ground_NotIntentional", False,
  "he accepted before the Tribunal below, and on appeal, that he does not know and cannot prove "
  "how the Prohibited Substance entered his body"),
]

SPORTS = [("Rugby_league", "Rugby league"), ("Field_hockey", "Field hockey")]

# Each decision, as the document states it.
DECISIONS = [
 dict(local="NADP_SR_007_2023", cls="adro:FirstInstanceDecision",
      ident="SR/007/2023", body="NADP", date="2024-10-18",
      title="UK Anti-Doping v Emir Ahmatovic",
      sport="Sport_Boxing", instrument="BBBofC_ADR",
      provisions=["UKAD_ADR_2_1", "UKAD_ADR_2_2"],
      adrv=["ADRVType_Presence", "ADRVType_Use"],
      mentions=["Substance_Metandienone_LTM", "Substance_Metandienone"],
      sanctions=["SanctionType_Ineligibility", "SanctionType_Disqualification"],
      months=48, status="Final",
      note="Two violations determined on one sample: presence of the metabolite, and use of "
           "the parent substance. The decision is the example of a single sample supporting "
           "more than one violation type.",
      date_note=None),
 dict(local="NADP_SR_389_2024", cls="adro:AppealDecision",
      ident="SR/389/2024", body="NADPAppealTribunal", date="2025-04-01",
      title="Emir Ahmatovic v UK Anti-Doping",
      sport="Sport_Boxing", instrument="BBBofC_ADR",
      provisions=["UKAD_ADR_2_1", "UKAD_ADR_2_2", "UKAD_ADR_10_2_1a"],
      adrv=["ADRVType_Presence", "ADRVType_Use"],
      mentions=["Substance_Metandienone_LTM", "Substance_Metandienone"],
      sanctions=["SanctionType_Ineligibility", "SanctionType_Disqualification"],
      months=48, status="Final", appeals="NADP_SR_007_2023",
      effective=("2023-08-09", "2027-08-08"),
      note="The appeal tribunal confirmed the violations and the period of ineligibility.",
      date_note=None),
 dict(local="NADP_SR_056_2022", cls="adro:FirstInstanceDecision",
      ident="SR/056/2022", body="NADP", date="2023-01-04",
      title="UK Anti-Doping v Rowland Kaye",
      sport="Sport_Rugby_league", instrument="RFL_ADR",
      provisions=["UKAD_ADR_2_1"], adrv=["ADRVType_Presence"],
      mentions=["Substance_Oxymetholone_Methasterone_LTM"],
      sanctions=["SanctionType_Ineligibility"], months=48, status="Final",
      note="The charge names a metabolite whose parent substance the deciding body records "
           "as indeterminate between two listed substances. The decision is the example of a "
           "violation established without identifying a single Prohibited List entry.",
      date_note=None),
 dict(local="NADP_SR_015_2023", cls="adro:AppealDecision",
      ident="SR/015/2023", body="NADPAppealTribunal", date="2023-04-26",
      title="Rowland Kaye v UK Anti-Doping",
      sport="Sport_Rugby_league", instrument="RFL_ADR",
      provisions=["UKAD_ADR_2_1"], adrv=["ADRVType_Presence"],
      mentions=["Substance_Oxymetholone_Methasterone_LTM"],
      sanctions=["SanctionType_Ineligibility"], months=48, status="Final",
      appeals="NADP_SR_056_2022", effective=("2022-03-04", "2026-03-03"),
      note="The appeal was dismissed and the period of ineligibility confirmed.",
      date_note=None),
 dict(local="AFLD_D_2025_01", cls="adro:FirstInstanceDecision",
      ident="D. 2025-01", body="AFLD", date="2025-01-06",
      title="Décision D. 2025-01 relative à M. Kamel Balil",
      sport="Sport_Boxing", instrument="CodeDuSport",
      provisions=["CodeDuSport_L232_9"], adrv=["ADRVType_Presence"],
      mentions=["Substance_Oxandrolone_LTM", "Substance_Oxandrolone"],
      sanctions=["SanctionType_Ineligibility", "SanctionType_Disqualification"],
      months=24, status="Final", effective=("2024-06-25", "2026-06-25"),
      note="A violation determined under national legislation rather than under the Code.",
      date_note=None),
 dict(local="AFLD_D_2025_15", cls="adro:FirstInstanceDecision",
      ident="D. 2025-15", body="AFLD", date="2025-03-20",
      title="Décision D. 2025-15 relative à M. Paul Mathon",
      sport="Sport_Field_hockey", instrument="CodeDuSport",
      provisions=["CodeDuSport_L232_9"], adrv=["ADRVType_Presence"],
      mentions=["Substance_Amfetamine", "Substance_Methylenedioxymethamphetamine",
                "Substance_Methylenedioxyamphetamine"],
      sanctions=["SanctionType_Ineligibility"], months=36, status="Final",
      effective=("2024-05-03", "2027-05-03"),
      note="Three listed substances in one sample, each named with its List section in the "
           "decision. The decision is the example of a single determination resting on more "
           "than one Prohibited List entry.",
      date_note=None),
 dict(local="AAA_30_190_00847_06", cls="adro:FirstInstanceDecision",
      ident="AAA Case No. 30 190 00847 06", body="AAA_NACAS", date="2007-09-20",
      title="United States Anti-Doping Agency v. Floyd Landis",
      sport="Sport_Cycling", instrument="UCIADR",
      provisions=["UCI_ADR_15_1", "UCI_ADR_261"], adrv=["ADRVType_Presence"],
      mentions=["Substance_Testosterone"],
      sanctions=["SanctionType_Ineligibility", "SanctionType_Disqualification"],
      months=24, status="Final", effective=("2007-01-30", "2009-01-29"),
      appealed_by="Decision_CAS_2007_A_1394",
      note="The panel dismissed the charge founded on the ratio of testosterone to "
           "epitestosterone and upheld the charge founded on carbon isotope ratio analysis. "
           "The decision is the example of a determination in which one analytical charge "
           "fails and another succeeds on the same sample.",
      date_note=None),
 dict(local="AAA_30_190_00170_07", cls="adro:FirstInstanceDecision",
      ident="AAA No. 30 190 00170 07", body="AAA_NACAS", date=None,
      title="United States Anti-Doping Agency v. Justin Gatlin",
      sport="Sport_Athletics", instrument=None,
      provisions=[], adrv=["ADRVType_Presence"],
      mentions=["Substance_Testosterone"],
      sanctions=["SanctionType_Ineligibility", "SanctionType_Disqualification"],
      months=48, status="Final", appealed_by="Decision_CAS_2008_A_1461",
      note="The period of ineligibility runs from a date thirty days after the sample was "
           "taken, and the panel treated an earlier finding as a first violation.",
      date_note="The award as published states no date of issue, so none is asserted."),
]

HEAD = """@prefix adro: <https://w3id.org/adro/> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/adro/cases-national> a owl:Ontology ;
    owl:imports <https://w3id.org/adro/cases-cas> , <https://w3id.org/adro/analytes> ;
    dcterms:title "Anti-Doping Regulation Ontology: decisions of national bodies, as examples"@en ;
    rdfs:comment "Generated by scripts/build_cases_national.py. These decisions are examples selected to exercise structures the appeal register does not exercise. They are not a corpus and support no claim about frequency or distribution. Selection and per-field sourcing are stated in reports/national-examples-report.md."@en .

"""

def esc(s):
    return s.replace('"', "'")

def dt(d):
    return f'"{d}T00:00:00"^^xsd:dateTime'

def main(out, report):
    o = [HEAD]
    o.append("########  Bodies  ########\n\n")
    for local, cls, label, note in ORGS:
        o.append(f'adro:{local} a {cls} ;\n    rdfs:label "{label}"@en')
        o.append(f' ;\n    rdfs:comment "{note}"@en' if note else "")
        o.append(" .\n\n")

    o.append("########  Instruments and their provisions  ########\n\n")
    for local, cls, label, title, note in INSTRUMENTS:
        o.append(f'adro:{local} a {cls} ;\n    rdfs:label "{label}"@en')
        if title:
            o.append(f' ;\n    dcterms:title "{title}"@en')
        if note:
            o.append(f' ;\n    rdfs:comment "{note}"@en')
        o.append(" .\n\n")
    for child, parent, src, wording in ADOPTS:
        o.append(f'adro:{child} adro:adoptsInstrument adro:{parent} .\n')
        o.append(f'adro:{child} rdfs:comment "As stated in {src}: {wording}."@en .\n\n')
    for local, label, title, inst, code, note in PROVISIONS:
        o.append(f'adro:{local} a adro:InstrumentProvision ;\n'
                 f'    rdfs:label "{label}"@en ;\n'
                 f'    dcterms:title "{title}"@en ;\n'
                 f'    obo:BFO_0000176 adro:{inst}')
        if code:
            o.append(f' ;\n    adro:implementsCodeArticle adro:{code}')
        if note:
            o.append(f' ;\n    rdfs:comment "{note}"@en')
        o.append(" .\n\n")

    o.append("########  Jurisdictions  ########\n\n")
    for jid, label, src, wording in JURISDICTIONS:
        o.append(f'adro:{jid} a adro:Jurisdiction ;\n'
                 f'    rdfs:label "{label}"@en ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(wording)}."@en .\n\n')
    for inst, jid in INSTRUMENT_JURISDICTION.items():
        o.append(f'adro:{inst} adro:bindsWithin adro:{jid} .\n')
    o.append("\n")

    o.append("########  Grounds that lengthen or shorten a sanction  ########\n\n")
    for gid, label, prov, wording in GROUNDS:
        o.append(f'adro:{gid} a adro:SanctionModifyingGround ;\n'
                 f'    rdfs:label "{label}"@en ;\n'
                 f'    adro:definedIn adro:{prov} ;\n'
                 f'    rdfs:comment "As stated in the instrument: {esc(wording)}."@en .\n\n')
    for case, gid, accepted, wording in GROUNDS_RAISED:
        rel = "acceptsGround" if accepted else "raisesGround"
        o.append(f'adro:Decision_{case} adro:{rel} adro:{gid} ;\n'
                 f'    rdfs:comment "Ground raised and {"accepted" if accepted else "not established"}: {esc(wording)}."@en .\n\n')

    o.append("########  Sports not already named in the appeal register  ########\n\n")
    for local, label in SPORTS:
        o.append(f'adro:Sport_{local} a adro:Sport ;\n    rdfs:label "{label}"@en .\n\n')

    o.append("########  Decisions  ########\n\n")
    for d in DECISIONS:
        L = d["local"]
        types = [d["cls"]]
        if d.get("sanctions"):
            types.append("adro:SanctionDecision")
        o.append(f'adro:Decision_{L} a {" , ".join(types)} ;\n')
        o.append(f'    rdfs:label "{d["ident"]}"@en ;\n')
        o.append(f'    dcterms:title "{d["title"]}"@en ;\n')
        o.append(f'    adro:issuedBy adro:{d["body"]} ;\n')
        o.append(f'    adro:hasCaseIdentifier "{d["ident"]}"')
        if d["date"]:
            o.append(f' ;\n    adro:hasDecisionDate {dt(d["date"])}')
        for p in d["provisions"]:
            o.append(f' ;\n    adro:appliedProvision adro:{p}')
        for a in d["adrv"]:
            o.append(f' ;\n    adro:assignsType adro:{a}')
        for m in d["mentions"]:
            o.append(f' ;\n    adro:mentions adro:{m}')
        for s in d["sanctions"]:
            o.append(f' ;\n    adro:hasSanctionType adro:{s}')
        if d.get("appeals"):
            o.append(f' ;\n    adro:appealsAgainst adro:Decision_{d["appeals"]}')
        if d.get("months"):
            o.append(f' ;\n    adro:establishes adro:Ineligibility_{L}')
        o.append(f' ;\n    rdfs:comment "{d["note"]}"@en')
        if d.get("date_note"):
            o.append(f' ;\n    rdfs:comment "{d["date_note"]}"@en')
        o.append(" .\n\n")

        if d.get("months"):
            o.append(f'adro:Ineligibility_{L} a adro:IneligibilityStatus ;\n'
                     f'    rdfs:label "ineligibility established by {d["ident"]}"@en ;\n'
                     f'    adro:hasIneligibilityDurationInMonths "{d["months"]}"^^xsd:decimal')
            if d.get("effective"):
                a, b = d["effective"]
                o.append(f' ;\n    adro:hasEffectiveFrom {dt(a)} ;\n    adro:hasEffectiveTo {dt(b)}')
            o.append(" .\n\n")

        o.append(f'adro:CaseRecord_{L} a adro:CaseRecord ;\n'
                 f'    rdfs:label "case record for {d["ident"]}"@en ;\n'
                 f'    obo:IAO_0000136 adro:Decision_{L} ;\n'
                 f'    adro:resultsManagementAuthority adro:{d["body"]} ;\n'
                 f'    adro:caseStatus adro:CaseStatus_{d["status"]} ;\n'
                 f'    adro:concernsSport adro:{d["sport"]} ;\n'
                 f'    adro:hasCaseIdentifier "{d["ident"]}" .\n\n')

    o.append("########  Appeals taken from these decisions to the Court of Arbitration for Sport  ########\n\n")
    for d in DECISIONS:
        if d.get("appealed_by"):
            o.append(f'adro:{d["appealed_by"]} adro:appealsAgainst adro:Decision_{d["local"]} .\n')
    o.append("\n")

    open(out, "w", encoding="utf-8").write("".join(o))

    # report
    r = ["# National decisions included as examples\n",
         "\nThese decisions are examples. They are not a corpus, they are not a sample of one,",
         " and no statement about how often anything occurs may be drawn from them.",
         " Each was selected because it exercises a structure the appeal register does not exercise.\n",
         "\n## The decisions\n\n",
         "| issuing body | identifier | date | what it exercises |\n|---|---|---|---|\n"]
    names = {k: v for k, _, v, _ in ORGS}
    for d in DECISIONS:
        r.append(f'| {names[d["body"]]} | {d["ident"]} | {d["date"] or "not stated in the document"} '
                 f'| {d["note"].split(". ")[-1].rstrip(".")} |\n')
    r.append("\n## Where each decision is published\n\n"
             "| issuing body | published by | how to retrieve |\n|---|---|---|\n"
             "| National Anti-Doping Panel (United Kingdom) | Sport Resolutions, on behalf of the "
             "panel | by the SR reference printed on the first page |\n"
             "| Agence française de lutte contre le dopage | the agency, in its register of "
             "disciplinary decisions | by the decision number D. yyyy-nn |\n"
             "| North American Court of Arbitration for Sport Panel of the American Arbitration "
             "Association | the United States Anti-Doping Agency, in its register of arbitration "
             "decisions | by the American Arbitration Association case number |\n")

    r.append("\n## Decisions considered and not included\n\n"
             "Four first instance awards of the American Arbitration Association whose appeals "
             "are in the register were considered and left out: the documents as published carry "
             "no text layer, and transcribing them by optical recognition would put reading "
             "errors into the source data. They are the awards concerning Hamilton, Thompson, "
             "Trafeh and Gil Roberts.\n")

    r.append("\n## Fields omitted because the decision does not state them\n\n")
    for d in DECISIONS:
        if d.get("date_note"):
            r.append(f'- {d["ident"]}: {d["date_note"]}\n')
        if not d["provisions"]:
            r.append(f'- {d["ident"]}: no provision is asserted, because the award as '
                     f'published states no provision number for the violation found.\n')
    r.append("\n## Correspondence between an instrument provision and a Code article\n\n")
    r.append("| provision | Code article | basis |\n|---|---|---|\n")
    for local, label, title, inst, code, note in PROVISIONS:
        basis = note or ("The provision carries the Code's own numbering and wording."
                         if code else "")
        r.append(f'| {label} | {code.replace("Article_2021_", "2021 Code, ") if code else "not asserted"} | {basis} |\n')
    open(report, "w", encoding="utf-8").write("".join(r))
    print("decisions", len(DECISIONS), "instruments", len(INSTRUMENTS),
          "provisions", len(PROVISIONS))

main(sys.argv[1], sys.argv[2])
