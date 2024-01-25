#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
from zipfile import ZipFile
import json
from collections import Counter

with ZipFile(sys.argv[1]) as f:
    access_points = json.loads(f.read("accessPoints.json"))
    vendor_model = []
    for ap in access_points["accessPoints"]:
        vendor = ap["vendor"]
        if ap["mine"]:
            vendor_model += [(ap["vendor"], ap["model"], ap["color"])]

    simulated_radios = json.loads(f.read("simulatedRadios.json"))
    antennas = json.loads(f.read("antennaTypes.json"))
    antenna_ids = []
    antenna_types = []
    for radio in simulated_radios["simulatedRadios"]:
        for antenna in antennas["antennaTypes"]:
            if radio["antennaTypeId"] == antenna["id"]:
                antenna_types += [antenna["name"]]

with open("access_points.csv", "w") as ap_csv_f:
    csv_result = csv.writer(ap_csv_f, dialect="excel", quoting=csv.QUOTE_ALL)
    for ap, count in Counter(vendor_model).items():
        csv_result.writerow([ap[0], ap[1], ap[2], count])

with open("antennas.csv", "w") as ant_csv_f:
    csv_result = csv.writer(ant_csv_f, dialect="excel", quoting=csv.QUOTE_ALL)
    for antenna, count in Counter(antenna_types).items():
        csv_result.writerow([antenna, count])