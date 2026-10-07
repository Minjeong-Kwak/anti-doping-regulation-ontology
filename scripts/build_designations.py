# -*- coding: utf-8 -*-
"""
Generates doping-ontology-designations.ttl : the L1 document individuals and the
L2 regulatory designations they define.

Sources
  Prohibited List  : WADA, The 2026 Prohibited List (International Standard),
                     effective 1 January 2026.
  Code articles    : World Anti-Doping Code 2021, Article 2, as reproduced verbatim
                     in the UK Anti-Doping Rules 2021 v1.0.

Every designation carries adro:definedIn to the document part it is specified in.
No designation is asserted as a class.
"""
import io

NS = "https://w3id.org/adro/"
LIST_ED = "ProhibitedList_2026"
CODE_ED = "WADACode_2021"

# (id, label, parent_id, kind, specified)  kind: S = substance, M = method
CATS = [
 ("S0",     "Non-approved substances", None, "S", True),
 ("S1",     "Anabolic agents", None, "S", False),
 ("S1_1",   "Anabolic androgenic steroids (AAS)", "S1", "S", None),
 ("S1_2",   "Other anabolic agents", "S1", "S", None),
 ("S2",     "Peptide hormones, growth factors, related substances, and mimetics", None, "S", False),
 ("S2_1",   "Erythropoietins (EPO) and agents affecting erythropoiesis", "S2", "S", None),
 ("S2_1_1", "Erythropoietin receptor agonists", "S2_1", "S", None),
 ("S2_1_2", "Hypoxia-inducible factor (HIF) activating agents", "S2_1", "S", None),
 ("S2_1_3", "GATA inhibitors", "S2_1", "S", None),
 ("S2_1_4", "Transforming growth factor beta (TGF-beta) signalling inhibitors", "S2_1", "S", None),
 ("S2_1_5", "Innate repair receptor agonists", "S2_1", "S", None),
 ("S2_2",   "Peptide hormones and their releasing factors", "S2", "S", None),
 ("S2_2_1", "Testosterone-stimulating peptides in males", "S2_2", "S", None),
 ("S2_2_2", "Corticotrophins and their releasing factors", "S2_2", "S", None),
 ("S2_2_3", "Growth hormone, its analogues and fragments", "S2_2", "S", None),
 ("S2_2_4", "Growth hormone releasing factors", "S2_2", "S", None),
 ("S2_3",   "Growth factors and growth factor modulators", "S2", "S", None),
 ("S3",     "Beta-2 agonists", None, "S", True),
 ("S4",     "Hormone and metabolic modulators", None, "S", None),
 ("S4_1",   "Aromatase inhibitors", "S4", "S", True),
 ("S4_2",   "Anti-estrogenic substances", "S4", "S", True),
 ("S4_3",   "Agents preventing activin receptor IIB activation", "S4", "S", False),
 ("S4_4",   "Metabolic modulators", "S4", "S", False),
 ("S4_4_1", "AMPK activators, PPAR-delta agonists and Rev-erb-alpha agonists", "S4_4", "S", None),
 ("S4_4_2", "Insulins and insulin-mimetics", "S4_4", "S", None),
 ("S4_4_3", "Meldonium", "S4_4", "S", None),
 ("S4_4_4", "Trimetazidine", "S4_4", "S", None),
 ("S5",     "Diuretics and masking agents", None, "S", True),
 ("S6",     "Stimulants", None, "S", None),
 ("S6_A",   "Non-specified stimulants", "S6", "S", False),
 ("S6_B",   "Specified stimulants", "S6", "S", True),
 ("S7",     "Narcotics", None, "S", True),
 ("S8",     "Cannabinoids", None, "S", True),
 ("S9",     "Glucocorticoids", None, "S", True),
 ("P1",     "Beta-blockers", None, "S", True),
 ("M1",     "Manipulation of blood and blood components", None, "M", False),
 ("M1_1",   "Administration or reintroduction of blood or red blood cell products", "M1", "M", None),
 ("M1_2",   "Artificially enhancing the uptake, transport or delivery of oxygen", "M1", "M", None),
 ("M1_3",   "Intravascular manipulation of the blood or blood components", "M1", "M", None),
 ("M1_4",   "Use of re-breathing systems or equipment delivering carbon monoxide", "M1", "M", None),
 ("M2",     "Chemical and physical manipulation", None, "M", None),
 ("M2_1",   "Tampering or Attempting to Tamper with Samples", "M2", "M", False),
 ("M2_2",   "Intravenous infusions and injections above the stated volume", "M2", "M", True),
 ("M3",     "Gene and cell doping", None, "M", False),
 ("M3_1",   "Use of nucleic acids or nucleic acid analogues", "M3", "M", None),
 ("M3_2",   "Use of normal or genetically modified cells or cell components", "M3", "M", None),
]

# top-level category -> competition context designation
CONTEXT = {
 "S0":"AtAllTimes","S1":"AtAllTimes","S2":"AtAllTimes","S3":"AtAllTimes",
 "S4":"AtAllTimes","S5":"AtAllTimes","M1":"AtAllTimes","M2":"AtAllTimes",
 "M3":"AtAllTimes","S6":"InCompetition","S7":"InCompetition","S8":"InCompetition",
 "S9":"InCompetition","P1":"InCompetition",
}

# (id, article number, title, ontological character)
ADRVS = [
 ("Presence","2.1","Presence of a Prohibited Substance or its Metabolites or Markers in an Athlete's Sample","state"),
 ("Use","2.2","Use or Attempted Use by an Athlete of a Prohibited Substance or a Prohibited Method","process"),
 ("EvadingRefusingFailing","2.3","Evading, refusing or failing to submit to Sample collection","omission"),
 ("WhereaboutsFailures","2.4","Whereabouts failures","omission"),
 ("Tampering","2.5","Tampering or Attempted Tampering with any part of Doping Control","process"),
 ("Possession","2.6","Possession of a Prohibited Substance or a Prohibited Method","state"),
 ("Trafficking","2.7","Trafficking or Attempted Trafficking in any Prohibited Substance or Prohibited Method","process"),
 ("Administration","2.8","Administration or Attempted Administration to any Athlete of any Prohibited Substance or Prohibited Method","process"),
 ("Complicity","2.9","Complicity or Attempted Complicity","process"),
 ("ProhibitedAssociation","2.10","Prohibited Association by an Athlete or other Person","state"),
 ("Retaliation","2.11","Acts by an Athlete or other Person to discourage or retaliate against reporting to authorities","process"),
]

SANCTIONS = [
 ("Disqualification","disqualification","Code 2021 Articles 9, 10.1 and 10.10"),
 ("Ineligibility","period of ineligibility","Code 2021 Articles 10.2 and 10.3"),
 ("LifetimeIneligibility","lifetime ineligibility","Code 2021 Article 10.3; a period of ineligibility of lifetime, carrying no numeric duration"),
 ("ProvisionalSuspension","provisional suspension","Code 2021 Article 7.4 and UK Anti-Doping Rules 2021 Article 7.10"),
 ("FinancialConsequence","financial consequence","Code 2021 Article 10.12"),
]

CONTEXTS = [
 ("AtAllTimes","prohibited at all times","Prohibited in-competition and out-of-competition."),
 ("InCompetition","prohibited in-competition","Prohibited during the in-competition period as defined by the Code."),
 ("OutOfCompetition","prohibited out-of-competition","Prohibited outside the in-competition period."),
 ("InParticularSports","prohibited in particular sports","As stated in the running header of section P1 of the 2026 Prohibited List: PROHIBITED IN PARTICULAR SPORTS. The sports are named in the section and carried by sportScope."),
]

# Specimen matrices named by the List where it states a threshold. Only the matrix
# a source actually names is emitted; nothing is added for completeness.
MATRICES = [
 ("Urine","urine","The 2026 Prohibited List states each of its decision limits as a urinary concentration, and the decisions in the corpus report their measured concentrations in urine."),
]

# Units in which the List states its thresholds and the decisions state their
# measured values. The display name is one spelling; the spellings the sources
# use are carried as a comment, as is done for sports.
UNITS = [
 ("MicrogramPerMillilitre","microgram per millilitre","Written in the 2026 Prohibited List as micrograms per millilitre and abbreviated elsewhere as ug/mL."),
 ("NanogramPerMillilitre","nanogram per millilitre","Written in the 2026 Prohibited List as nanograms per millilitre and in the decisions as ng/mL."),
]

ROUTES_PROHIBITED_S9 = [("Injectable","injectable"),("Oral","oral"),("Oromucosal","oromucosal"),("Rectal","rectal")]
ROUTES_OTHER = [("Inhaled","inhaled"),("Dermal","dermal"),("Intranasal","intranasal"),
                ("Ophthalmological","ophthalmological"),("Otic","otic"),
                ("DentalIntracanal","dental-intracanal"),("Perianal","perianal"),
                ("Intravenous","intravenous")]

CASE_STATUS = [
 ("Pending","pending","No final decision has been issued."),
 ("Final","final","The decision is final and no appeal is outstanding."),
 ("UnderAppeal","under appeal","An appeal against the decision is outstanding."),
 ("Overturned","overturned","The decision was set aside on appeal."),
]

# P1 sports, with the governing federation as given in the List, and whether also
# prohibited out-of-competition (marked * in the List)
# Section P1 names the sports in running text and in lower case. The display name
# is given in the form the award headnotes also use, so that one sport carries one
# name whichever document it came from; the List's own wording is kept alongside.
P1_SPORTS = [
 ("Archery","Archery","archery","WA",True),
 ("Automobile","Automobile","automobile","FIA",False),
 ("Billiards","Billiards","billiards (all disciplines)","WCBS",False),
 ("Darts","Darts","darts","WDF",False),
 ("Golf","Golf","golf","IGF",False),
 ("MiniGolf","Mini-golf","mini-golf","WMF",False),
 ("Shooting","Shooting","shooting","ISSF, IPC",True),
 ("UnderwaterSports","Underwater sports","underwater sports","CMAS",True),
]

o = io.StringIO()
w = o.write

w("""@prefix adro: <https://w3id.org/adro/> .
@prefix obo:  <http://purl.obolibrary.org/obo/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/adro/designations> a owl:Ontology ;
    owl:imports <https://w3id.org/adro/> ;
    dcterms:title "Anti-Doping Regulation Ontology: normative documents and regulatory designations"@en ;
    rdfs:comment "Generated by scripts/build_designations.py from the 2026 Prohibited List and Article 2 of the 2021 World Anti-Doping Code."@en .

########################################
# L1 normative documents
########################################

""")

w(f"""adro:{CODE_ED} a adro:WorldAntiDopingCode ;
    rdfs:label "World Anti-Doping Code 2021"@en ;
    adro:hasEffectiveFrom "2021-01-01T00:00:00"^^xsd:dateTime .

adro:{LIST_ED} a adro:ProhibitedListEdition ;
    rdfs:label "The 2026 Prohibited List"@en ;
    adro:hasEffectiveFrom "2026-01-01T00:00:00"^^xsd:dateTime ;
    adro:hasEffectiveTo   "2026-12-31T00:00:00"^^xsd:dateTime ;
    adro:issuedBy adro:WADA .

adro:WADA a adro:AntiDopingOrganization ;
    rdfs:label "World Anti-Doping Agency"@en .

""")

# Code articles
for cid, num, title, char in ADRVS:
    w(f"""adro:Article_2021_{cid} a adro:CodeArticle ;
    rdfs:label "World Anti-Doping Code 2021, Article {num}"@en ;
    dcterms:title "{title}"@en ;
    obo:BFO_0000176 adro:{CODE_ED} .

""")

# Prohibited List entries
for cid, label, parent, kind, spec in CATS:
    disp = cid.replace("_", ".")
    line = f"""adro:Entry_2026_{cid} a adro:ProhibitedListEntry ;
    rdfs:label "The 2026 Prohibited List, {disp}"@en ;
    dcterms:title "{label}"@en ;
    obo:BFO_0000176 adro:{LIST_ED}"""
    if spec is not None:
        line += f" ;\n    adro:isSpecified \"{str(spec).lower()}\"^^xsd:boolean"
    w(line + " .\n\n")

w("""########################################
# L2 regulatory designations
########################################

# Anti-doping rule violation types. Each is defined in a Code article.
# The ontologicalCharacter annotation records that the provisions are not
# homogeneous: some proscribe a process, some a state, some an omission.

""")
for cid, num, title, char in ADRVS:
    w(f"""adro:ADRVType_{cid} a adro:ADRVType ;
    rdfs:label "ADRV type: {title}"@en ;
    adro:definedIn adro:Article_2021_{cid} ;
    adro:ontologicalCharacter "{char}" .

""")

w("# Prohibited substance and method categories.\n\n")
for cid, label, parent, kind, spec in CATS:
    cls = "adro:ProhibitedSubstanceCategory" if kind == "S" else "adro:ProhibitedMethodCategory"
    disp = cid.replace("_", ".")
    line = f"""adro:Category_{cid} a {cls} ;
    rdfs:label "{disp} {label}"@en ;
    adro:definedIn adro:Entry_2026_{cid}"""
    if parent:
        line += f" ;\n    adro:broaderCategory adro:Category_{parent}"
    w(line + " .\n\n")

w("# Sanction types.\n\n")
for sid, label, src in SANCTIONS:
    w(f"""adro:SanctionType_{sid} a adro:SanctionType ;
    rdfs:label "{label}"@en ;
    obo:IAO_0000119 "{src}" .

""")

w("# Competition contexts.\n\n")
for cid, label, note in CONTEXTS:
    w(f"""adro:Context_{cid} a adro:CompetitionContext ;
    rdfs:label "{label}"@en ;
    rdfs:comment "{note}"@en ;
    adro:definedIn adro:Entry_2026_S0 .

""")

w("# Routes of administration named in the 2026 Prohibited List.\n\n")
for rid, label in ROUTES_PROHIBITED_S9 + ROUTES_OTHER:
    w(f"""adro:Route_{rid} a adro:RouteOfAdministration ;
    rdfs:label "{label}"@en .

""")

w("# Specimen matrices named where the List states a threshold.\n\n")
for mid, label, note in MATRICES:
    w(f"""adro:Matrix_{mid} a adro:SpecimenMatrix ;
    rdfs:label "{label}"@en ;
    rdfs:comment "{note}"@en ;
    obo:IAO_0000119 "WADA, The 2026 Prohibited List (International Standard)" .

""")

w("# Units in which thresholds and measured values are stated.\n\n")
for uid, label, note in UNITS:
    w(f"""adro:Unit_{uid} a adro:MeasurementUnit ;
    rdfs:label "{label}"@en ;
    rdfs:comment "{note}"@en ;
    obo:IAO_0000119 "WADA, The 2026 Prohibited List (International Standard)" .

""")

w("# Case statuses.\n\n")
for sid, label, note in CASE_STATUS:
    w(f"""adro:CaseStatus_{sid} a adro:CaseStatus ;
    rdfs:label "{label}"@en ;
    rdfs:comment "{note}"@en .

""")

w("# Sports named in P1 of the 2026 Prohibited List.\n\n")
for spid, label, listed, fed, ooc in P1_SPORTS:
    w(f"""adro:Sport_{spid} a adro:Sport ;
    rdfs:label "{label}"@en ;
    rdfs:comment "As named in section P1 of the 2026 Prohibited List: {listed}. Governing body as given in the List: {fed}."@en .

""")

w("""########################################
# Category-level prohibition applicabilities for the 2026 edition
########################################

""")
n = 0
for cid in ["S0","S1","S2","S3","S4","S5","M1","M2","M3","S6","S7","S8","S9"]:
    ctx = CONTEXT[cid]
    n += 1
    w(f"""adro:App_2026_{cid} a adro:ProhibitionApplicability ;
    rdfs:label "applicability of {cid} under the 2026 Prohibited List"@en ;
    adro:hasCategory adro:Category_{cid} ;
    adro:statedIn adro:Entry_2026_{cid} ;
    adro:competitionContext adro:Context_{ctx} ;
    adro:validFrom "2026-01-01T00:00:00"^^xsd:dateTime ;
    adro:validTo   "2026-12-31T00:00:00"^^xsd:dateTime .

""")

# P1 is sport-scoped
for spid, label, listed, fed, ooc in P1_SPORTS:
    n += 1
    w(f"""adro:App_2026_P1_{spid} a adro:ProhibitionApplicability ;
    rdfs:label "applicability of P1 in {label} under the 2026 Prohibited List"@en ;
    adro:hasCategory adro:Category_P1 ;
    adro:statedIn adro:Entry_2026_P1 ;
    adro:competitionContext adro:Context_InCompetition ;
    adro:sportScope adro:Sport_{spid} ;
    adro:validFrom "2026-01-01T00:00:00"^^xsd:dateTime ;
    adro:validTo   "2026-12-31T00:00:00"^^xsd:dateTime .

""")
    if ooc:
        n += 1
        w(f"""adro:App_2026_P1_{spid}_OOC a adro:ProhibitionApplicability ;
    rdfs:label "applicability of P1 out-of-competition in {label} under the 2026 Prohibited List"@en ;
    adro:hasCategory adro:Category_P1 ;
    adro:statedIn adro:Entry_2026_P1 ;
    adro:competitionContext adro:Context_OutOfCompetition ;
    adro:sportScope adro:Sport_{spid} ;
    adro:validFrom "2026-01-01T00:00:00"^^xsd:dateTime ;
    adro:validTo   "2026-12-31T00:00:00"^^xsd:dateTime .

""")

# S9 route restriction
w("""adro:App_2026_S9_Routes a adro:ProhibitionApplicability ;
    rdfs:label "applicability of S9 by prohibited route under the 2026 Prohibited List"@en ;
    adro:hasCategory adro:Category_S9 ;
    adro:statedIn adro:Entry_2026_S9 ;
    adro:competitionContext adro:Context_InCompetition ;
    adro:routeOfAdministration adro:Route_Injectable , adro:Route_Oral ,
                               adro:Route_Oromucosal , adro:Route_Rectal ;
    adro:validFrom "2026-01-01T00:00:00"^^xsd:dateTime ;
    adro:validTo   "2026-12-31T00:00:00"^^xsd:dateTime ;
    rdfs:comment "Glucocorticoids are prohibited when administered by these routes. Other routes are not prohibited within licensed doses and therapeutic indications."@en .
""")

open("doping-ontology-designations.ttl", "w", encoding="utf-8").write(o.getvalue())
print("written. applicabilities:", n + 1)
