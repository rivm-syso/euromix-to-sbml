# euromix

## Overview

| key                          | value                                                                                  |
|:-----------------------------|:---------------------------------------------------------------------------------------|
| Modelled species/orgamism(s) | http://purl.obolibrary.org/obo/NCBITaxon_40674                                         |
| Model chemical(s)            | http://purl.obolibrary.org/obo/CHEBI_59999, http://purl.obolibrary.org/obo/CHEBI_25212 |
| Input route(s)               | 3 (inhalation, dermal, oral)                                                           |
| Time resolution              | h                                                                                      |
| Amounts unit                 | mmol                                                                                   |
| Volume unit                  | L                                                                                      |
| Number of compartments       | 13                                                                                     |
| Number of species            | 14                                                                                     |
| Number of parameters         | 41 (31 external / 10 internal)                                                         |

## Diagram

![Diagram](euromix.report.svg)

## Compartments

| id        | name                            | unit   | model qualifier                            |
|:----------|:--------------------------------|:-------|:-------------------------------------------|
| Air       | alveolar air                    | L      | http://purl.obolibrary.org/obo/PBPKO_00448 |
| Urine     | urine                           | L      | http://purl.obolibrary.org/obo/PBPKO_00556 |
| Fat       | adipose tissue                  | L      | http://purl.obolibrary.org/obo/PBPKO_00460 |
| Rich      | richly perfused tissue          | L      | http://purl.obolibrary.org/obo/PBPKO_00453 |
| Liver     | liver                           | L      | http://purl.obolibrary.org/obo/PBPKO_00558 |
| Art       | arterial blood                  | L      | http://purl.obolibrary.org/obo/PBPKO_00552 |
| Ven       | venous blood                    | L      | http://purl.obolibrary.org/obo/PBPKO_00561 |
| Skin_e    | viable epidermis exposed skin   | L      | http://purl.obolibrary.org/obo/PBPKO_00456 |
| Skin_u    | viable epidermis unexposed skin | L      | http://purl.obolibrary.org/obo/PBPKO_00455 |
| Skin_sc_e | stratum corneum exposed skin    | L      | http://purl.obolibrary.org/obo/PBPKO_00458 |
| Skin_sc_u | stratum corneum unexposed skin  | L      | http://purl.obolibrary.org/obo/PBPKO_00457 |
| Poor      | poorly perfused tissue          | L      | http://purl.obolibrary.org/obo/PBPKO_00454 |
| Gut       | gut                             | L      | http://purl.obolibrary.org/obo/PBPKO_00477 |

## Species

| id         | name                                                         | unit   | model qualifier                            |
|:-----------|:-------------------------------------------------------------|:-------|:-------------------------------------------|
| QFat       | amount of chemical in fat tissues                            | mmol   | http://purl.obolibrary.org/obo/PBPKO_00550 |
| QRich      | amount of chemical in richly tissues                         | mmol   | http://purl.obolibrary.org/obo/PBPKO_00629 |
| QPoor      | amount of chemical in poor tissues                           | mmol   | http://purl.obolibrary.org/obo/PBPKO_00630 |
| QLiver     | amount of chemical in liver                                  | mmol   | http://purl.obolibrary.org/obo/PBPKO_00497 |
| QMetab     | amount of chemical metabolized (cumulated)                   | mmol   | http://purl.obolibrary.org/obo/PBPKO_00058 |
| QGut       | amount of chemical in gut lumen                              | mmol   | http://purl.obolibrary.org/obo/PBPKO_00496 |
| QSkin_u    | amount of chemical in viable epidermis of unexposed skin     | mmol   | *not specified*                            |
| QSkin_e    | amount of chemical in viable epidermis of exposed skin       | mmol   | *not specified*                            |
| QSkin_sc_u | amount of chemical in skin stratum corneum of unexposed skin | mmol   | *not specified*                            |
| QSkin_sc_e | amount of chemical in skin stratum corneum of exposed skin   | mmol   | *not specified*                            |
| QArt       | amount of chemical in arterial blood                         | mmol   | http://purl.obolibrary.org/obo/PBPKO_00631 |
| QVen       | amount of chemical in venous blood                           | mmol   | http://purl.obolibrary.org/obo/PBPKO_00632 |
| QExcret    | amount of chemical excreted in urine (cumulated)             | mmol   | http://purl.obolibrary.org/obo/PBPKO_00274 |
| QAir       | amount of chemical in alveolar air                           | mmol   | http://purl.obolibrary.org/obo/PBPKO_00633 |

## Transfer equations

| id   | from       | to         | equation                                                                                                                                                                                                                                                                                                             |
|:-----|:-----------|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| _J0  | QArt       | QAir       | $ \frac{\mathit{Falv}\cdot \frac{\mathit{QArt}}{\mathit{Art}}}{\mathit{PCAir}}$                                                                                                                                                                                                                                      |
| _J1  | QAir       | QArt       | $ \mathit{FBlood}\cdot \frac{\mathit{QAir}}{\mathit{Air}}$                                                                                                                                                                                                                                                           |
| _J2  | QArt       | QFat       | $ \mathit{FFat}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                                             |
| _J3  | QFat       | QVen       | $ \frac{\mathit{FFat}\cdot \frac{\mathit{QFat}}{\mathit{Fat}}}{\mathit{PCFat}}$                                                                                                                                                                                                                                      |
| _J4  | QArt       | QRich      | $ \mathit{FRich}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                                            |
| _J5  | QRich      | QVen       | $ \frac{\mathit{FRich}\cdot \frac{\mathit{QRich}}{\mathit{Rich}}}{\mathit{PCRich}}$                                                                                                                                                                                                                                  |
| _J6  | QArt       | QPoor      | $ \mathit{FPoor}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                                            |
| _J7  | QPoor      | QVen       | $ \frac{\mathit{FPoor}\cdot \frac{\mathit{QPoor}}{\mathit{Poor}}}{\mathit{PCPoor}}$                                                                                                                                                                                                                                  |
| _J8  | QArt       | QLiver     | $ \mathit{FLiver}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                                           |
| _J9  | QLiver     | QVen       | $ \frac{\mathit{FLiver}\cdot \frac{\mathit{QLiver}}{\mathit{Liver}}}{\mathit{PCLiver}}$                                                                                                                                                                                                                              |
| _J10 | QGut       | QLiver     | $ \mathit{kGut}\cdot \mathit{QGut}$                                                                                                                                                                                                                                                                                  |
| _J11 | QArt       | QSkin_u    | $ \mathit{FSkin_{u}}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                                        |
| _J12 | QSkin_u    | QVen       | $ \frac{\mathit{FSkin_{u}}\cdot \mathit{conc}\left(\mathit{QSkin_{u}},\mathit{Skin_{u}}\right)}{\mathit{PCSkin}}$                                                                                                                                                                                                    |
| _J13 | QSkin_u    | QSkin_sc_u | $ \frac{\mathit{f_{su}}\cdot \mathit{conc}\left(\mathit{QSkin_{u}},\mathit{Skin_{u}}\right)}{\mathit{PCSkin_{sc}}}$                                                                                                                                                                                                  |
| _J14 | QSkin_sc_u | QSkin_u    | $ \mathit{f_{su}}\cdot \mathit{conc}\left(\mathit{QSkin\_sc\_u},\mathit{Skin\_sc\_u}\right)$                                                                                                                                                                                                                         |
| _J15 | QArt       | QSkin_e    | $ \mathit{FSkin_{e}}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                                        |
| _J16 | QSkin_e    | QVen       | $ \frac{\mathit{FSkin_{e}}\cdot \mathit{conc}\left(\mathit{QSkin_{e}},\mathit{Skin_{e}}\right)}{\mathit{PCSkin}}$                                                                                                                                                                                                    |
| _J17 | QSkin_e    | QSkin_sc_e | $ \frac{\mathit{f_{se}}\cdot \mathit{conc}\left(\mathit{QSkin_{e}},\mathit{Skin_{e}}\right)}{\mathit{PCSkin_{sc}}}$                                                                                                                                                                                                  |
| _J18 | QSkin_sc_e | QSkin_e    | $ \mathit{f_{se}}\cdot \mathit{conc}\left(\mathit{QSkin\_sc\_e},\mathit{Skin\_sc\_e}\right)$                                                                                                                                                                                                                         |
| _J19 | QVen       | QArt       | $ \mathit{FBlood}\cdot \frac{\mathit{QVen}}{\mathit{Ven}}$                                                                                                                                                                                                                                                           |
| _J20 | QLiver     | QMetab     | $ \mathit{fub}\cdot \begin{cases} \mathit{metab_{MM}}\left(\mathit{Vmax},\mathit{Km},\mathit{PCLiver},\mathit{QLiver},\mathit{Liver}\right)& \text{  if  } & \mathit{Michaelis}>0.5\\ \mathit{metab_{MA}}\left(\mathit{CLH},\mathit{PCLiver},\mathit{QLiver},\mathit{Liver}\right)& {\text{  otherwise}}\end{cases}$ |
| _J21 | QArt       | QExcret    | $ \mathit{Ke}\cdot \mathit{fub}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$                                                                                                                                                                                                                                             |

## ODEs

$\frac{d[\mathtt{QFat}]}{dt} =  \mathit{FFat}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             -  \frac{\mathit{FFat}\cdot \frac{\mathit{QFat}}{\mathit{Fat}}}{\mathit{PCFat}}$

$\frac{d[\mathtt{QRich}]}{dt} =  \mathit{FRich}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
              -  \frac{\mathit{FRich}\cdot \frac{\mathit{QRich}}{\mathit{Rich}}}{\mathit{PCRich}}$

$\frac{d[\mathtt{QPoor}]}{dt} =  \mathit{FPoor}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
              -  \frac{\mathit{FPoor}\cdot \frac{\mathit{QPoor}}{\mathit{Poor}}}{\mathit{PCPoor}}$

$\frac{d[\mathtt{QLiver}]}{dt} =  \mathit{FLiver}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
               -  \frac{\mathit{FLiver}\cdot \frac{\mathit{QLiver}}{\mathit{Liver}}}{\mathit{PCLiver}}
               +  \mathit{kGut}\cdot \mathit{QGut}
               -  \mathit{fub}\cdot \begin{cases} \mathit{metab_{MM}}\left(\mathit{Vmax},\mathit{Km},\mathit{PCLiver},\mathit{QLiver},\mathit{Liver}\right)& \text{  if  } & \mathit{Michaelis}>0.5\\ \mathit{metab_{MA}}\left(\mathit{CLH},\mathit{PCLiver},\mathit{QLiver},\mathit{Liver}\right)& {\text{  otherwise}}\end{cases}$

$\frac{d[\mathtt{QMetab}]}{dt} =  \mathit{fub}\cdot \begin{cases} \mathit{metab_{MM}}\left(\mathit{Vmax},\mathit{Km},\mathit{PCLiver},\mathit{QLiver},\mathit{Liver}\right)& \text{  if  } & \mathit{Michaelis}>0.5\\ \mathit{metab_{MA}}\left(\mathit{CLH},\mathit{PCLiver},\mathit{QLiver},\mathit{Liver}\right)& {\text{  otherwise}}\end{cases}$

$\frac{d[\mathtt{QGut}]}{dt} = -  \mathit{kGut}\cdot \mathit{QGut}$

$\frac{d[\mathtt{QSkin-u}]}{dt} =  \mathit{FSkin_{u}}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
                -  \frac{\mathit{FSkin_{u}}\cdot \mathit{conc}\left(\mathit{QSkin_{u}},\mathit{Skin_{u}}\right)}{\mathit{PCSkin}}
                -  \frac{\mathit{f_{su}}\cdot \mathit{conc}\left(\mathit{QSkin_{u}},\mathit{Skin_{u}}\right)}{\mathit{PCSkin_{sc}}}
                +  \mathit{f_{su}}\cdot \mathit{conc}\left(\mathit{QSkin\_sc\_u},\mathit{Skin\_sc\_u}\right)$

$\frac{d[\mathtt{QSkin-e}]}{dt} =  \mathit{FSkin_{e}}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
                -  \frac{\mathit{FSkin_{e}}\cdot \mathit{conc}\left(\mathit{QSkin_{e}},\mathit{Skin_{e}}\right)}{\mathit{PCSkin}}
                -  \frac{\mathit{f_{se}}\cdot \mathit{conc}\left(\mathit{QSkin_{e}},\mathit{Skin_{e}}\right)}{\mathit{PCSkin_{sc}}}
                +  \mathit{f_{se}}\cdot \mathit{conc}\left(\mathit{QSkin\_sc\_e},\mathit{Skin\_sc\_e}\right)$

$\frac{d[\mathtt{QSkin-sc-u}]}{dt} =  \frac{\mathit{f_{su}}\cdot \mathit{conc}\left(\mathit{QSkin_{u}},\mathit{Skin_{u}}\right)}{\mathit{PCSkin_{sc}}}
                   -  \mathit{f_{su}}\cdot \mathit{conc}\left(\mathit{QSkin\_sc\_u},\mathit{Skin\_sc\_u}\right)$

$\frac{d[\mathtt{QSkin-sc-e}]}{dt} =  \frac{\mathit{f_{se}}\cdot \mathit{conc}\left(\mathit{QSkin_{e}},\mathit{Skin_{e}}\right)}{\mathit{PCSkin_{sc}}}
                   -  \mathit{f_{se}}\cdot \mathit{conc}\left(\mathit{QSkin\_sc\_e},\mathit{Skin\_sc\_e}\right)$

$\frac{d[\mathtt{QArt}]}{dt} = -  \frac{\mathit{Falv}\cdot \frac{\mathit{QArt}}{\mathit{Art}}}{\mathit{PCAir}}
             +  \mathit{FBlood}\cdot \frac{\mathit{QAir}}{\mathit{Air}}
             -  \mathit{FFat}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             -  \mathit{FRich}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             -  \mathit{FPoor}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             -  \mathit{FLiver}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             -  \mathit{FSkin_{u}}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             -  \mathit{FSkin_{e}}\cdot \frac{\mathit{QArt}}{\mathit{Art}}
             +  \mathit{FBlood}\cdot \frac{\mathit{QVen}}{\mathit{Ven}}
             -  \mathit{Ke}\cdot \mathit{fub}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$

$\frac{d[\mathtt{QVen}]}{dt} =  \frac{\mathit{FFat}\cdot \frac{\mathit{QFat}}{\mathit{Fat}}}{\mathit{PCFat}}
             +  \frac{\mathit{FRich}\cdot \frac{\mathit{QRich}}{\mathit{Rich}}}{\mathit{PCRich}}
             +  \frac{\mathit{FPoor}\cdot \frac{\mathit{QPoor}}{\mathit{Poor}}}{\mathit{PCPoor}}
             +  \frac{\mathit{FLiver}\cdot \frac{\mathit{QLiver}}{\mathit{Liver}}}{\mathit{PCLiver}}
             +  \frac{\mathit{FSkin_{u}}\cdot \mathit{conc}\left(\mathit{QSkin_{u}},\mathit{Skin_{u}}\right)}{\mathit{PCSkin}}
             +  \frac{\mathit{FSkin_{e}}\cdot \mathit{conc}\left(\mathit{QSkin_{e}},\mathit{Skin_{e}}\right)}{\mathit{PCSkin}}
             -  \mathit{FBlood}\cdot \frac{\mathit{QVen}}{\mathit{Ven}}$

$\frac{d[\mathtt{QExcret}]}{dt} =  \mathit{Ke}\cdot \mathit{fub}\cdot \frac{\mathit{QArt}}{\mathit{Art}}$

$\frac{d[\mathtt{QAir}]}{dt} =  \frac{\mathit{Falv}\cdot \frac{\mathit{QArt}}{\mathit{Art}}}{\mathit{PCAir}}
             -  \mathit{FBlood}\cdot \frac{\mathit{QAir}}{\mathit{Air}}$

## Assignment rules

$Fat =  \mathit{BM}\cdot \mathit{scVFat}$

$Rich =  \mathit{BM}\cdot \mathit{scVRich}$

$Liver =  \mathit{BM}\cdot \mathit{scVLiver}$

$Art =  \mathit{BM}\cdot \mathit{scVBlood}\cdot \mathit{scVArt}$

$Ven =  \mathit{BM}\cdot \mathit{scVBlood}-\mathit{Art}$

$Skin_e =  \mathit{BSA}\cdot \mathit{Height_{vs}}\cdot \mathit{fSA_{exposed}}$

$Skin_u =  \mathit{BSA}\cdot \mathit{Height_{vs}}\cdot (1-\mathit{fSA_{exposed}})$

$Skin_sc_e =  \mathit{BSA}\cdot \mathit{Height_{sc}}\cdot \mathit{fSA_{exposed}}$

$Skin_sc_u =  \mathit{BSA}\cdot \mathit{Height_{sc}}\cdot (1-\mathit{fSA_{exposed}})$

$Poor =  \mathit{BM}\cdot (1-\mathit{scVFat}-\mathit{scVRich}-\mathit{scVLiver}-\mathit{scVBlood}-0.1)-\mathit{Skin_{e}}-\mathit{Skin_{u}}-\mathit{Skin\_sc\_e}-\mathit{Skin\_sc\_u}$

$f_su =  \mathit{Kp\_sc\_vs}\cdot \mathit{BSA}\cdot (1-\mathit{fSA_{exposed}})$

$f_se =  \mathit{Kp\_sc\_vs}\cdot \mathit{BSA}\cdot \mathit{fSA_{exposed}}$

$FBlood =  \mathit{scFBlood}\cdot \mathit{BM}$

$FFat =  \mathit{FBlood}\cdot \mathit{scFFat}$

$FPoor =  \mathit{FBlood}\cdot \mathit{scFPoor}$

$FLiver =  \mathit{FBlood}\cdot \mathit{scFLiver}$

$FSkin =  \mathit{FBlood}\cdot \mathit{scFSkin}$

$FRich =  \mathit{FBlood}-\mathit{FFat}-\mathit{FPoor}-\mathit{FLiver}-\mathit{FSkin}$

$FSkin_e =  \mathit{FSkin}\cdot \mathit{fSA_{exposed}}$

$FSkin_u =  \mathit{FSkin}-\mathit{FSkin_{e}}$

## Function definitions

$conc( \mathit{q},  \mathit{vol}) =  \lambda(\mathit{q}, \mathit{vol}) =\begin{cases} \frac{\mathit{q}}{\mathit{vol}}& \text{  if  } & \mathit{vol}>0\\ 0& {\text{  otherwise}}\end{cases}$

$metab_MM( \mathit{Vmax},  \mathit{Km},  \mathit{PC},  \mathit{q},  \mathit{vol}) =  \lambda(\mathit{Vmax}, \mathit{Km}, \mathit{PC}, \mathit{q}, \mathit{vol}) =\left(\frac{\mathit{vol}\cdot \mathit{Vmax}\cdot \mathit{conc}\left(\mathit{q},\mathit{vol}\right)}{\mathit{PC}\cdot \mathit{Km}+\mathit{conc}\left(\mathit{q},\mathit{vol}\right)}\right)$

$metab_MA( \mathit{CLH},  \mathit{PC},  \mathit{q},  \mathit{vol}) =  \lambda(\mathit{CLH}, \mathit{PC}, \mathit{q}, \mathit{vol}) =\left(\frac{\mathit{CLH}\cdot \mathit{conc}\left(\mathit{q},\mathit{vol}\right)}{\mathit{PC}}\right)$

## Parameters

| id          | name                                                            | unit          | model qualifier                            |
|:------------|:----------------------------------------------------------------|:--------------|:-------------------------------------------|
| BM          | body weight                                                     | kg            | http://purl.obolibrary.org/obo/PBPKO_00008 |
| BSA         | body surface area                                               | dm^2          | http://purl.obolibrary.org/obo/PBPKO_00010 |
| scVFat      | fat volume as fraction of total body weight                     | L/kg          | http://purl.obolibrary.org/obo/PBPKO_00086 |
| scVRich     | richly perfused tissues volume as fraction of total body weight | L/kg          | http://purl.obolibrary.org/obo/PBPKO_00102 |
| scVLiver    | liver volume as fraction of total body weight                   | L/kg          | http://purl.obolibrary.org/obo/PBPKO_00078 |
| scVBlood    | blood volume as fraction of total body weight                   | L/kg          | http://purl.obolibrary.org/obo/PBPKO_00107 |
| scVArt      | arterial blood volume as fraction of total blood volume         | dimensionless | *not specified*                            |
| scFBlood    | total blood flow per unit mass                                  | L/kg/h        | *not specified*                            |
| scFFat      | fraction of blood flow going to adipose tissue                  | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00033 |
| scFPoor     | fraction total blood flow going to poorly perfused tissue       | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00047 |
| scFLiver    | fraction total blood flow going to liver                        | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00025 |
| scFSkin     | fraction total blood flow going to skin                         | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00037 |
| fSA_exposed | fraction of skin surface area actually exposed                  | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00110 |
| Height_sc   | thickness stratum corneum                                       | dm            | *not specified*                            |
| Height_vs   | thickness viable epidermis                                      | dm            | *not specified*                            |
| Falv        | alveolar ventilation rate                                       | L/h           | http://purl.obolibrary.org/obo/PBPKO_00114 |
| PCFat       | partition coefficient fat over blood                            | dimensionless | *not specified*                            |
| PCLiver     | partition coefficient liver over blood                          | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00577 |
| PCRich      | partition coefficient poorly perfused tissue over blood         | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00587 |
| PCPoor      | partition coefficient richly perfused tissue over blood         | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00584 |
| PCSkin_sc   | partition coefficient viable skin over stratum corneum          | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00182 |
| PCSkin      | partition coefficient viable skin over blood                    | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00588 |
| PCAir       | partition coefficient blood over air                            | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00568 |
| kGut        | absorption rate constant gut                                    | /h            | http://purl.obolibrary.org/obo/PBPKO_00141 |
| Kp_sc_vs    | diffusion rate from stratum corneum to viable epidermis         | dm/h          | *not specified*                            |
| Km          | Michaelis-Menten constant liver                                 | mmol          | http://purl.obolibrary.org/obo/PBPKO_00214 |
| Michaelis   | flag for Michaelis-Menten or linear metabolism                  | dimensionless | *not specified*                            |
| Vmax        | maximum rate of metabolism in the liver                         | mmol/L/h      | http://purl.obolibrary.org/obo/PBPKO_00213 |
| CLH         | hepatic clearance rate                                          | L/h           | http://purl.obolibrary.org/obo/PBPKO_00234 |
| Ke          | renal excretion rate                                            | L/h           | http://purl.obolibrary.org/obo/PBPKO_00237 |
| fub         | fraction unbound in blood                                       | dimensionless | http://purl.obolibrary.org/obo/PBPKO_00622 |
| f_su        | dermal absorption flow through unexposed skin                   | L/h           | *not specified*                            |
| f_se        | dermal absorption flow through exposed skin                     | L/h           | *not specified*                            |
| FBlood      | blood flow                                                      | L/h           | http://purl.obolibrary.org/obo/PBPKO_00030 |
| FFat        | blood flow to the fat                                           | L/h           | http://purl.obolibrary.org/obo/PBPKO_00032 |
| FPoor       | blood flow to poorly perfused tissues                           | L/h           | http://purl.obolibrary.org/obo/PBPKO_00046 |
| FLiver      | blood flow to the liver                                         | L/h           | http://purl.obolibrary.org/obo/PBPKO_00024 |
| FSkin       | blood flow to the skin                                          | L/h           | http://purl.obolibrary.org/obo/PBPKO_00036 |
| FRich       | blood flow to richly perfused tissues                           | L/h           | http://purl.obolibrary.org/obo/PBPKO_00048 |
| FSkin_e     | blood flow to exposed skin                                      | L/h           | *not specified*                            |
| FSkin_u     | blood flow to unexposed skin                                    | L/h           | *not specified*                            |

## Creators

|    | first-name   | last-name     | affiliation                                                           | email   |
|---:|:-------------|:--------------|:----------------------------------------------------------------------|:--------|
|  0 | Margriet     | Palm          | Dutch National Institute for Public Health and the Environment (RIVM) |         |
|  1 | Jordi        | Minnema       | Dutch National Institute for Public Health and the Environment (RIVM) |         |
|  2 | Johannes     | Kruisselbrink | Wageningen University & Research, Biometris                           |         |

