#! /usr/bin/python

# am facut fisierul asta ptc cel ipynb pare sa fie proprietary si are compatibilitate putin ciudata

from astroquery.gaia import Gaia
import time 
SIZEOF_REQUEST = 2000 # trebuie marit dar momentan il las asa sa ruleze mai rapid
INITIAL_TIME = time.time()

query = """
SELECT TOP """ + str(SIZEOF_REQUEST) + """ SOURCE_ID, RA, DEC, PARALLAX
FROM gaiadr3.gaia_source
"""

job = Gaia.launch_job(query)

results = job.get_results()

print("Time passed: " + str(time.time() - INITIAL_TIME))

number_of_rows = len(results)
print(f"Number of rows: {number_of_rows}")


print(f"{'Source ID':<20} {'RA (deg)':<15} {'Dec (deg)':<15} {'Parallax (mas)':<15}")

# Print a separator
print('-' * 65)

# Print each row in the results
for row in results:
    print(f"{row['SOURCE_ID']:<20} {row['RA']:<15.6f} {row['DEC']:<15.6f} {row['PARALLAX']:<15.6f}")

print("Time after print: " + str(time.time() - INITIAL_TIME))
