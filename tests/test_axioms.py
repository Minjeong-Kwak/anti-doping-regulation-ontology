"""
Axiom test suite for the anti-doping regulation ontology.

Runs the TBox through HermiT and checks:
  P-tests  the property chains produce entailments that are not asserted
  N-tests  each defect pattern found in the previous ontology is rejected

Requires: rdflib, owlready2, java
Run from the directory containing doping-ontology-core.ttl, bfo-core.owl, iao.owl:
    python3 tests/test_axioms.py
"""
import os, sys
import rdflib
from rdflib import RDF, OWL, URIRef, Namespace
from owlready2 import World, sync_reasoner_hermit, OwlReadyInconsistentOntologyError

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ADRO = Namespace('https://w3id.org/adro/')
OBO  = Namespace('http://purl.obolibrary.org/obo/')
X    = lambda n: URIRef('https://w3id.org/adro/test#' + n)

def load_base():
    g = rdflib.Graph()
    for f, fmt in [('bfo-core.owl', 'xml'), ('iao.owl', 'xml'),
                   ('doping-ontology-core.ttl', 'turtle'),
                   ('doping-ontology-designations.ttl', 'turtle'),
                   ('doping-ontology-substances.ttl', 'turtle'),
                   ('doping-ontology-analytes.ttl', 'turtle'),
                   ('doping-ontology-cases-cas.ttl', 'turtle'),
                   ('doping-ontology-cases-national.ttl', 'turtle'),
                   ('doping-ontology-procedure.ttl', 'turtle')]:
        g.parse(os.path.join(ROOT, f), format=fmt)
    for s in list(g.subjects(RDF.type, OWL.Ontology)):
        for t in list(g.triples((s, None, None))):
            g.remove(t)
    return g

BASE = load_base()
RESULTS = []

def run(name, abox, expect):
    g = rdflib.Graph()
    for t in BASE:
        g.add(t)
    g.add((URIRef('https://w3id.org/adro/test'), RDF.type, OWL.Ontology))
    for t in abox:
        g.add(t)
    fn = os.path.join(HERE, '_tmp_%s.owl' % abs(hash(name)))
    g.serialize(fn, format='xml')
    w = World()
    o = w.get_ontology('file://' + fn).load()
    try:
        with o:
            sync_reasoner_hermit(w, infer_property_values=True, debug=0)
        res = 'CONSISTENT'
    except OwlReadyInconsistentOntologyError:
        res = 'INCONSISTENT'
    os.remove(fn)
    ok = res == expect
    RESULTS.append(ok)
    print(('PASS  ' if ok else 'FAIL  ') + name + ': %s (expected %s)' % (res, expect))
    return w

# ---------------------------------------------------------------- P tests
POS = [
    (X('P1'),   RDF.type, ADRO.Person),
    (X('SC1'),  RDF.type, ADRO.SampleCollection),
    (X('SC1'),  OBO.BFO_0000057, X('P1')),
    (X('SC1'),  ADRO.hasCollectedSample, X('S1')),
    (X('S1'),   RDF.type, ADRO.UrineSample),
    (X('AAF1'), RDF.type, ADRO.AdverseAnalyticalFinding),
    (X('AAF1'), OBO.IAO_0000136, X('S1')),
]
w = run('P1  property chains yield entailments', POS, 'CONSISTENT')
cf = list(w.sparql('SELECT ?s ?o WHERE { ?s <https://w3id.org/adro/collectedFrom> ?o }'))
cp = list(w.sparql('SELECT ?s ?o WHERE { ?s <https://w3id.org/adro/concernsPerson> ?o }'))
for label, rows in (('collectedFrom', cf), ('concernsPerson', cp)):
    got = bool(rows)
    RESULTS.append(got)
    print(('PASS  ' if got else 'FAIL  ') + '      entailed %s: %s'
          % (label, [(a.name, b.name) for a, b in rows]))

# ---------------------------------------------------------------- N tests
NEG = [
    ('N1  determination process typed as chemical substance',
     [(X('E1'), RDF.type, ADRO.ADRVDeterminationProcess),
      (X('E1'), RDF.type, ADRO.ChemicalSubstance)]),
    ('N2  person typed as ineligibility status',
     [(X('P2'), RDF.type, ADRO.Person),
      (X('P2'), RDF.type, ADRO.IneligibilityStatus)]),
    ('N3  decision typed as both first instance and appeal',
     [(X('D1'), RDF.type, ADRO.FirstInstanceDecision),
      (X('D1'), RDF.type, ADRO.AppealDecision)]),
    ('N4  designation typed as both ADRV type and substance category',
     [(X('C1'), RDF.type, ADRO.ADRVType),
      (X('C1'), RDF.type, ADRO.ProhibitedSubstanceCategory)]),
    ('N5  sample typed as decision',
     [(X('S2'), RDF.type, ADRO.Sample),
      (X('S2'), RDF.type, ADRO.Decision)]),
    ('N6  one role instance typed as ineligibility and provisional suspension',
     [(X('R1'), RDF.type, ADRO.IneligibilityStatus),
      (X('R1'), RDF.type, ADRO.ProvisionalSuspensionStatus)]),
    ('N8  instrument typed as both national legislation and governing body rule',
     [(X('I1'), RDF.type, ADRO.NationalLegislation),
      (X('I1'), RDF.type, ADRO.SportGoverningBodyRule)]),
    ('N9  a first instance decision asserted to hear an appeal',
     [(X('D9'), RDF.type, ADRO.FirstInstanceDecision),
      (X('D10'), RDF.type, ADRO.Decision),
      (X('D9'), ADRO.appealsAgainst, X('D10'))]),
    ('N10 an exemption asserted for a person a decision says held none',
     [(X('E10'), RDF.type, ADRO.ExemptionStatus),
      (X('E10'), ADRO.exemptionFor, ADRO.Substance_Metandienone),
      (ADRO.Person_Emir_Ahmatovic, ADRO.bearerOfRole, X('E10'))]),
    ('N11 a decision typed as both an exemption decision and an appeal',
     [(X('D11'), RDF.type, ADRO.TUEDecision),
      (X('D11'), RDF.type, ADRO.AppealDecision)]),
    ('N12 one role instance typed as exemption and ineligibility',
     [(X('R12'), RDF.type, ADRO.ExemptionStatus),
      (X('R12'), RDF.type, ADRO.IneligibilityStatus)]),
    ('N13 one report typed as both adverse and atypical',
     [(X('F13'), RDF.type, ADRO.AdverseAnalyticalFinding),
      (X('F13'), RDF.type, ADRO.AtypicalFinding)]),
    ('N14 a sample portion typed as a sample',
     [(X('P14'), RDF.type, ADRO.SamplePortion),
      (X('P14'), RDF.type, ADRO.UrineSample)]),
    ('N15 one designation typed as both a specimen matrix and a unit',
     [(X('G15'), RDF.type, ADRO.SpecimenMatrix),
      (X('G15'), RDF.type, ADRO.MeasurementUnit)]),
]
for name, abox in NEG:
    run(name, abox, 'INCONSISTENT')

# ---------------------------------------------------------------- D tests
w = run('D1  designations load and remain consistent', [], 'CONSISTENT')

rows = list(w.sparql('''SELECT ?c ?p WHERE
  { ?c <https://w3id.org/adro/broaderCategory> ?p }'''))
got = any(a.name == 'Category_S2_1_1' and b.name == 'Category_S2' for a, b in rows)
RESULTS.append(got)
print(('PASS  ' if got else 'FAIL  ')
      + 'D2  transitive broaderCategory entails Category_S2_1_1 -> Category_S2')

rows = list(w.sparql('''SELECT ?t WHERE
  { ?t a <https://w3id.org/adro/ADRVType> ;
       <https://w3id.org/adro/definedIn> ?a }'''))
got = len(rows) == 11
RESULTS.append(got)
print(('PASS  ' if got else 'FAIL  ')
      + 'D3  all 11 ADRV types cite a Code article (found %d)' % len(rows))

def ids(q):
    return set(str(r[0]) for r in w.sparql(q))

def check(label, subject_q, prop):
    subs = ids(subject_q)
    have = ids('SELECT ?s WHERE { ?s <%s> ?o }' % prop)
    miss = subs - have
    RESULTS.append(not miss)
    print(('PASS  ' if not miss else 'FAIL  ')
          + label + ' (%d without, of %d)' % (len(miss), len(subs)))

CATS = ('SELECT ?s WHERE { { ?s a <https://w3id.org/adro/ProhibitedSubstanceCategory> }'
        ' UNION { ?s a <https://w3id.org/adro/ProhibitedMethodCategory> } }')
check('D4  every category designation cites a List entry', CATS,
      'https://w3id.org/adro/definedIn')

SUBS = 'SELECT ?s WHERE { ?s a <https://w3id.org/adro/ChemicalSubstance> }'
appl = ids('SELECT ?o WHERE { ?a <https://w3id.org/adro/appliesTo> ?o }')
miss = ids(SUBS) - appl
RESULTS.append(not miss)
print(('PASS  ' if not miss else 'FAIL  ')
      + 'D5  every substance has a prohibition applicability (%d without)' % len(miss))

check('D6  every applicability cites a List entry',
      'SELECT ?s WHERE { ?s a <https://w3id.org/adro/ProhibitionApplicability> }',
      'https://w3id.org/adro/statedIn')

# A stated value is not comparable without the unit it is stated in and the
# specimen it was stated of. Both are designations, so both are checked as
# relations rather than as strings.
QUANT = ('SELECT ?s WHERE { { ?s a <https://w3id.org/adro/DecisionLimit> }'
         ' UNION { ?s a <https://w3id.org/adro/Measurement> } }')
check('D17 every threshold and measured value states its unit', QUANT,
      'https://w3id.org/adro/hasMeasurementUnit')
check('D18 every threshold and measured value states its specimen matrix', QUANT,
      'https://w3id.org/adro/hasSpecimenMatrix')

# Provenance checks over the case file itself. These do not depend on the
# reasoner: every decision individual must carry a citable identifier and name
# the body that issued it.
_cg = rdflib.Graph()
_cg.parse(os.path.join(ROOT, 'doping-ontology-cases-cas.ttl'), format='turtle')
_cg.parse(os.path.join(ROOT, 'doping-ontology-cases-national.ttl'), format='turtle')
_A = URIRef('https://w3id.org/adro/AppealDecision')
_F = URIRef('https://w3id.org/adro/FirstInstanceDecision')
_D = URIRef('https://w3id.org/adro/Decision')
_dec = {s for s, o in _cg.subject_objects(RDF.type) if o in (_A, _F, _D)}
for label, prop in [
        ('D7  every decision carries a case identifier',
         'https://w3id.org/adro/hasCaseIdentifier'),
        ('D8  every decision names an issuing body',
         'https://w3id.org/adro/issuedBy')]:
    have = {s for s, _ in _cg.subject_objects(URIRef(prop))}
    miss = _dec - have
    RESULTS.append(not miss)
    print(('PASS  ' if not miss else 'FAIL  ')
          + label + ' (%d without, of %d)' % (len(miss), len(_dec)))

# D9  every appeal decision that names the decision it reconsiders must name one
# that is present in the graph, not a dangling reference.
_app = URIRef('https://w3id.org/adro/appealsAgainst')
_targets = {o for _, o in _cg.subject_objects(_app)}
_missing = _targets - _dec
RESULTS.append(not _missing)
print(('PASS  ' if not _missing else 'FAIL  ')
      + 'D9  every appealed decision is present (%d dangling, of %d appeal links)'
      % (len(_missing), len(_targets)))

# D10  every instrument provision belongs to an instrument
_ng = rdflib.Graph()
_ng.parse(os.path.join(ROOT, 'doping-ontology-cases-national.ttl'), format='turtle')
_prov = {s for s, _ in _ng.subject_objects(RDF.type)
         if (s, RDF.type, URIRef('https://w3id.org/adro/InstrumentProvision')) in _ng}
_part = {s for s, _ in _ng.subject_objects(URIRef('http://purl.obolibrary.org/obo/BFO_0000176'))}
_miss = _prov - _part
RESULTS.append(not _miss)
print(('PASS  ' if not _miss else 'FAIL  ')
      + 'D10 every instrument provision belongs to an instrument (%d without, of %d)'
      % (len(_miss), len(_prov)))

# D11  every metabolite names at least one parent substance
_ag = rdflib.Graph()
_ag.parse(os.path.join(ROOT, 'doping-ontology-analytes.ttl'), format='turtle')
_met = set(_ag.subjects(RDF.type, URIRef('https://w3id.org/adro/Metabolite')))
_par = {s for s, _ in _ag.subject_objects(URIRef('https://w3id.org/adro/isMetaboliteOf'))}
_miss = _met - _par
RESULTS.append(not _miss)
print(('PASS  ' if not _miss else 'FAIL  ')
      + 'D11 every metabolite names a parent substance (%d without, of %d)'
      % (len(_miss), len(_met)))

# D16  the absence is scoped to the substance named. An exemption for a different
# substance is not excluded, because the decision said nothing about one.
run('D16 an exemption for a different substance stays consistent',
    [(X('E16'), RDF.type, ADRO.ExemptionStatus),
     (X('E16'), ADRO.exemptionFor, ADRO.Substance_Oxandrolone),
     (ADRO.Person_Emir_Ahmatovic, ADRO.bearerOfRole, X('E16'))], 'CONSISTENT')

# D12  the property chains fire on the procedural data, not only on test data.
# collectedFrom is asserted nowhere in the files. concernsPerson is asserted
# only for notices addressed to a named person, never for a finding.
_pg = rdflib.Graph()
_pg.parse(os.path.join(ROOT, 'doping-ontology-procedure.ttl'), format='turtle')
_asserted = {p for _, p, _ in _pg} | {p for _, p, _ in _cg}
_chain_asserted = {URIRef('https://w3id.org/adro/collectedFrom')} & _asserted
RESULTS.append(not _chain_asserted)
print(('PASS  ' if not _chain_asserted else 'FAIL  ')
      + 'D12 collectedFrom is nowhere asserted in the data files')

_w = run('D13 procedural data loads and remains consistent', [], 'CONSISTENT')
_cf = list(_w.sparql('''SELECT ?s ?o WHERE
  { ?s <https://w3id.org/adro/collectedFrom> ?o .
    ?s a <https://w3id.org/adro/UrineSample> }'''))
_cp = list(_w.sparql('''SELECT ?s ?o WHERE
  { ?s <https://w3id.org/adro/concernsPerson> ?o .
    ?s a <https://w3id.org/adro/AdverseAnalyticalFinding> }'''))
# One sample per matter, each split into portions. Four matters in the
# procedural layer, so four samples and four findings.
for _label, _rows, _n in (('collectedFrom on real samples', _cf, 4),
                          ('concernsPerson on real findings', _cp, 4)):
    _got = len(_rows) >= _n
    RESULTS.append(_got)
    print(('PASS  ' if _got else 'FAIL  ')
          + 'D14 %s: %d entailed (expected at least %d)' % (_label, len(_rows), _n))

# D15  every procedural individual cites the decision it comes from
_ind = {s for s, _, o in _pg.triples((None, RDF.type, None))
        if str(o).startswith('https://w3id.org/adro/')}
_cited = {s for s, _ in _pg.subject_objects(
    URIRef('http://purl.obolibrary.org/obo/IAO_0000119'))}
_miss = _ind - _cited
RESULTS.append(not _miss)
print(('PASS  ' if not _miss else 'FAIL  ')
      + 'D15 every procedural individual cites its source decision (%d without, of %d)'
      % (len(_miss), len(_ind)))

# negative: a category may not be asserted as a type of an event
run('N7  determination process typed as a substance category designation',
    [(X('E7'), RDF.type, ADRO.ADRVDeterminationProcess),
     (X('E7'), RDF.type, ADRO.ProhibitedSubstanceCategory)], 'INCONSISTENT')

print('\n%d/%d passed' % (sum(RESULTS), len(RESULTS)))
sys.exit(0 if all(RESULTS) else 1)
