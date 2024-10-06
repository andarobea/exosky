#! /usr/bin/bash

rm -r ./hips
java -jar Hipsgen-cat.jar -cat exoplanet -in output.csv -out static/hips -ra ra -dec dec -score mag -lM 5