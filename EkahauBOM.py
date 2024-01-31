#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import json
from zipfile import ZipFile
from collections import Counter
from pathlib import Path

color_database = {"#FFE600" : "Yellow", "#FF8500" : "Orange", "#FF0000" : "Red",
                  "#FF00FF" : "Pink", "#C297FF" : "Violet", "#0068FF" : "Blue",
                  "#6D6D6D" : "Gray", "#00FF00" : "Green", "#C97700" : "Brown",
                  "#00FFCE" : "Mint"}

with ZipFile(sys.argv[1]) as f:
    access_points = json.loads(f.read("accessPoints.json"))
    floor_plans = json.loads(f.read("floorPlans.json"))
    vendor_model = []
    for ap in access_points["accessPoints"]:
        if ap["mine"]:
            for floor in floor_plans["floorPlans"]:
                if ap["location"]["floorPlanId"] == floor["id"]:
                    floor_name = floor["name"]
            if "color" in ap.keys():
                try:
                    color_name = color_database[ap["color"]]
                    vendor_model += [(ap["vendor"], ap["model"], color_name, floor_name)]
                except:
                    vendor_model += [(ap["vendor"], ap["model"], ap["color"], floor_name)]
            else:
                vendor_model += [(ap["vendor"], ap["model"], None, floor_name)]

    simulated_radios = json.loads(f.read("simulatedRadios.json"))
    antennas = json.loads(f.read("antennaTypes.json"))
    antenna_ids = []
    antenna_types = []
    for radio in simulated_radios["simulatedRadios"]:
        for antenna in antennas["antennaTypes"]:
            if radio["antennaTypeId"] == antenna["id"]:
                antenna_types += [antenna["name"]]

with open(f'output/{Path(sys.argv[1]).stem}_access_points.csv', "w") as ap_csv_f:
    csv_result = csv.writer(ap_csv_f, dialect="excel", quoting=csv.QUOTE_ALL)
    csv_result.writerow(["Vendor", "Model", "Floor", "Color", "Quantity"])
    for ap, count in Counter(vendor_model).items():
        csv_result.writerow([ap[0], ap[1], ap[3], ap[2], count])

with open(f'output/{Path(sys.argv[1]).stem}_antennas.csv', "w") as ant_csv_f:
    csv_result = csv.writer(ant_csv_f, dialect="excel", quoting=csv.QUOTE_ALL)
    csv_result.writerow(["Antenna Model", "Quantity"])
    for antenna, count in Counter(antenna_types).items():
        csv_result.writerow([antenna, count])