from COA_ModernCanna01 import ModernCanna_COA

# Your Modern Canna text (format 4 - 47993_0006162867)
mc_text = """Certificate of Analysis
Trulieve
816 Commerce Blvd. Midway, FL 32343
Sample Alias:
ALC-VapeCartCDT-.5g-BlueSpringCks-I-FL
Sample Date:
12/18/24
Completed:
12/20/24 15:12
Lab ID:
IL18006-04
Sample Matrix:
Vape
Received:
12/18/24 14:26
47993_0006162867
ANALYSIS SUMMARY
TERPENES
POTENCY DETAILS
 
80.7% 
 delta 9-THC
0.241% 
 CBD
0.639% 
 CBN
0.323% 
 THCa
<LOQ% 
 CBDa
<LOQ% 
 delta 8-THC
<LOQ% 
 CBGa
1.14% 
 THCV
<LOQ% 
 CBDV
0.659% 
 CBC
2.03% 
 CBG
Total Terpenes: 2.21%
Total CBG
2.03% (10.2 mg)
Total CBN
0.639% (3.20 mg)
Completed
Potency
PASS
Foreign Matter
PASS
Heavy Metals
Not Tested
Homogeneity
PASS
Microbials
PASS
Water Activity
PASS
Mycotoxins
PASS
Pesticides
Not Tested
% Moisture
PASS
Residual Solvents
Completed
Terpenes
Analyte
%
 
 beta-Caryophyllene
0.632
 d-Limonene
0.464
 beta-Myrcene
0.320
 Linalool
0.230
 alpha-Humulene
0.182
 alpha-Bisabolol
0.114
 Fenchyl Alcohol
0.0739
 alpha-Terpineol
0.0619
 alpha-Pinene
0.0383
 beta-Pinene
0.0376
 Terpinolene
0.0266
 (+/-)-Borneol
0.0217
 Camphene
0.0113
Total THC
81.0% (405 mg)
Total CBD
0.241% (1.21 mg)
Total Active Cannabinoids
85.7% (429 mg)
LOQ = Limit of Quantification
ND = Non-Detect 
RPD = Relative Percent Difference
  MDL = Method Detection Limit
PQL = Practical Quantitation Limit
Copyright © 2024 Modern Canna, LLC. All rights reserved. 
This report shall not be reproduced, distributed, or transmitted in any form or by any means, without written consent from Modern Canna, LLC.  The 
results in this report relate only to the products analyzed. The results in this report are confidential. For more information regarding our reporting 
limits, please visit: www.moderncanna.com/modern-canna-reporting-limits/
4705 Old Rd 37
Lakeland, FL 33813
www.moderncanna.com
CMTL-0005
Page 1 of 1
863-608-7800
Accreditation #102020
Wyatt Bergel
   Laboratory Director
Jini Glaros, M.S.
Chief Scientific Officer
"""

# Parse the COA
coa = ModernCanna_COA.from_text(mc_text)

# Output as JSON
print(coa.to_json())

# Save to file
coa.save_json('modern_canna_47993_0006162867.json')

# Access specific data
print(f"Batch: {coa.batch_number}")
print(f"Lab ID: {coa.lab_id}")
print(f"THC: {coa.total_thc_percent}% ({coa.total_thc_mg} mg)")
print(f"Total Active Cannabinoids: {coa.total_active_cannabinoids_percent}%")

# Access cannabinoids
for cannabinoid in coa.cannabinoids:
    mg_text = f" ({cannabinoid.mg} mg)" if cannabinoid.mg else ""
    print(f"{cannabinoid.name}: {cannabinoid.percent}%{mg_text}")

# Access terpenes
for terpene in coa.terpenes:
    print(f"{terpene.name}: {terpene.percent}%")