#! /usr/bin/python

# am facut fisierul asta ptc cel ipynb pare sa fie proprietary si are compatibilitate putin ciudata

from astroquery.gaia import Gaia
import time 
SIZEOF_REQUEST = 1000                           # trebuie marit dar momentan il las asa sa ruleze mai rapid
INITIAL_TIME = time.time()

query = """
SELECT TOP """ + str(SIZEOF_REQUEST) + """ SOURCE_ID, RA, DEC, PARALLAX, phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE PARALLAX IS NOT NULL
AND phot_g_mean_mag < 20.5
"""

job = Gaia.launch_job(query)

results = job.get_results()

# print("Time passed: " + str(time.time() - INITIAL_TIME))

number_of_rows = len(results)
# print(f"Number of rows: {number_of_rows}")


print(f"{'RA'},{'Dec'},{'Parallax'},{'Phot_g_mean_mag'}")

# Print a separator
# print('-' * 65)

# Print each row in the results
for row in results:
    print(f"{row['SOURCE_ID']},{row['RA']:.6f},{row['DEC']:.6f},{row['PARALLAX']:.6f},{row['phot_g_mean_mag']:.6f}")
    # print(f"{row['RA']:.6f},{row['DEC']:.6f}")

# print("Time after print: " + str(time.time() - INITIAL_TIME))
