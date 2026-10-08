# -*- coding: utf-8 -*-
"""
Generates doping-ontology-procedure.ttl

The course of a matter as a first instance decision records it: the person
tested, the sample, its collection, the laboratory and its analysis, the
finding, the notice of charge, the provisional suspension and the hearing.

Every field below is a statement of the decision named in its source line.
Where a decision does not state a field, the field is absent. Nothing here is
supplied from another document, from a register, or from inference.

Fields deliberately not asserted are listed in
reports/procedure-extraction-report.md with the reason.
"""
import sys

# case -> the decision individual it belongs to, and the wording sourced
# The jurisdiction each matter fell under, and where the decision was obtained.
CASE_CONTEXT = {
 "NADP_SR_007_2023": dict(jurisdiction="Jurisdiction_UK",
   url="https://www.sportresolutions.com/disputes/anti-doping", retrieved="2026-09-10"),
 "NADP_SR_056_2022": dict(jurisdiction="Jurisdiction_UK",
   url="https://www.sportresolutions.com/disputes/anti-doping", retrieved="2026-09-10"),
 "AAA_30_190_00847_06": dict(jurisdiction="Jurisdiction_International",
   url="https://www.usada.org/results/arbitration-decisions/", retrieved="2026-09-10"),
 "AAA_30_190_00170_07": dict(jurisdiction="Jurisdiction_International",
   url="https://www.usada.org/results/arbitration-decisions/", retrieved="2026-09-10"),
}

CASES = {
 "NADP_SR_007_2023": dict(
   src="National Anti-Doping Panel (United Kingdom) SR/007/2023",
   person=("Emir_Ahmatovic", "Emir Ahmatovic"),
   collection=dict(date="2023-06-09", place="York Hall, London",
     quote="On 9 June 2023, UKAD Doping Control Personnel collected a urine Sample from "
           "the Athlete following a heavyweight bout at York Hall, London",
     context="CompetitionContext_InCompetition",
     context_quote="the Sample was collected In-Competition"),
   samples=[("A", "A1182501"), ("B", "B1182501")],
   lab=("DrugControlCentre_KCL", "Drug Control Centre, King's College London",
     "Both Samples were transported to the World Anti-Doping Agency accredited "
     "laboratory, the Drug Control Centre, King's College London"),
   analysis=dict(sample="A", method=None,
     quote="The A Sample was analysed in accordance with WADA's International Standard "
           "for Laboratories"),
   finding=dict(substance="Substance_Metandienone_LTM", value="2.2",
     unit="NanogramPerMillilitre", matrix="Urine",
     quote="Analysis of the A Sample returned an AAF for "
           "17β-hydroxymethyl,17α-methyl-18-norandrost-1,4,13-trien-3-one, a "
           "Metabolite of metandienone at an estimated concentration of 2.2 ng/mL"),
   list_edition=("ProhibitedList_2023", "World Anti-Doping Agency 2023 Prohibited List",
     "Metandienone is listed under section 1.1 of the WADA 2023 Prohibited List as an "
     "Anabolic Androgenic Steroid. It is a non-Specified Substance that is prohibited at "
     "all times"),
   list_text=dict(src="World Anti-Doping Agency, The 2023 Prohibited List",
     effective_from="2023-01-01",
     effective_quote="This List shall come into effect on 1 January 2023",
     entries=[("Entry_2023_S1_1", "S1.1", "Anabolic androgenic steroids (AAS)",
               "Metandienone", "Metandienone", "Category_S1_1", "Context_AtAllTimes",
               "PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION)")]),
   notices=[("Notice", "2023-08-09",
     "On 9 August 2023, UKAD sent a letter (the 'Notice Letter') to the Athlete formally "
     "notifying him that he may have committed"),
            ("Charge", "2023-11-01",
     "the Athlete was charged by letter dated 1 November 2023")],
   provisional=("2023-08-09",
     "The Notice Letter also provisionally suspended the Athlete from all sport with "
     "immediate effect from 9 August 2023"),
   hearing=("2024-09-13", None,
     "The Athlete attended in person at a remote hearing, convened on 13 September 2024"),
 ),
 "NADP_SR_056_2022": dict(
   src="National Anti-Doping Panel (United Kingdom) SR/056/2022",
   person=("Rowland_Kaye", "Rowland Kaye"),
   collection=dict(date="2022-01-05", place="the Hunslet RLFC ground",
     quote="On 5 January 2022 a UKAD Doping Control Officer attended the Hunslet RLFC "
           "ground in order to carry out testing. Mr Kaye was selected to take a urine "
           "test. He completed the Doping Control Form and provided a urine Sample",
     context=None, context_quote=None),
   samples=[("A", "A1164806")],
   lab=None,
   analysis=dict(sample="A", method=None,
     quote="The laboratory test report for the A Sample was provided to UKAD on 1 March 2022"),
   finding=dict(substance="Substance_Oxymetholone_Methasterone_LTM", value=None, unit=None,
     quote="It revealed that it contained a small quantity of the Metabolite"),
   list_edition=None,
   notices=[("Notice", "2022-03-04",
     "Mr Kaye was informed of the positive test by letter of 4 March 2022")],
   provisional=("2022-03-04",
     "The Ineligibility will run from 4 March 2022, that is the date of Mr Kaye's "
     "provisional suspension"),
   hearing=("2022-12-14", None,
     "We held a remote hearing on Zoom with the consent of the parties for a full day on "
     "14 December 2022"),
 ),
 "AAA_30_190_00847_06": dict(
   src="American Arbitration Association case 30 190 00847 06",
   person=("Floyd_Landis", "Floyd Landis"),
   collection=dict(date="2006-07-20", place="the Doping Control Station in Morzine Avoriaz",
     quote="a sample was collected from the Respondent at approximately 5:55 p.m. on 20 "
           "July 2006 at the Doping Control Station in Morzine Avoriaz following Stage 17 "
           "of the Tour",
     context="CompetitionContext_InCompetition",
     context_quote="The violation of the UCI Rules having occurred as a result of an "
                   "In-Competition test"),
   samples=[("A", "995474")],
   lab=("LNDD", "Laboratoire National de Dépistage du Dopage",
     "the Sample was then transported by courier, helicopter, and private plane to Paris "
     "where it was received by LNDD"),
   analysis=dict(sample="A", method="carbon isotope ratio analysis",
     quote="The charge of exogenous testosterone being found in the sample by the Carbon "
           "Isotope Ratio analysis is established in accordance with the UCI Anti-Doping "
           "Regulations"),
   finding=dict(substance="Substance_Testosterone", value=None, unit=None,
     quote="exogenous testosterone being found in the sample by the Carbon Isotope Ratio "
           "analysis"),
   list_edition=None,
   notices=[("Charge", "2006-09-19",
     "On 19 September 2006 USADA issued the charging letter")],
   provisional=None,
   hearing=("2007-05-14", "2007-05-23",
     "the arbitration hearing held from May 14-23, 2007"),
 ),
 "AAA_30_190_00170_07": dict(
   src="American Arbitration Association case 30 190 00170 07",
   person=("Justin_Gatlin", "Justin Gatlin"),
   collection=dict(date="2006-04-22", place="the Kansas Relays",
     quote="on April 22, 2006 at the Kansas Relays, Mr. Gatlin gave the urine sample "
           "designated by USADA as USADA specimen number 4960404",
     context="CompetitionContext_InCompetition",
     context_quote="the sample was given at the Kansas Relays"),
   samples=[("A", "496040")],
   sample_note="The award prints the specimen number as 4960404 once, where the sample is "
               "first identified, and as 496040 in every later mention. The form printed "
               "once is read as a misprint and is not recorded as an identifier.",
   lab=("UCLA_Laboratory", "World Anti-Doping Agency accredited laboratory at the "
        "University of California in Los Angeles",
     "the chain of custody for USADA specimen number 496040 from the time of collection "
     "and processing at the collection site to the receipt of the sample by the World "
     "Anti-Doping Agency accredited laboratory at the University of California in Los "
     "Angeles"),
   analysis=dict(sample="A", method="carbon isotope ratio analysis",
     quote="the UCLA Laboratory, through accepted scientific procedures and without error, "
           "accurately determined by carbon isotope ratio analysis the sample positive for "
           "the finding of the substance testosterone or its precursors"),
   finding=dict(substance="Substance_Testosterone", value=None, unit=None,
     quote="the sample positive for the finding of the substance testosterone or its "
           "precursors, which are prohibited as an androgenic anabolic agent under the "
           "applicable rules, in both the A and B bottles"),
   list_edition=None,
   notices=[],
   provisional=None,
   hearing=("2007-07-30", "2007-08-01",
     "after hearing held from July 30, 2007 through August 1, 2007"),
 ),
}

# Appeal proceedings, as the appeal decisions record them.
APPEALS = [
 dict(case="NADP_SR_389_2024", person="Emir_Ahmatovic",
      src="National Anti-Doping Panel Appeal Tribunal (United Kingdom) SR/389/2024",
      notice=("2024-11-07",
        "The Appellant appeals by way of a Notice and Grounds of Appeal dated 7 November 2024"),
      hearings=[("2025-03-12", "present at the hearing on 12 March 2025")]),
 dict(case="NADP_SR_015_2023", person="Rowland_Kaye",
      src="National Anti-Doping Panel Appeal Tribunal (United Kingdom) SR/015/2023",
      notice=("2023-01-18",
        "a Notice of Appeal was served by the Athlete on 18 January 2023"),
      hearings=[("2023-02-07", "A directions hearing took place before the Chair on 7 February 2023"),
                ("2023-04-04", "a final hearing before the Appeal Tribunal took place on 4 April 2023")]),
]

# documents on which a first instance determination was opened
OPENINGS = [
 ("NADP_SR_007_2023", "ChargeLetter_NADP_SR_007_2023",
  "the Athlete was charged by letter dated 1 November 2023",
  "National Anti-Doping Panel (United Kingdom) SR/007/2023"),
 ("AAA_30_190_00847_06", "ChargeLetter_AAA_30_190_00847_06",
  "On 19 September 2006 USADA issued the charging letter",
  "American Arbitration Association case 30 190 00847 06"),
]

# a decision's statement that a person held no exemption for a named substance
ABSENT_EXEMPTIONS = [
 ("Emir_Ahmatovic", "Substance_Metandienone",
  "National Anti-Doping Panel (United Kingdom) SR/007/2023",
  "The Athlete did not have a Therapeutic Use Exemption for metandienone"),
]

HEAD = """@prefix adro: <https://w3id.org/adro/> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/adro/procedure> a owl:Ontology ;
    owl:imports <https://w3id.org/adro/cases-national> ;
    dcterms:title "Anti-Doping Regulation Ontology: the course of a matter as first instance decisions record it"@en ;
    rdfs:comment "Generated by scripts/build_procedure.py. Every assertion reproduces a statement of the decision cited on it. Fields the decisions do not state are absent; see reports/procedure-extraction-report.md."@en .

"""

def dt(d):
    return f'"{d}T00:00:00"^^xsd:dateTime'

def esc(s):
    return s.replace('"', "'")

def main(out, report):
    o, r = [HEAD], []
    labs, counts = {}, dict(person=0, sample=0, collection=0, analysis=0,
                            finding=0, notice=0, provisional=0, hearing=0,
                            laboratory=0, measurement=0, edition=0)
    omitted = []

    for case, d in CASES.items():
        src = d["src"]
        o.append(f"########  {src}  ########\n\n")

        # person and the role borne while subject to regulation
        pid, pname = d["person"]
        counts["person"] += 1
        o.append(f'adro:Person_{pid} a adro:Person ;\n'
                 f'    rdfs:label "{pname}"@en ;\n'
                 f'    adro:bearerOfRole adro:AthleteRole_{pid} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" .\n\n')
        o.append(f'adro:AthleteRole_{pid} a adro:AthleteRole ;\n'
                 f'    rdfs:label "athlete role of {pname}"@en ;\n'
                 f'    obo:IAO_0000119 "{src}" .\n\n')

        # sample collection
        c = d["collection"]
        counts["collection"] += 1
        o.append(f'adro:SampleCollection_{case} a adro:SampleCollection ;\n'
                 f'    rdfs:label "sample collection in {src}"@en ;\n'
                 f'    obo:BFO_0000057 adro:Person_{pid} ;\n'
                 f'    adro:hasCollectionDateTime {dt(c["date"])} ;\n')
        o.append(f'    adro:hasCollectedSample adro:Sample_{case} ;\n')
        if c["context"]:
            o.append(f'    adro:competitionContext adro:{c["context"]} ;\n')
        o.append(f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(c["quote"])}."@en .\n\n')

        # one sample, split at collection into portions that each carry a reference
        counts["sample"] += 1
        o.append(f'adro:Sample_{case} a adro:UrineSample ;\n'
                 f'    rdfs:label "sample collected in {src}"@en ;\n')
        for kind, num in d["samples"]:
            o.append(f'    adro:hasPortion adro:SamplePortion_{case}_{kind} ;\n')
        o.append(f'    adro:isCollectedSampleOf adro:SampleCollection_{case} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" .\n\n')
        for kind, num in d["samples"]:
            counts["portion"] = counts.get("portion", 0) + 1
            o.append(f'adro:SamplePortion_{case}_{kind} a adro:SamplePortion ;\n'
                     f'    rdfs:label "{kind} portion {num} in {src}"@en ;\n'
                     f'    adro:hasSampleIdentifier "{num}" ;\n')
            if kind == "A" and d.get("sample_note"):
                o.append(f'    rdfs:comment "{esc(d["sample_note"])}"@en ;\n')
            o.append(f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                     f'    obo:IAO_0000119 "{src}" .\n\n')

        # laboratory
        if d["lab"]:
            lid, lname, lquote = d["lab"]
            if lid not in labs:
                labs[lid] = (lname, lquote, src)
                counts["laboratory"] += 1
        else:
            omitted.append((src, "laboratory",
                            "the decision refers to a WADA approved laboratory without naming it"))

        # analysis
        a = d["analysis"]
        counts["analysis"] += 1
        o.append(f'adro:LaboratoryAnalysis_{case} a adro:LaboratoryAnalysis ;\n'
                 f'    rdfs:label "analysis of the {a["sample"]} sample in {src}"@en ;\n'
                 f'    adro:hasSpecifiedInput adro:Sample_{case} ;\n'
                 f'    adro:hasSpecifiedInput adro:SamplePortion_{case}_{a["sample"]} ;\n')
        if a.get("date"):
            o.append(f'    adro:hasAnalysisDateTime {dt(a["date"])} ;\n')
        if a.get("method"):
            o.append(f'    adro:hasAnalyticalMethod "{a["method"]}" ;\n')
        if d["lab"]:
            o.append(f'    obo:BFO_0000057 adro:{d["lab"][0]} ;\n')
        o.append(f'    adro:hasSpecifiedOutput adro:Finding_{case} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(a["quote"])}."@en .\n\n')

        # the finding
        f = d["finding"]
        counts["finding"] += 1
        o.append(f'adro:Finding_{case} a adro:AdverseAnalyticalFinding ;\n'
                 f'    rdfs:label "adverse analytical finding in {src}"@en ;\n'
                 f'    obo:IAO_0000136 adro:Sample_{case} ;\n'
                 f'    adro:mentions adro:{f["substance"]} ;\n'
                 f'    adro:isEvidenceFor adro:Determination_{case} ;\n')
        if f["value"]:
            o.append(f'    obo:IAO_0000136 adro:Measurement_{case} ;\n')
        o.append(f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(f["quote"])}."@en .\n\n')
        if f["value"]:
            counts["measurement"] += 1
            o.append(f'adro:Measurement_{case} a adro:Measurement ;\n'
                     f'    rdfs:label "estimated concentration reported in {src}"@en ;\n'
                     f'    adro:hasMeasuredValue "{f["value"]}"^^xsd:decimal ;\n'
                     f'    adro:hasMeasurementUnit adro:Unit_{f["unit"]} ;\n'
                     f'    adro:hasSpecimenMatrix adro:Matrix_{f["matrix"]} ;\n'
                     f'    adro:measuresAnalyte adro:{f["substance"]} ;\n'
                     f'    obo:IAO_0000119 "{src}" .\n\n')
        else:
            omitted.append((src, "measured concentration",
                            "the decision reports the finding without a stated concentration"))

        # the determination the decision is the outcome of
        o.append(f'adro:Determination_{case} a adro:ADRVDeterminationProcess ;\n'
                 f'    rdfs:label "determination of the matter in {src}"@en ;\n'
                 f'    obo:BFO_0000057 adro:Person_{pid} ;\n'
                 f'    adro:hasSpecifiedOutput adro:Decision_{case} ;\n'
                 f'    obo:BFO_0000117 adro:Hearing_{case} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" .\n\n')

        # the hearing
        h = d["hearing"]
        counts["hearing"] += 1
        o.append(f'adro:Hearing_{case} a adro:Hearing ;\n'
                 f'    rdfs:label "hearing in {src}"@en ;\n'
                 f'    adro:hasStartDateTime {dt(h[0])} ;\n')
        if h[1]:
            o.append(f'    adro:hasEndDateTime {dt(h[1])} ;\n')
        o.append(f'    obo:BFO_0000057 adro:Person_{pid} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(h[2])}."@en .\n\n')

        # notices
        for kind, date, quote in d["notices"]:
            counts["notice"] += 1
            o.append(f'adro:{kind}Letter_{case} a adro:NotificationOfCharge ;\n'
                     f'    rdfs:label "{kind.lower()} letter in {src}"@en ;\n'
                     f'    adro:hasIssueDateTime {dt(date)} ;\n'
                     f'    adro:concernsPerson adro:Person_{pid} ;\n'
                     f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                     f'    obo:IAO_0000119 "{src}" ;\n'
                     f'    rdfs:comment "As stated in {src}: {esc(quote)}."@en .\n\n')
        if not d["notices"]:
            omitted.append((src, "notice of charge",
                            "the award records no date on which the person was notified"))

        # provisional suspension
        if d["provisional"]:
            date, quote = d["provisional"]
            counts["provisional"] += 1
            o.append(f'adro:ProvisionalSuspension_{case} a adro:ProvisionalSuspensionStatus ;\n'
                     f'    rdfs:label "provisional suspension in {src}"@en ;\n'
                     f'    adro:hasEffectiveFrom {dt(date)} ;\n'
                     f'    adro:concernsCase adro:CaseRecord_{case} ;\n'
                     f'    obo:IAO_0000119 "{src}" ;\n'
                     f'    rdfs:comment "As stated in {src}: {esc(quote)}."@en .\n\n')
            o.append(f'adro:Person_{pid} adro:bearerOfRole adro:ProvisionalSuspension_{case} .\n\n')
        else:
            omitted.append((src, "provisional suspension",
                            "the award records no provisional suspension"))

        # the person bears the ineligibility the decision established
        o.append(f'adro:Person_{pid} adro:bearerOfRole adro:Ineligibility_{case} .\n\n')

        # the Prohibited List edition the decision applied
        if d["list_edition"]:
            eid, ename, equote = d["list_edition"]
            counts["edition"] += 1
            o.append(f'adro:{eid} a adro:ProhibitedListEdition ;\n'
                     f'    rdfs:label "{ename}"@en ;\n'
                     f'    adro:issuedBy adro:WADA ;\n'
                     f'    obo:IAO_0000119 "{src}" ;\n'
                     f'    rdfs:comment "As stated in {src}: {esc(equote)}."@en .\n\n')
            o.append(f'adro:Decision_{case} adro:appliedEdition adro:{eid} .\n\n')
            # the List edition itself, where its text is held: when it came into
            # effect, the entry the decision relied on, and the applicability that
            # entry states for the substance the decision named
            if d.get("list_text"):
                lt = d["list_text"]
                lsrc = lt["src"]
                o.append(f'adro:{eid} adro:hasEffectiveFrom {dt(lt["effective_from"])} ;\n'
                         f'    rdfs:comment "As stated on the cover of {lsrc}: {esc(lt["effective_quote"])}."@en .\n\n')
                for (entry, number, title, sub, sublabel, cat, ctx, ctxquote) in lt["entries"]:
                    counts["list_entry"] = counts.get("list_entry", 0) + 1
                    o.append(f'adro:{entry} a adro:ProhibitedListEntry ;\n'
                             f'    rdfs:label "{ename}, {number}"@en ;\n'
                             f'    dcterms:title "{title}"@en ;\n'
                             f'    obo:BFO_0000176 adro:{eid} ;\n'
                             f'    obo:IAO_0000119 "{lsrc}" .\n\n')
                    counts["applicability"] = counts.get("applicability", 0) + 1
                    o.append(f'adro:App_{eid.split("_")[-1]}_{sub} a adro:ProhibitionApplicability ;\n'
                             f'    rdfs:label "applicability of {sublabel} under the {ename}"@en ;\n'
                             f'    adro:appliesTo adro:Substance_{sub} ;\n'
                             f'    adro:hasCategory adro:{cat} ;\n'
                             f'    adro:statedIn adro:{entry} ;\n'
                             f'    adro:validFrom {dt(lt["effective_from"])} ;\n'
                             f'    adro:competitionContext adro:{ctx} ;\n'
                             f'    obo:IAO_0000119 "{lsrc}" ;\n'
                             f'    rdfs:comment "Context as stated in the running header of section S1 of {lsrc}: {esc(ctxquote)}"@en .\n\n')
        else:
            omitted.append((src, "Prohibited List edition",
                            "the decision refers to the Prohibited List without naming an edition"))

    # ------------------------------------------------------------------
    # the appeal stage, where an appeal decision records how it came about
    # ------------------------------------------------------------------
    o.append("########  Jurisdiction, and where each decision was obtained  ########\n\n")
    for case, ctx in CASE_CONTEXT.items():
        o.append(f'adro:CaseRecord_{case} adro:concernsJurisdiction adro:{ctx["jurisdiction"]} .\n')
        o.append(f'adro:Decision_{case} adro:hasSourceURL "{ctx["url"]}"^^xsd:anyURI ;\n'
                 f'    adro:hasRetrievalDate {dt(ctx["retrieved"])} .\n\n')

    o.append("########  Appeal proceedings  ########\n\n")
    for a in APPEALS:
        src = a["src"]
        counts["appeal"] = counts.get("appeal", 0) + 1
        o.append(f'adro:NoticeOfAppeal_{a["case"]} a adro:NoticeOfAppeal ;\n'
                 f'    rdfs:label "notice of appeal in {src}"@en ;\n'
                 f'    adro:hasIssueDateTime {dt(a["notice"][0])} ;\n'
                 f'    adro:concernsCase adro:CaseRecord_{a["case"]} ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(a["notice"][1])}."@en .\n\n')
        o.append(f'adro:Appeal_{a["case"]} a adro:AppealProcess ;\n'
                 f'    rdfs:label "appeal proceeding in {src}"@en ;\n'
                 f'    adro:initiatedBy adro:NoticeOfAppeal_{a["case"]} ;\n'
                 f'    obo:BFO_0000057 adro:Person_{a["person"]} ;\n'
                 f'    adro:hasSpecifiedOutput adro:Decision_{a["case"]} ;\n')
        for i, _ in enumerate(a["hearings"], start=1):
            o.append(f'    obo:BFO_0000117 adro:Hearing_{a["case"]}_{i} ;\n')
        o.append(f'    adro:concernsCase adro:CaseRecord_{a["case"]} ;\n'
                 f'    obo:IAO_0000119 "{src}" .\n\n')
        for i, (hd, hq) in enumerate(a["hearings"], start=1):
            counts["hearing"] += 1
            o.append(f'adro:Hearing_{a["case"]}_{i} a adro:Hearing ;\n'
                     f'    rdfs:label "hearing in {src}"@en ;\n'
                     f'    adro:hasStartDateTime {dt(hd)} ;\n'
                     f'    adro:concernsCase adro:CaseRecord_{a["case"]} ;\n'
                     f'    obo:IAO_0000119 "{src}" ;\n'
                     f'    rdfs:comment "As stated in {src}: {esc(hq)}."@en .\n\n')

    # the charge letter opens the determination, where a decision says so
    for case, doc, quote, src in OPENINGS:
        o.append(f'adro:Determination_{case} adro:initiatedBy adro:{doc} ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(quote)}."@en .\n\n')

    # ------------------------------------------------------------------
    # a decision may state that something does not exist. The statement is
    # recorded as a class axiom on the person, scoped to the substance named,
    # rather than as a silence in the file.
    # ------------------------------------------------------------------
    o.append("########  Absence of an exemption, as a decision states it  ########\n\n")
    for person, subst, src, quote in ABSENT_EXEMPTIONS:
        o.append(f'adro:Person_{person} a [ a owl:Class ;\n'
                 f'    owl:complementOf [ a owl:Restriction ;\n'
                 f'        owl:onProperty adro:bearerOfRole ;\n'
                 f'        owl:someValuesFrom [ a owl:Class ; owl:intersectionOf (\n'
                 f'            adro:ExemptionStatus\n'
                 f'            [ a owl:Restriction ; owl:onProperty adro:exemptionFor ;\n'
                 f'              owl:hasValue adro:{subst} ] ) ] ] ] .\n\n')
        o.append(f'adro:Person_{person} rdfs:comment '
                 f'"As stated in {src}: {esc(quote)}. The statement is recorded as the absence '
                 f'of an exemption for that substance, and not as the absence of any exemption."@en .\n\n')

    o.append("########  Laboratories named in the decisions  ########\n\n")
    for lid, (lname, lquote, src) in labs.items():
        o.append(f'adro:{lid} a adro:Laboratory ;\n'
                 f'    rdfs:label "{lname}"@en ;\n'
                 f'    obo:IAO_0000119 "{src}" ;\n'
                 f'    rdfs:comment "As stated in {src}: {esc(lquote)}."@en .\n\n')

    open(out, "w", encoding="utf-8").write("".join(o))

    r.append("# The course of a matter, from first instance decisions\n\n")
    r.append("Appeal digests state the outcome. First instance decisions state how the matter "
             "came about. The individuals in `doping-ontology-procedure.ttl` reproduce those "
             "statements and nothing else: each carries the decision it comes from and the "
             "wording it rests on.\n\n")
    r.append("## What the four decisions yielded\n\n| kind | individuals |\n|---|---|\n")
    for k, v in counts.items():
        r.append(f"| {k} | {v} |\n")
    r.append("\n## Fields not asserted, and why\n\n| decision | field | reason |\n|---|---|---|\n")
    for src, field, why in omitted:
        r.append(f"| {src} | {field} | {why} |\n")
    r.append("\n## Entailments this data produces\n\n"
             "The property chains in the core file fire on these individuals rather than on "
             "test data alone. A sample collection with a participant and a specified output "
             "entails that the sample was collected from that person. A finding about that "
             "sample entails that the finding concerns that person. Neither relation is "
             "asserted anywhere in this file.\n")
    open(report, "w", encoding="utf-8").write("".join(r))
    print(counts)

main(sys.argv[1], sys.argv[2])
