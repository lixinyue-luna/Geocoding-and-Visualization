import urllib
import sqlite3
import openpyxl
import os, os.path
import shutil

# Creat a database of power plant with cooling and locations information
conn = sqlite3.connect('powerPlant.sqlite')
cur = conn.cursor()
# cur.executescript('''
#     DROP TABLE IF EXISTS coolingInfo;
#     DROP TABLE IF EXISTS plantInfo;
#     CREATE TABLE coolingInfo (
#         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#         plantID INTEGER, coolingID TEXT, coolingStatus TEXT, month INTEGER, year INTEGER,
#         coolingType TEXT, multiCooling INTEGER, coolingSource TEXT, coolingDischarge TEXT
#         );
#     CREATE TABLE plantInfo (
#         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#         plantID INTEGER, plantName TEXT, address TEXT, city TEXT,
#         state TEXT, zipcode INTEGER, county TEXT, lat REAL, lng REAL
#         );
# ''')
#
# # Load Excel files
# print "\n"
# print "Please wait. Loading Cooling Type and Source for US Plants..."
# cooling_wb = openpyxl.load_workbook(filename=r'Cooling Type and Source for US Plants.xlsx')
# cooling_sheets = cooling_wb.get_sheet_names()
# coolingList = cooling_wb.get_sheet_by_name(cooling_sheets[0])
#
# print "Please wait. Loading US Plants with Latitude and Longitude..."
# plant_wb = openpyxl.load_workbook(filename=r'US Plants with Latitude and Longitude.xlsx')
# plant_sheets = plant_wb.get_sheet_names()
# plantList = plant_wb.get_sheet_by_name(plant_sheets[0])
#
# # Write to databases coolingList and plantList
# tmp = 0 # count multiCooling
# for row in coolingList.rows[2:]:
#     try:
#         res = (int(row[0].value), row[3].value, row[4].value, row[5].value,
#             row[6].value, row[7].value, row[9].value, row[11].value, row[12].value)
#         cur.execute('''
#             INSERT OR REPLACE INTO coolingInfo
#             (plantID, coolingID, coolingStatus, month, year,
#             coolingType, multiCooling, coolingSource, coolingDischarge)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', res)
#         if int(row[9].value) == 1:
#             res = (int(row[0].value), row[3].value, row[4].value, row[5].value,
#                 row[6].value, row[8].value, row[9].value, row[11].value, row[12].value)
#             cur.execute('''
#                 INSERT OR REPLACE INTO coolingInfo
#                 (plantID, coolingID, coolingStatus, month, year,
#                 coolingType, multiCooling, coolingSource, coolingDischarge)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', res)
#     except:
#         continue
#
# for row in plantList.rows[2:]:
#     try:
#         res = (int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value,
#             row[5].value, row[6].value, row[7].value, row[8].value)
#         cur.execute('''
#             INSERT OR REPLACE INTO plantInfo
#             (plantID, plantName, address, city, state, zipcode, county, lat, lng)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', res)
#     except:
#         continue
#
# conn.commit()

# Create a folder for each known cooling type.
coolingFolders = cur.execute("SELECT DISTINCT coolingType FROM coolingInfo")
res = coolingFolders.fetchall()
for row in range(len(res)):
    newFolder = res[row][0]
    if len(newFolder) < 1:
        newFolder = "NA"
    path = "images/" + newFolder
    if os.path.exists(path) is False:
        os.makedirs(path)

# Select plants and cooling types
data = cur.execute('''
    SELECT DISTINCT coolingInfo.plantID, plantInfo.plantName, coolingInfo.coolingType, plantInfo.lat, plantInfo.lng
    FROM coolingInfo, plantInfo
    WHERE coolingInfo.plantID = plantInfo.plantID
    ORDER BY coolingInfo.plantID
    ''')
res = data.fetchall()

# Google Maps API
serviceurl = "https://maps.googleapis.com/maps/api/staticmap?"
# # Deal with SSL certificate anomalies Python > 2.7
# scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

# Image format
maptype = "satellite"
zoom = "16"
size = "640x640"
image_format = "png"
key = "AIzaSyBNN6-EvyqIrh0O4A2c5GjbgoNR7zFeAdI"  # This is rate limited to 2500 free queries per day

# Retrieve image from Google Maps API and save to local directories
countLimit = 10  # Limit each run
count = 0
row = 0
while count < countLimit:
    # Plant and cooling info
    plantCode = res[row][0]
    name = res[row][1]
    coolType = res[row][2]
    lat = str(res[row][3])
    lng = str(res[row][4])
    center = lat + "," + lng

    # Image destination and file name
    # 1. File folder
    folder = coolType
    if len(folder) < 1:
        folder = "NA"

    # 2. File name. First check if the plant has multiple cooling types:
    if row > 0 and row < len(res) - 1:
        if plantCode == res[row-1][0] or plantCode == res[row+1][0]:
            fileName = name + "_multipleCT_" + lat + "," + lng + ".png"
        else:
            fileName = name + "_" + lat + "," + lng + ".png"
    elif row == 0:
        if plantCode == res[1][0]:
            fileName = name + "_multipleCT_" + lat + "," + lng + ".png"
        else:
            fileName = name + "_" + lat + "," + lng + ".png"
    else:
        if plantCode == res[row-1][0]:
            fileName = name + "_multipleCT_" + lat + "," + lng + ".png"
        else:
            fileName = name + "_" + lat + "," + lng + ".png"

    # 3. Save images
    # 3.1. Copy image from another directory if it has been downloaded to avoid a new query
    if row > 0 and plantCode == res[row-1][0]:
        srcfile = os.path.join("images", str(res[row-1][2]), fileName)
        dstfile = os.path.join("images", folder, fileName)
        shutil.copy(srcfile, dstfile)
        print "Copied ", fileName, " to ", folder
    # 3.2. Retrieve image if it has not been downloaded
    else:
        url =  serviceurl + urllib.urlencode({
            "maptype": maptype, "center": center, "zoom": zoom, "size": size, "format": image_format, "key": key
            })
        urllib.urlretrieve(url, os.path.join("images", folder, fileName))
        print "Saved ", fileName, " to ", folder
        count += 1

    row += 1

conn.close()
