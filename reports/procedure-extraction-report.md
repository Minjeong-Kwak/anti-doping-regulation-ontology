# The course of a matter, from first instance decisions

Appeal digests state the outcome. First instance decisions state how the matter came about. The individuals in `doping-ontology-procedure.ttl` reproduce those statements and nothing else: each carries the decision it comes from and the wording it rests on.

## What the four decisions yielded

| kind | individuals |
|---|---|
| person | 4 |
| sample | 4 |
| collection | 4 |
| analysis | 4 |
| finding | 4 |
| notice | 4 |
| provisional | 2 |
| hearing | 7 |
| laboratory | 3 |
| measurement | 1 |
| edition | 1 |
| portion | 5 |
| appeal | 2 |

## Fields not asserted, and why

| decision | field | reason |
|---|---|---|
| National Anti-Doping Panel (United Kingdom) SR/056/2022 | laboratory | the decision refers to a WADA approved laboratory without naming it |
| National Anti-Doping Panel (United Kingdom) SR/056/2022 | measured concentration | the decision reports the finding without a stated concentration |
| National Anti-Doping Panel (United Kingdom) SR/056/2022 | Prohibited List edition | the decision refers to the Prohibited List without naming an edition |
| American Arbitration Association case 30 190 00847 06 | measured concentration | the decision reports the finding without a stated concentration |
| American Arbitration Association case 30 190 00847 06 | provisional suspension | the award records no provisional suspension |
| American Arbitration Association case 30 190 00847 06 | Prohibited List edition | the decision refers to the Prohibited List without naming an edition |
| American Arbitration Association case 30 190 00170 07 | measured concentration | the decision reports the finding without a stated concentration |
| American Arbitration Association case 30 190 00170 07 | notice of charge | the award records no date on which the person was notified |
| American Arbitration Association case 30 190 00170 07 | provisional suspension | the award records no provisional suspension |
| American Arbitration Association case 30 190 00170 07 | Prohibited List edition | the decision refers to the Prohibited List without naming an edition |

## Entailments this data produces

The property chains in the core file fire on these individuals rather than on test data alone. A sample collection with a participant and a specified output entails that the sample was collected from that person. A finding about that sample entails that the finding concerns that person. Neither relation is asserted anywhere in this file.
