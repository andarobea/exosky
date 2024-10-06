from astroquery.gaia import Gaia
import numpy as np
import math
import tqdm
import csv
import pickle 

def perform_gaia_query():
    query = """
    SELECT SOURCE_ID, RA, DEC, PARALLAX
    FROM gaiadr3.gaia_source
    """

    job = Gaia.launch_job(query)
    results = job.get_results()

    number_of_rows = len(results)
    print(f"[INFO] Retrieved {number_of_rows} number of rows from Gaia API.\n")
    return results

def load_gaia_data(filename):
    with open(filename, mode='rb') as file:
        gaia_results = pickle.load(file)
    return gaia_results

def get_preprocessed_data(gaia_results):
    # Extract RA and Dec
    coordinates = gaia_results[['RA', 'DEC']]
    parallax = np.array(gaia_results['PARALLAX'], dtype=float)
    star_ra = np.array(gaia_results['RA'], dtype=float)
    star_dec = np.array(gaia_results['DEC'], dtype=float)

    # Handle invalid parallax values (e.g., negative or zero)
    valid_parallax = np.where(parallax > 0, parallax, np.nan)  # set invalid values to NaN

    # Calculate distance in parsecs (1 / parallax in arcseconds)
    distance = 1 / (valid_parallax / 1000)  # convert parallax from milliarcseconds to arcseconds

    return {"dist": distance, "ra": star_ra, "dec": star_dec}

def reposition(star_dict, ex_ra, ex_dec, ex_dist):
    new_coord = []
    
    # To radians
    ex_ra = ex_ra * math.pi/180
    ex_dec = ex_dec * math.pi/180

    for s_dist, s_ra, s_dec in tqdm(zip(star_dict["dist"], star_dict["ra"], star_dict["dec"]), total=len(star_dict["dist"])):
        if not math.isnan(s_dist) and not math.isnan(s_ra) and not math.isnan(s_dec):

            # To radians
            s_ra = s_ra * math.pi/180
            s_dec = s_dec * math.pi/180

            # print("dist: ", s_dist, ex_dist)
            # print("dec: ", s_dec, ex_dec)
            # print("ra: ", s_ra, ex_ra)

            # Ignore this crazy math, trust in us
            gamma = s_ra - ex_ra
            aux = s_dist**2 * math.cos(s_dec)**2 + ex_dist**2 * math.cos(ex_dec)**2 - 2 * s_dist * math.cos(s_dec) * ex_dist * math.cos(ex_dec) * math.cos(gamma)
            new_ra = math.acos((ex_dist**2 * math.cos(ex_dec)**2 + aux -s_dist**2 * math.cos(s_dec)**2) / (2 * ex_dist * math.cos(ex_dec) * aux) )
            new_dec = math.atan((s_dist * math.sin(s_dec) - ex_dist * math.sin(ex_dec)) / math.sqrt(aux))
            new_dist = (s_dist * math.sin(s_dec) - ex_dist * math.sin(ex_dec)) / math.sin(new_dec)
            # Ignore this crazy math, trust in us

            # To degrees 
            s_ra = s_ra * 180/math.pi
            s_dec = s_dec * 180/math.pi

            new_coord.append((new_dist, new_ra, new_dec))
    
    return new_coord

def load_exoplanet_data_from_csv(filename="planet_data.csv"):
    data = []

    with open("planet_data.csv", "r") as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            data.append(row)

    header = data[0][1:]
    data = data[1:]

    exo_dict = {}

    for row in data:
        exo_dict[row[0]] = {}

        for name, info in zip(header, row[1:]):
            exo_dict[row[0]][name] = info 

    return exo_dict

def compute_positions(exoplanet_name):
    # these should be computed on start, not at every re-computation 
    exoplanets = load_exoplanet_data_from_csv()
    stars = get_preprocessed_data(perform_gaia_query()) # should load from .pkl file -- load_gaia_data
    # these should be computed on start

    return reposition(stars, exoplanets[exoplanet_name]["ra"], exoplanets[exoplanet_name]["dec"], exoplanets[exoplanet_name]["sy_dist"])


# def printstring(string):
#     print("String is: ", string)