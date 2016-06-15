import urllib
import urllib.request
import sqlite3
import openpyxl
import json
import codecs
import time
import ssl

################################################
# Choose a case to start with
print ("Please select a case to start with:")
print ("1. Enter a location of your choice; or")
print ("2. Use default list of U.S. power plants.")
case = input("Please enter 1 or 2: ")
while case != "1" and case != "2":
    print ("Warning: The input should be 1 or 2.")
    print ("1. Enter a location of your choice; or")
    print ("2. Use default list of U.S. power plants.")
    case = input("Please enter 1 or 2: ")

################################################
# Case 1: user input
if case == "1":
    serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"
    # Deal with SSL certificate anomalies Python > 2.7
    scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    # scontext = None

    # Connect to database
    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)
    ''')

    count = 0    # Set the rate limit
    while True:
        if count > 100 : break
        address = input('Please enter a location: ')
        if len(address) < 1 : break
        print ('')
        cur.execute("SELECT geodata FROM Locations WHERE address= ?", (address, ))

        # If location in database, skip
        try:
            data = cur.fetchone()[0]
            print ("Found in database ",address)
            continue
        except:
            pass

        # If location not in database, geocode the location using Google API
        print ('Resolving', address)
        url = serviceurl + urllib.parse.urlencode({"address": address})
        print ('Retrieving', url)
        uh = urllib.request.urlopen(url, context=scontext)
        data = uh.read()
        print ('Retrieved',len(data))
        print (type(data))
        count = count + 1
        try:
            js = json.loads(data.decode("utf-8"))
            # print (js) #  Uncomment this line to print js in case unicode causes an error
        except:
            continue

        if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
            print ('==== Failure To Retrieve ====')
            continue

        cur.execute('''INSERT INTO Locations (address, geodata)
                VALUES ( ?, ? )''', (address, data) )
        conn.commit()
        time.sleep(1)

    # Read the database to visualize it on a map
    print ("Writing results to where.js...")
    cur.execute('SELECT * FROM Locations')
    fhand = codecs.open('where.js','w', "utf-8")
    fhand.write("myData = [\n")
    count = 0
    for row in cur :
        data = row[1].decode("utf-8")
        try:
            js = json.loads(data)
            # print (js)    #  Uncomment this line to print js in case unicode causes an error
        except: continue

        if not('status' in js and js['status'] == 'OK') : continue

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        if lat == 0 or lng == 0 : continue
        where = js['results'][0]['formatted_address']
        where = where.replace("'","")
        try :
            print (where, lat, lng)
            count = count + 1
            if count > 1 : fhand.write(",\n")
            output = "["+str(lat)+","+str(lng)+", '"+where+"']"
            fhand.write(output)
        except:
            continue

    fhand.write("\n];\n")
    cur.close()
    fhand.close()
    print (count, "records written to where.js")
    print ("Please open where.html to view the data in a browser")


################################################
# Case 2: use exsiting list of power plants
elif case == "2":
    # Load workbook from EIA Form-860 Plant_Y2014
    # Get the first sheet that contains the plant information
    print ("Please wait. Loading Excel...")
    plant_wb = openpyxl.load_workbook(filename=r'2___Plant_Y2014.xlsx')
    plant_sheets = plant_wb.get_sheet_names()
    plantList = plant_wb.get_sheet_by_name(plant_sheets[0])
    print ("\n")
    # Open an encoded file where.js
    fhand = codecs.open('where.js','w', "utf-8")
    fhand.write("myData = [\n")
    print ("How many data points would you like to see on the map?")
    cap = input("Please enter a number between 0 and 8518: ")
    if cap == "":
        cap = 8519
    count = 0
    for row in plantList.rows[2:]:
        if count >= int(cap): break
        try:
            plantName = row[3].value
            lat = row[9].value
            lng = row[10].value
            if lat == 0 or lng == 0 : continue
            where = plantName
            where = where.replace("'","")
            try:
                # print (where, lat, lng)
                count = count + 1
                if count > 1: fhand.write(",\n")
                output = "["+str(lat)+","+str(lng)+", '"+where+"']"
                fhand.write(output)
            except:
                continue
        except: continue

    fhand.write("\n];\n")
    fhand.close()
    print ("\n")
    print (count, "records written to where.js")
    print ("Please open where.html to view the data in a browser")
