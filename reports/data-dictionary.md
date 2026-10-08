# Data dictionary

Every term the ontology declares, with its definition, where it sits under the upper ontology, and how much use it gets. Generated from the files by `scripts/build_documentation.py`, so it cannot drift from them.

## Classes

| class | label | placed under | individuals | definition |
|---|---|---|---|---|
| `adro:ADRVDeterminationProcess` | ADRV determination process | adro:ResultsManagementProcess | 4 | A results management process in which it is determined whether a given matter constitutes an anti-doping rule violation. |
| `adro:ADRVType` | anti-doping rule violation type | obo:IAO_0000033 | 11 | A directive information entity that designates a type of anti-doping rule violation as specified by a Code article. |
| `adro:AdverseAnalyticalFinding` | adverse analytical finding | obo:IAO_0000088 | 4 | A report in which a laboratory states that a prohibited substance, its metabolite, or a marker has been identified in a sample. |
| `adro:AntiDopingInstrument` | anti-doping instrument | obo:IAO_0000310 | 0 | A document that states anti-doping rules binding on the persons within its stated scope. |
| `adro:AntiDopingOrganization` | anti-doping organization | adro:Organization | 1 | An organization with authority to adopt or enforce anti-doping rules. |
| `adro:AppealDecision` | appeal decision | adro:Decision | 198 | A decision issued by a body that reconsiders a decision of a lower body. |
| `adro:AppealProcess` | appeal process | adro:ResultsManagementProcess | 2 | A results management process in which a superior body reconsiders a decision of a lower body. |
| `adro:AthleteRole` | athlete role | obo:BFO_0000023 | 4 | A role borne by a person during the interval in which that person is subject to anti-doping regulation in connection with sporting competition. |
| `adro:AthleteSupportPersonnelRole` | athlete support personnel role | obo:BFO_0000023 | 3 | A role borne by a person during the interval in which that person works with, treats or assists an athlete participating in or preparing for sporting competition, and is for that reason subject to anti-doping regulation. |
| `adro:AtypicalFinding` | atypical finding | obo:IAO_0000088 | 0 | A report from an accredited laboratory that requires further investigation before an adverse analytical finding can be determined. |
| `adro:CaseRecord` | case record | obo:IAO_0000310 | 220 | A document that identifies a single matter and gathers the procedures and decisions pertaining to it. |
| `adro:CaseStatus` | case status | obo:IAO_0000030 | 4 | An information content entity that designates the procedural standing of a matter, such as final, under appeal, or overturned. |
| `adro:ChemicalSubstance` | chemical substance | obo:BFO_0000040 | 479 | A material entity that is individuated by its chemical composition. |
| `adro:CodeArticle` | Code article | adro:InstrumentProvision | 11 | A document part that constitutes a single article of a World Anti-Doping Code edition and directs conduct. |
| `adro:CompetitionContext` | competition context | obo:IAO_0000030 | 4 | An information content entity that designates a distinction of competition context on which prohibition depends. |
| `adro:Decision` | decision | obo:IAO_0000310 | 12 | A document in which a deciding body records its determination of a matter. |
| `adro:DecisionLimit` | decision limit | obo:IAO_0000030 | 6 | An information content entity that states the threshold at or above which an analytical result for a given analyte is to be reported. |
| `adro:ExemptionStatus` | exemption status | obo:BFO_0000023 | 0 | A role borne by a person during the interval in which that person is permitted to use a stated prohibited substance or method for a therapeutic purpose. |
| `adro:FirstInstanceDecision` | first instance decision | adro:Decision | 10 | A decision issued by a body of first instance. |
| `adro:Hearing` | hearing | adro:ResultsManagementProcess | 7 | A results management process in which a deciding body receives submissions from the parties and reaches a determination. |
| `adro:IneligibilityStatus` | ineligibility status | obo:BFO_0000023 | 8 | A role borne by a person during the interval in which that person is barred from participation by a sanction decision. |
| `adro:InstrumentProvision` | instrument provision | obo:IAO_0000033, obo:IAO_0000314 | 13 | A document part that constitutes a single numbered provision of an anti-doping instrument and directs conduct. |
| `adro:InternationalStandard` | international standard | obo:IAO_0000310 | 1 | A document that supplements the Code by specifying requirements in a defined area. |
| `adro:Jurisdiction` | jurisdiction | obo:IAO_0000030 | 3 | An information content entity that designates the persons and the territory within which an anti-doping instrument binds. |
| `adro:Laboratory` | laboratory | adro:Organization | 3 | An organization accredited to analyse samples collected in doping control. |
| `adro:LaboratoryAnalysis` | laboratory analysis | obo:BFO_0000015 | 4 | A process in which an accredited laboratory analyses a sample and produces a finding. |
| `adro:Marker` | marker | obo:BFO_0000040 | 0 | A material entity whose presence or quantity indicates the use of a prohibited substance or a prohibited method. |
| `adro:Measurement` | measurement | obo:IAO_0000109 | 1 | A measurement datum that records a value, its unit, and the analyte measured, as produced by an analysis. |
| `adro:MeasurementUnit` | measurement unit | obo:IAO_0000030 | 2 | An information content entity that designates the unit in which a measured value or a stated threshold is expressed. |
| `adro:Metabolite` | metabolite | adro:ChemicalSubstance | 8 | A chemical substance that is produced by the metabolism of another chemical substance. |
| `adro:NationalAntiDopingOrganization` | national anti-doping organization | adro:AntiDopingOrganization | 3 | An anti-doping organization with authority to operate an anti-doping programme within a given jurisdiction. |
| `adro:NationalAntiDopingRule` | national anti-doping rule | adro:AntiDopingInstrument | 1 | A document adopted by a national anti-doping organization that applies within its jurisdiction. |
| `adro:NationalLegislation` | national legislation | adro:AntiDopingInstrument | 1 | An anti-doping instrument enacted by a state and binding within its territory. |
| `adro:NoticeOfAppeal` | notice of appeal | obo:IAO_0000310 | 2 | A document by which a party states that it appeals a decision, and on which an appeal process is opened. |
| `adro:NotificationOfCharge` | notification of charge | obo:IAO_0000310 | 4 | A document by which an alleged anti-doping rule violation is notified to the person concerned. |
| `adro:Organization` | organization | obo:BFO_0000027 | 4 | An object aggregate of persons that acts with an assigned authority or function within the anti-doping system. |
| `adro:Person` | person | obo:BFO_0000030 | 7 | A material entity that is a human being falling within the scope of anti-doping regulation or participating in its administration. |
| `adro:ProhibitedListEdition` | Prohibited List edition | adro:InternationalStandard | 2 | An international standard that is a given edition of the Prohibited List, effective over a stated interval. |
| `adro:ProhibitedListEntry` | Prohibited List entry | obo:IAO_0000314 | 47 | A document part of a Prohibited List edition that specifies a substance, a method, or a category thereof. |
| `adro:ProhibitedMethodCategory` | prohibited method category | obo:IAO_0000030 | 11 | An information content entity that designates a category of prohibited methods as specified by a Prohibited List entry. |
| `adro:ProhibitedSubstanceCategory` | prohibited substance category | obo:IAO_0000030 | 35 | An information content entity that designates a category of prohibited substances as specified by a Prohibited List entry. |
| `adro:ProhibitionApplicability` | prohibition applicability | obo:IAO_0000001 | 505 | A conditional specification that states that a substance or method is prohibited under stated conditions of time, competition context, sport, route of administration, threshold, and jurisdiction. |
| `adro:ProvisionalSuspensionStatus` | provisional suspension status | obo:BFO_0000023 | 2 | A role borne by a person during the interval in which that person is barred from participation before a final decision is reached. |
| `adro:ResultsManagementProcess` | results management process | obo:BFO_0000015 | 0 | A process in which an anti-doping organization handles information bearing on whether an anti-doping rule has been violated. |
| `adro:RouteOfAdministration` | route of administration | obo:IAO_0000030 | 12 | An information content entity that designates a route of administration on which prohibition may depend. |
| `adro:Sample` | sample | obo:BFO_0000030 | 0 | A material entity that is biological material collected from a person in a doping control procedure for the purpose of analysis. |
| `adro:SampleCollection` | sample collection | obo:BFO_0000015 | 4 | A process in which a sample is collected from a person under a doping control procedure. |
| `adro:SamplePortion` | sample portion | obo:BFO_0000030 | 5 | A continuant that is a part of a sample, separated at collection and given its own reference, so that it can be analysed independently of the remainder. |
| `adro:SanctionDecision` | sanction decision | adro:Decision | 8 | A decision that determines the kind and extent of the consequence imposed in respect of an anti-doping rule violation. |
| `adro:SanctionModifyingGround` | sanction modifying ground | obo:IAO_0000030 | 4 | A designation of a circumstance which, if established, lengthens or shortens the period of ineligibility that would otherwise follow from an established violation. |
| `adro:SanctionType` | sanction type | obo:IAO_0000030 | 5 | An information content entity that designates a kind of consequence specified by the Code. |
| `adro:SpecimenMatrix` | specimen matrix | obo:IAO_0000030 | 1 | An information content entity that designates the kind of specimen in which a measurement is made or in which a stated threshold applies. |
| `adro:Sport` | sport | obo:IAO_0000030 | 81 | An information content entity that designates a sport for the purposes of applying and recording anti-doping regulation. |
| `adro:SportGoverningBodyRule` | sport governing body rule | adro:AntiDopingInstrument | 3 | An anti-doping instrument adopted by a body that governs a sport, binding on the persons under that body. |
| `adro:TUEDecision` | therapeutic use exemption decision | adro:Decision | 0 | A decision in which a body determines an application to use a prohibited substance or method for a therapeutic purpose. |
| `adro:UrineSample` | urine sample | adro:Sample | 4 | A sample that consists of urine. |
| `adro:WorldAntiDopingCode` | World Anti-Doping Code | adro:AntiDopingInstrument | 1 | A document that is a given edition of the Code issued by the World Anti-Doping Agency. |

## Object properties

| property | label | domain | range | assertions | definition |
|---|---|---|---|---|---|
| `adro:acceptsGround` | accepts ground | adro:Decision | adro:SanctionModifyingGround | 0 | Relates a decision to a ground it establishes, so that the period of ineligibility is altered accordingly. |
| `adro:adoptsInstrument` | adopts instrument | adro:AntiDopingInstrument | adro:AntiDopingInstrument | 2 | Relates an anti-doping instrument to another instrument that it takes over in place of stating its own rules. |
| `adro:appealsAgainst` | appeals against | adro:AppealDecision | adro:Decision | 4 | Relates an appeal decision to the decision that it reconsiders. |
| `adro:appliedEdition` | applied edition | adro:Decision | obo:IAO_0000310 | 1 | Relates a decision to the edition of a normative document that the deciding body applied. |
| `adro:appliedProvision` | applied provision | adro:Decision | adro:InstrumentProvision | 11 | Relates a decision to the provision that the deciding body applied in reaching its determination. |
| `adro:appliesTo` | applies to | adro:ProhibitionApplicability | adro:ChemicalSubstance | 480 | Relates a prohibition applicability to the chemical substance whose prohibition it states. |
| `adro:assignsType` | assigns type | adro:Decision | adro:ADRVType | 31 | Relates a decision to the violation type that the deciding body assigned to the matter. |
| `adro:bearerOfRole` | bearer of role | adro:Person | obo:BFO_0000023 | 13 | Relates a person to a role that inheres in that person. |
| `adro:bindsWithin` | binds within | adro:AntiDopingInstrument | adro:Jurisdiction | 5 | Relates an anti-doping instrument to the jurisdiction its own scope provision states. |
| `adro:broaderCategory` | broader category | obo:IAO_0000030 | obo:IAO_0000030 | 56 | Relates a regulatory designation to a designation under which it falls. |
| `adro:caseStatus` | case status | adro:CaseRecord | adro:CaseStatus | 220 | Relates a case record to the designation of the stage the matter has reached. |
| `adro:collectedFrom` | collected from | adro:Sample | adro:Person | 0 | Relates a sample to the person from whom it was collected. |
| `adro:competitionContext` | competition context | — | adro:CompetitionContext | 508 | Relates a prohibition applicability or a sample collection to the designation of the competition context in which it holds or occurs. |
| `adro:concernsCase` | concerns case | — | adro:CaseRecord | 49 | Relates an entity to the case record that gathers the matter it belongs to. |
| `adro:concernsJurisdiction` | concerns jurisdiction | — | adro:Jurisdiction | 4 | Relates a case record or a prohibition applicability to the jurisdiction within which it holds. |
| `adro:concernsPerson` | concerns person | obo:IAO_0000030 | adro:Person | 4 | Relates an information content entity to the person it is about. |
| `adro:concernsSport` | concerns sport | adro:CaseRecord | adro:Sport | 214 | Relates a case record to the designation of the sport in which the matter arose. |
| `adro:definedIn` | defined in | obo:IAO_0000030 | obo:IAO_0000314 | 65 | Relates a regulatory designation to the document part that specifies it. |
| `adro:establishes` | establishes | adro:Decision | obo:BFO_0000023 | 8 | Relates a decision to the role it brings into being in the person it concerns. |
| `adro:exemptionFor` | exemption for | adro:ExemptionStatus | adro:ChemicalSubstance | 0 | Relates an exemption status to the substance whose use it permits. |
| `adro:hasCategory` | has category | adro:ProhibitionApplicability | — | 505 | Relates a prohibition applicability to the designation of the category under which the substance or method falls. |
| `adro:hasCollectedSample` | has collected sample | adro:SampleCollection | adro:Sample | 4 | Relates a sample collection to the sample it produced. |
| `adro:hasDecisionLimit` | has decision limit | adro:ProhibitionApplicability | adro:DecisionLimit | 6 | Relates a prohibition applicability to the decision limit above which a finding is reported. |
| `adro:hasMeasurementUnit` | has measurement unit | — | adro:MeasurementUnit | 7 | Relates a measurement or a decision limit to the designation of the unit in which its value is expressed. |
| `adro:hasPortion` | has portion | adro:Sample | adro:SamplePortion | 5 | Relates a sample to a portion of it that carries its own reference. |
| `adro:hasSanctionType` | has sanction type | adro:SanctionDecision | adro:SanctionType | 13 | Relates a sanction decision to the designation of the kind of consequence it imposes. |
| `adro:hasSpecifiedInput` | has specified input | obo:BFO_0000015 | — | 8 | Relates a process to an entity it takes in and acts upon. |
| `adro:hasSpecifiedOutput` | has specified output | obo:BFO_0000015 | — | 10 | Relates a process to an entity it produces. |
| `adro:hasSpecimenMatrix` | has specimen matrix | — | adro:SpecimenMatrix | 7 | Relates a measurement or a decision limit to the designation of the kind of specimen in which it is stated. |
| `adro:implementsCodeArticle` | implements Code article | adro:InstrumentProvision | adro:CodeArticle | 3 | Relates a provision of an instrument other than the Code to the Code article it restates. |
| `adro:indicatesUseOf` | indicates use of | adro:Marker | adro:ChemicalSubstance | 0 | Relates a marker to the substance whose use it indicates. |
| `adro:initiatedBy` | initiated by | obo:BFO_0000015 | obo:IAO_0000310 | 4 | Relates a process to the document by which it was set in motion. |
| `adro:isCollectedSampleOf` | is collected sample of | — | — | 4 | Relates a sample to the collection that produced it. |
| `adro:isEvidenceFor` | is evidence for | adro:AdverseAnalyticalFinding | adro:ADRVDeterminationProcess | 4 | Relates an analytical finding to the determination process it bears upon. |
| `adro:isMetaboliteOf` | is metabolite of | adro:Metabolite | adro:ChemicalSubstance | 9 | Relates a metabolite to a substance from which a biotransformation process produces it. |
| `adro:isSpecifiedOutputOf` | is specified output of | — | — | 0 | Relates an entity to the process that produced it. |
| `adro:issuedBy` | issued by | — | adro:Organization | 222 | Relates a document to the organization that issued it. |
| `adro:measuresAnalyte` | measures analyte | adro:Measurement | adro:ChemicalSubstance | 1 | Relates a measurement to the substance whose quantity it reports. |
| `adro:mentions` | mentions | obo:IAO_0000030 | adro:ChemicalSubstance | 184 | Relates an information content entity to a substance it names. |
| `adro:raisesGround` | raises ground | adro:Decision | adro:SanctionModifyingGround | 4 | Relates a decision to a ground it records as raised in the matter, whether or not the deciding body accepted it. |
| `adro:resultsManagementAuthority` | results management authority | adro:CaseRecord | adro:AntiDopingOrganization | 220 | Relates a case record to the organization that managed the results of the matter. |
| `adro:routeOfAdministration` | route of administration | adro:ProhibitionApplicability | adro:RouteOfAdministration | 68 | Relates a prohibition applicability to the designation of the route of administration to which it is confined. |
| `adro:sportScope` | sport scope | adro:ProhibitionApplicability | adro:Sport | 11 | Relates a prohibition applicability to the designation of a sport to which it is confined. |
| `adro:statedIn` | stated in | adro:ProhibitionApplicability | adro:ProhibitedListEntry | 505 | Relates a prohibition applicability to the Prohibited List entry that states it. |

## Data properties

| property | label | domain | range | assertions | definition |
|---|---|---|---|---|---|
| `adro:hasAnalysisDateTime` | has analysis date time | adro:LaboratoryAnalysis | xsd:dateTime | 0 | The time at which a laboratory analysis was carried out or reported, as the source states it. |
| `adro:hasAnalyticalMethod` | has analytical method | adro:LaboratoryAnalysis | xsd:string | 2 | The analytical method applied, in the words the source uses for it. |
| `adro:hasCaseIdentifier` | has case identifier | adro:Decision | xsd:string | 469 | The reference by which the issuing institution identifies a matter or a decision. |
| `adro:hasCollectionDateTime` | has collection date time | adro:SampleCollection | xsd:dateTime | 4 | The time at which a sample was collected, as the source states it. |
| `adro:hasDecisionDate` | has decision date | adro:Decision | xsd:dateTime | 214 | The date on which a decision was issued, as the decision states it. |
| `adro:hasEffectiveFrom` | has effective from | — | xsd:dateTime | 10 | The time from which a document, an edition or a status takes effect. |
| `adro:hasEffectiveTo` | has effective to | — | xsd:dateTime | 6 | The time at which a document, an edition or a status ceases to have effect. |
| `adro:hasEndDateTime` | has end date time | obo:BFO_0000015 | xsd:dateTime | 2 | The time at which a process ended, where the source states an interval. |
| `adro:hasExternalIdentifier` | has external identifier | obo:BFO_0000040 | xsd:string | 0 | An identifier by which an entity is known in a resource outside this ontology, written as a prefixed identifier such as CHEBI:15365. |
| `adro:hasIneligibilityDurationInMonths` | has ineligibility duration in months | adro:IneligibilityStatus | xsd:decimal | 8 | The length of a period of ineligibility, in months, as a number. |
| `adro:hasIssueDateTime` | has issue date time | obo:IAO_0000310 | xsd:dateTime | 6 | The time at which a document was issued by the body that issued it. |
| `adro:hasMeasuredValue` | has measured value | adro:Measurement | xsd:decimal | 1 | The numeric value a measurement reports. |
| `adro:hasRetrievalDate` | has retrieval date | obo:IAO_0000310 | xsd:dateTime | 4 | The date on which the document was obtained from the address recorded for it. |
| `adro:hasSampleIdentifier` | has sample identifier | — | xsd:string | 5 | The reference the collecting authority assigns to a sample or to a portion of one. |
| `adro:hasSourceURL` | has source URL | obo:IAO_0000310 | xsd:anyURI | 4 | The address at which the issuing body published the document. |
| `adro:hasStartDateTime` | has start date time | obo:BFO_0000015 | xsd:dateTime | 7 | The time at which a process began. |
| `adro:hasThresholdValue` | has threshold value | adro:DecisionLimit | xsd:decimal | 6 | The numeric value at or above which a decision limit is exceeded. |
| `adro:isSpecified` | is specified | adro:ProhibitedListEntry | xsd:boolean | 19 | Whether a Prohibited List entry is designated as specified, which governs the range of sanction available. |
| `adro:validFrom` | valid from | adro:ProhibitionApplicability | xsd:dateTime | 505 | The time from which a prohibition applicability holds. |
| `adro:validTo` | valid to | adro:ProhibitionApplicability | xsd:dateTime | 504 | The time at which a prohibition applicability ceases to hold. |

A property with no domain or range has none asserted, because its subjects or values belong to more than one category. A property with no assertions is inferred rather than stated; the competency question report says which.
