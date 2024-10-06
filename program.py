#! /usr/bin/python

# am facut fisierul asta ptc cel ipynb pare sa fie proprietary si are compatibilitate putin ciudata

from astroquery.gaia import Gaia
import time 
SIZEOF_REQUEST = 10000    
# INITIAL_TIME = time.time()

query = """
SELECT TOP """ + str(SIZEOF_REQUEST) + """ SOURCE_ID, RA, DEC, PARALLAX, phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE PARALLAX IS NOT NULL  
AND phot_g_mean_mag < 10
ORDER BY phot_g_mean_mag ASC
"""
# AND PARALLAX < 0.005
# AND PARALLAX > -0.005 
# AND grvs_mag < 6

job = Gaia.launch_job(query)

results = job.get_results()

# print("Time passed: " + str(time.time() - INITIAL_TIME))

number_of_rows = len(results)
# print(f"Number of rows: {number_of_rows}")


# print(f"{'Source_ID'},{'RA'},{'Dec'},{'Parallax'},{'Phot_g_mean_mag'}")
print(f"{'RA'},{'Dec'},{'magnitude'}")


# Print a separator
# print('-' * 65)

# Print each row in the results
for row in results:
    # print(f"{row['SOURCE_ID']},{row['RA']:.6f},{row['DEC']:.6f},{row['PARALLAX']:.6f},{row['phot_g_mean_mag']:.6f}")
    print(f"{row['RA']:.6f},{row['DEC']:.6f},{row['phot_g_mean_mag']:.6f}")

    # print(f"{row['RA']:.6f},{row['DEC']:.6f}")

# print("Time after print: " + str(time.time() - INITIAL_TIME))
