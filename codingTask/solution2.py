import urllib
import sqlite3
import openpyxl
import os, os.path
import shutil

############################################################
### Functions
# Return image specifications
def imageSpec():
    # Default values:
    maptype = "satellite"
    zoom = "16"
    size = "640x640"
    image_format = "png"
    key = "AIzaSyBNN6-EvyqIrh0O4A2c5GjbgoNR7zFeAdI"  # This is rate limited to 2500 free queries per day
    default = (maptype, zoom, size, image_format, key)

    case = raw_input("Enter 1 to use default values. Enter 2 to customize image specifications: ")
    try:
        if int(case) == 1:
            return default
        elif int(case) == 2:
            print "Customizing image specifications..."
            # Map type
            print ""
            print "Map type (Enter 1 to 4 to choose a map type):"
            print "1. Satellite (default)"
            print "2. Hybrid"
            print "3. Roadmap"
            print "4. Terrain"
            maptype = raw_input("Map type: ")
            if str(maptype) == "1":
                maptype = "satellite"
            elif str(maptype) == "2":
                maptype = "hybrid"
            elif str(maptype) == "3":
                maptype = "roadmap"
            elif str(maptype) == "4":
                maptype = "terrain"
            else:
                print "Other input. Use default map type: Satellite"
                maptype = "satellite"

            # Zoom level
            print ""
            print "Zoom level (Range 0 to 21)"
            zoom = raw_input("Zoom level (Default 16): ")
            try:
                if int(zoom) >= 0 and int(zoom) <= 21:
                    zoom = str(zoom)
                else:
                    print "Not a vaild input. Use default zoom level: 16"
                    zoom = "16"
            except:
                print "Not a vaild input. Use default zoom level: 16"
                zoom = "16"

            # Map size
            print ""
            print "Map size (horizontal x vertical, default 640 pixels x 640 pixels): "
            horizontal = raw_input("Horizontal value (Default 640): ")
            vertical = raw_input("Vertical value (Default 640): ")
            try:
                horizontal = int(horizontal)
                vertical = int(vertical)
            except:
                print "Not a vaild input. Use default value: 640 x 640"
                horizontal = 640
                vertical = 640
            size = str(horizontal) + "x" + str(vertical)

            # Image format
            print ""
            print "Image format (Enter 1 to 3 to choose an output format):"
            print "1. PNG (default)"
            print "2. JPEG"
            print "3. GIF"
            image_format = raw_input("Image format: ")
            try:
                if str(image_format) == "1":
                    image_format = "png"
                elif str(image_format) == "2":
                    image_format = "jpeg"
                elif str(image_format) == "3":
                    image_format == "gif"
                else:
                    print "Other input. Use default image format: PNG"
                    image_format == "png"
            except:
                print "Other input. Use default image format: PNG"
                image_format == "png"

            # API key
            print ""
            print "Have a Google API key?"
            print "(You can get your API key at Google Developers Console)"
            key = raw_input("Key (or press Enter to use the default key): ")
            try:
                key = str(key)
            except:
                print "Other input. Use default key."
                key = "AIzaSyBNN6-EvyqIrh0O4A2c5GjbgoNR7zFeAdI"

            # Customize values
            return (maptype, zoom, size, image_format, key)

    except:
        print "Invalid input. Using default values."
        return default

# Return the Google Static Maps API URL
def imageURL(maptype, center, zoom, size, image_format, key):
    serviceurl = "https://maps.googleapis.com/maps/api/staticmap?"
    url = serviceurl + urllib.urlencode({
        "maptype": maptype, "center": center, "zoom": zoom, "size": size, "format": image_format, "key": key
        })
    return url

def newFolder(coolingTypes):
    for i in coolingTypes:
        if len(i) < 1:
            cooling = "NA"
        else:
            cooling = i
        path = os.path.join("images", cooling)
        if os.path.exists(path) is False:
            os.makedirs(path)

# Return file name
def fileNaming(plantName, multi, lat, lng, image_format):
    if multi == 1:
        return plantName + "_multipleCT_" + lat + "," + lng + "." + image_format
    elif multi == 0:
        return plantName + "_" + lat + "," + lng + "." + image_format

# Return file destination(s)
def fileDestination(fileName, coolingType):
    destination = []
    for i in coolingType:
        if len(i) < 1:
            destination.append(os.path.join("images", "NA", fileName))
        else:
            destination.append(os.path.join("images", i, fileName))
    return destination

############################################################
### Main
## Creat a database of power plant with cooling and locations information
# Set up database using Sqlite package
conn = sqlite3.connect('powerPlant.sqlite')
cur = conn.cursor()
cur.executescript('''
    DROP TABLE IF EXISTS coolingInfo;
    DROP TABLE IF EXISTS plantInfo;
    CREATE TABLE coolingInfo (
        plantID INTEGER, coolingID TEXT, coolingStatus TEXT, month INTEGER, year INTEGER,
        coolingType TEXT, multiCooling INTEGER, coolingSource TEXT, coolingDischarge TEXT
        );
    CREATE TABLE plantInfo (
        plantID INTEGER, plantName TEXT, address TEXT, city TEXT,
        state TEXT, zipcode INTEGER, county TEXT, lat REAL, lng REAL
        );
    CREATE TABLE IF NOT EXISTS savedImage (
        plantName TEXT, coolingType TEXT, multiCooling INTEGER, destination TEXT
        );
''')

# Load Excel files
print "\n"
print "Please wait. Loading Cooling Type and Source for US Plants..."
cooling_wb = openpyxl.load_workbook(filename=r'Cooling Type and Source for US Plants.xlsx')
cooling_sheets = cooling_wb.get_sheet_names()
coolingList = cooling_wb.get_sheet_by_name(cooling_sheets[0])

print "Please wait. Loading US Plants with Latitude and Longitude..."
plant_wb = openpyxl.load_workbook(filename=r'US Plants with Latitude and Longitude.xlsx')
plant_sheets = plant_wb.get_sheet_names()
plantList = plant_wb.get_sheet_by_name(plant_sheets[0])

# Write to databases coolingList and plantList
tmp = 0 # count multiCooling
for row in coolingList.rows[2:]:
    try:
        res = (int(row[0].value), row[3].value, row[4].value, row[5].value,
            row[6].value, row[7].value, row[9].value, row[11].value, row[12].value)
        cur.execute('''
            INSERT OR REPLACE INTO coolingInfo
            (plantID, coolingID, coolingStatus, month, year,
            coolingType, multiCooling, coolingSource, coolingDischarge)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', res)
        if int(row[9].value) == 1:
            res = (int(row[0].value), row[3].value, row[4].value, row[5].value,
                row[6].value, row[8].value, row[9].value, row[11].value, row[12].value)
            cur.execute('''
                INSERT OR REPLACE INTO coolingInfo
                (plantID, coolingID, coolingStatus, month, year,
                coolingType, multiCooling, coolingSource, coolingDischarge)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', res)
    except:
        continue

for row in plantList.rows[2:]:
    try:
        res = (int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value,
            row[5].value, row[6].value, row[7].value, row[8].value)
        cur.execute('''
            INSERT OR REPLACE INTO plantInfo
            (plantID, plantName, address, city, state, zipcode, county, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', res)
    except:
        continue

conn.commit()

# Create a folder for each known cooling type.
coolingFolders = cur.execute("SELECT DISTINCT coolingType FROM coolingInfo")
res = coolingFolders.fetchall()
coolingTypes = []
for row in range(len(res)):
    coolingTypes.append(res[row][0])
newFolder(coolingTypes)

# Select plants and cooling types
data = cur.execute('''
    SELECT DISTINCT coolingInfo.plantID, plantInfo.plantName, coolingInfo.coolingType, plantInfo.lat, plantInfo.lng
    FROM coolingInfo, plantInfo
    WHERE coolingInfo.plantID = plantInfo.plantID
    ORDER BY coolingInfo.plantID
    ''')
res = data.fetchall()

# Create a dictionary {(plantName, lat, lng): [list of coolingType]}
dictPlant = {}
for row in range(len(res)):
    plantName = res[row][1]
    coolingType = res[row][2]
    lat = str(res[row][3])
    lng = str(res[row][4])
    k = (plantName, lat, lng)
    v = coolingType
    dictPlant[k] = dictPlant.get(k, [])
    dictPlant[k].append(v)

## Retrieve image from Google Maps API and save to local directories
# Set parameters
print ""
print "How many new maps you wish to retrieve?"
countLimit = raw_input("Enter a number between 1 and 2500 (default 100): ")
try:
    if int(countLimit) > 2500 or int(countLimit) < 1:
        countLimit = 100
    else:
        countLimit = int(countLimit)
except:
    print "Invalid input. Use default limit: 100"
    countLimit = 100

print ""
print "Specify map properties:"
setPar = 2
while setPar == 2:
    maptype, zoom, size, image_format, key = imageSpec()
    print ""
    print "Double checking..."
    print "Map type: ", maptype
    print "Zoom level: ", zoom
    print "Map size (pixels): ", size
    print "Image format: ", image_format
    print ""
    setPar = raw_input("Please enter 1 to confirm, or 2 to reset parameters: ")
    try:
        while int(setPar) != 1 and int(setPar) != 2:
            print "Invalid input."
            setPar = raw_input("Please enter 1 to confirm, or 2 to reset parameters: ")
        if int(setPar) == 1:
            setPar = 1
            break
        elif int(setPar) == 2:
            print "Reset parameters."
        else:
            print "Invalid input"
            setPar == 2
    except:
        print "Invalid input. Reset parameters."
        setPar == 2

# Retreive the list of plants with cooling systems
plants = cur.execute('''SELECT DISTINCT coolingInfo.plantID, plantInfo.plantName, plantInfo.lat, plantInfo.lng
    FROM coolingInfo, plantInfo
    WHERE coolingInfo.plantID = plantInfo.plantID
    ORDER BY coolingInfo.plantID
    ''')
res = plants.fetchall()

count = 0
row = 0
while count < countLimit:
    plantName = res[row][1]
    lat = str(res[row][2])
    lng = str(res[row][3])
    cooling = dictPlant[(plantName, lat, lng)]
    center = lat + "," + lng

    cur.execute("SELECT plantName FROM savedImage WHERE plantName = ?", (plantName, ))

    # If the image has already been downloaded, skip
    try:
        entity = cur.fetchone()[0]
        print "Found in database", plantName
        row += 1
        continue
    except:
        pass

    # If the image is not in the database, fire a request
    if len(cooling) > 1:
        multi = 1
    else:
        multi = 0
    fileName = fileNaming(plantName, multi, lat, lng, image_format)
    destination = fileDestination(fileName, cooling)
    url = imageURL(maptype, center, zoom, size, image_format, key)
    urllib.urlretrieve(url, destination[0])
    print "Saved " + fileName + " to " + destination[0]
    cur.execute('''INSERT INTO savedImage (plantName, coolingType, multiCooling, destination)
        VALUES (?, ?, ?, ?)''', (plantName, cooling[0], multi, destination[0]))
    if multi == 1:
        for i in range(1, len(cooling)):
            shutil.copy(destination[0], destination[i])
            print "Copied ", fileName, " to ", destination[i]
            cur.execute('''INSERT INTO savedImage (plantName, coolingType, multiCooling, destination)
                VALUES (?, ?, ?, ?)''', (plantName, cooling[i], multi, destination[i]))
    conn.commit()
    row += 1
    count += 1

conn.close()
