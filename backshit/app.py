from astroquery.gaia import Gaia
import numpy as np
import math
from tqdm import tqdm
import csv
import pickle

import sys 
import subprocess

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   
#cors = CORS(app, resources={r"/process": {"origins": "http://127.0.0.1:5000"}})

#     print(f"Received exoplanet name: {exoplanet_name}")
# else:
#     print("No exoplanet name provided.")
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
def load_gaia_data(filename="static/data122.csv"):
    data={"RA": [], "DEC": [], "PRLX":[], "MAG": []}
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            data["RA"].append(row[1])
            data["DEC"].append(row[2])
            data["PRLX"].append(row[3])
            data["MAG"].append(row[4])
    return data
def get_preprocessed_data(gaia_results):
    # Extract RA and Dec
    parallax = np.array(gaia_results['PRLX'], dtype=float)
    star_ra = np.array(gaia_results['RA'], dtype=float)
    star_dec = np.array(gaia_results['DEC'], dtype=float)
    star_mag = np.array(gaia_results['MAG'], dtype=float)
    # Handle invalid parallax values (e.g., negative or zero)
    valid_parallax = np.where(parallax > 0, parallax, np.nan)  # set invalid values to NaN
    # Calculate distance in parsecs (1 / parallax in arcseconds)
    distance = 1 / (valid_parallax / 1000)  # convert parallax from milliarcseconds to arcseconds
    return {"dist": distance, "ra": star_ra, "dec": star_dec, "mag": star_mag}
def reposition(star_dict, ex_ra, ex_dec, ex_dist):
    new_coord = []
    
    # To radians
    ex_ra = ex_ra * math.pi/180
    ex_dec = ex_dec * math.pi/180
    for s_dist, s_ra, s_dec, s_mag in tqdm(zip(star_dict["dist"], star_dict["ra"], star_dict["dec"], star_dict["mag"]), total=len(star_dict["dist"])):
        if not math.isnan(s_dist) and not math.isnan(s_ra) and not math.isnan(s_dec):
            # To radians
            # print("dist: ", s_dist, ex_dist)
            # print("dec: ", s_dec, ex_dec * 180/math.pi)
            # print("ra: ", s_ra, ex_ra * 180/math.pi)
            s_ra = s_ra * math.pi/180
            s_dec = s_dec * math.pi/180
            # Ignore this crazy math, trust in us
            gamma = s_ra - ex_ra
            #print("gamma: ", gamma * 180/math.pi, "\na: ", s_dist * math.cos(s_dec), "\nb: ", ex_dist * math.cos(ex_dec))
            aux = s_dist**2 * math.cos(s_dec)**2 + ex_dist**2 * math.cos(ex_dec)**2 - 2 * s_dist * math.cos(s_dec) * ex_dist * math.cos(ex_dec) * math.cos(gamma)
            #print(math.sqrt(aux), (ex_dist**2 * math.cos(ex_dec)**2 + aux -s_dist**2 * math.cos(s_dec)**2) / (2 * ex_dist * math.cos(ex_dec) * math.sqrt(aux)))
            
            new_ra = math.acos((ex_dist**2 * math.cos(ex_dec)**2 + aux - s_dist**2 * math.cos(s_dec)**2) / (2 * ex_dist * math.cos(ex_dec) * math.sqrt(aux)) )
            new_dec = math.atan((s_dist * math.sin(s_dec) - ex_dist * math.sin(ex_dec)) / math.sqrt(aux))
            new_dist = (s_dist * math.sin(s_dec) - ex_dist * math.sin(ex_dec)) / math.sin(new_dec)
            new_mag = s_mag -5 + 5 * math.log10(new_dist)
            # Ignore this crazy math, trust in us
            # To degrees 
            new_ra = new_ra * 180/math.pi
            new_dec = new_dec * 180/math.pi
            new_coord.append((new_dist, new_ra, new_dec, new_mag))
    
    return new_coord
def load_exoplanet_data_from_csv(filename="static/planet_data.csv"):
    data = []
    with open(filename, "r") as file:
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
    print(exoplanets[exoplanet_name])
    stars = get_preprocessed_data(load_gaia_data()) # should load from .pkl file -- load_gaia_data
    # these should be computed on start
    # print(exoplanets[exoplanet_name]["ra"], exoplanets[exoplanet_name]["dec"], exoplanets[exoplanet_name]["sy_dist"])
    return reposition(stars, float(exoplanets[exoplanet_name]["ra"]), float(exoplanets[exoplanet_name]["dec"]), float(exoplanets[exoplanet_name]["sy_dist"]))
def get_csv_from_name(exoplanet_name):
    tuple_list = compute_positions(exoplanet_name)
    header = ["dist", "ra", "dec", "mag"]
    
    with open('output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        for row in tuple_list:
            writer.writerow(row)


@app.route('/process', methods=['POST'])
def process_string():
    data = request.get_json()
    input_string = data.get('inputString', '')
    # Use the string as a variable in your logic
    processed_string = input_string.upper()  # Example: processing the string
    print("something happened------------------------------")
    get_csv_from_name(input_string)
    subprocess.call("./static/hipsgen.sh")
    print("something finished")
    return jsonify({"result": processed_string})

@app.route('/', methods=['GET'])
def render():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
