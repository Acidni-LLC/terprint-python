import csv

# The output string provided by the user
output = """
https://muvfl.com/locations/boynton-beach: 283
https://muvfl.com/locations/apollo-beach: 279
https://muvfl.com/locations/bonita-springs: 282
https://muvfl.com/locations/bradenton: 357
https://muvfl.com/locations/bradenton-75th-west: 284
https://muvfl.com/locations/brandon: 285
https://muvfl.com/locations/cape-coral: 286
https://muvfl.com/locations/clearwater: 287
https://muvfl.com/locations/clearwater-roosevelt: 288
https://muvfl.com/locations/crystal-river: 570
https://muvfl.com/locations/deltona: None
https://muvfl.com/locations/deerfield: 289
https://muvfl.com/locations/fort-myers-beach: 292
https://muvfl.com/locations/ft-myers: 290
https://muvfl.com/locations/fort-myers-cypress: 291
https://muvfl.com/locations/fort-pierce: 293
https://muvfl.com/locations/gainesville: 294
https://muvfl.com/locations/haines-city: 295
https://muvfl.com/locations/hobe-sound: 296
https://muvfl.com/locations/hollywood: 297
https://muvfl.com/locations/jax-beach: 298
https://muvfl.com/locations/jacksonville: 299
https://muvfl.com/locations/jacksonville-skymarks: 300
https://muvfl.com/locations/key-west: 302
https://muvfl.com/locations/lady-lake: 303
https://muvfl.com/locations/lake-city: 304
https://muvfl.com/locations/lakeland: 305
https://muvfl.com/locations/longwood: 306
https://muvfl.com/locations/lutz: 307
https://muvfl.com/locations/marco-island: 308
https://muvfl.com/locations/melbourne: 380
https://muvfl.com/locations/merritt-island: 309
https://muvfl.com/locations/miami-kendall: 301
https://muvfl.com/locations/naranja: 310
https://muvfl.com/locations/navarre: 311
https://muvfl.com/locations/new-smyrna-beach: 544
https://muvfl.com/locations/new-tampa: 312
https://muvfl.com/locations/north-miami: 314
https://muvfl.com/locations/north-miami-beach: 313
https://muvfl.com/locations/north-port: 315
https://muvfl.com/locations/ocala: 316
https://muvfl.com/locations/okeechobee: 379
https://muvfl.com/locations/orange-city: 317
https://muvfl.com/locations/orange-park: 318
https://muvfl.com/locations/orlando-colonial: 319
https://muvfl.com/locations/orlando: 320
https://muvfl.com/locations/orlando-vineland: 321
https://muvfl.com/locations/ormond-beach: 322
https://muvfl.com/locations/palatka: 323
https://muvfl.com/locations/panama-city-beach: 324
https://muvfl.com/locations/pensacola: 325
https://muvfl.com/locations/port-charlotte: 327
https://muvfl.com/locations/pinellas-park: 326
https://muvfl.com/locations/port-orange: 328
https://muvfl.com/locations/port-richey: 329
https://muvfl.com/locations/port-st-lucie: 330
https://muvfl.com/locations/sarasota: 331
https://muvfl.com/locations/sarasota-main: 332
https://muvfl.com/locations/satellite-beach: 333
https://muvfl.com/locations/sebastian: 334
https://muvfl.com/locations/sebring: 335
https://muvfl.com/locations/shalimar: 336
https://muvfl.com/locations/spring-hill: 337
https://muvfl.com/locations/st-augustine: 338
https://muvfl.com/locations/st-petersburg: 339
https://muvfl.com/locations/stuart: 340
https://muvfl.com/locations/tallahassee: 341
https://muvfl.com/locations/tamarac: 342
https://muvfl.com/locations/tampa: 343
https://muvfl.com/locations/tampa-himes: 344
https://muvfl.com/locations/tampa-west-kennedy: 345
https://muvfl.com/locations/titusville: 346
https://muvfl.com/locations/venice: 347
https://muvfl.com/locations/wellington: 348
https://muvfl.com/locations/west-melbourne: 349
https://muvfl.com/locations/west-palm-okeechobee: 351
https://muvfl.com/locations/west-palm-beach: 350
https://muvfl.com/locations/winter-haven: 352
https://muvfl.com/locations/auburndale: 281
https://muvfl.com/locations/winter-springs: 353
https://muvfl.com/locations/yulee: 354
https://muvfl.com/locations/zephyrhills: 355
"""

# Parse the output
lines = [line.strip() for line in output.strip().split('\n') if line.strip()]

data = []
for line in lines:
    if ': ' in line:
        url, storeid_str = line.split(': ', 1)
        location = url.split('/')[-1]
        storeid = storeid_str if storeid_str != 'None' else None
        data.append({'location': location, 'storeid': storeid})

# Write to CSV
with open('storeid_location_list.csv', 'w', newline='') as csvfile:
    fieldnames = ['location', 'storeid']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("CSV file 'storeid_location_list.csv' created successfully.")