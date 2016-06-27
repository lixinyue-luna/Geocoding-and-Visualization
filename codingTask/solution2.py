import urllib
import sqlite3
import openpyxl
import os, os.path
import shutil

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
            print "Zoom level (Range 0 to 21)"
            zoom = raw_input("Zoom level (Default 16): ")
            try:
                if int(zoom) >= 0 and int(zoom) <= 21:
                    zoom = str(zoom)
                else:
                    print "Not a vaild input. Use default zoom level: 16."
                    zoom = "16"
            except:
                print "Not a vaild input. Use default zoom level: 16."
                zoom = "16"

            # Map size
            print "Map size (horizontal x vertical, default 640 pixels x 640 pixels): "
            horizontal = raw_input("Horizontal value (Default 640): ")
            vertical = raw_input("Vertical value (Default 640): ")
            try:
                horizontal = int(horizontal)
                vertical = int(vertical)
            except:
                horizontal = 640
                vertical = 640
            size = str(horizontal) + "x" + str(vertical)

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

# Return file name
def fileNaming(plantName, multi, lat, lng, image_format):
    if multi == 1:
        return name + "_multipleCT_" + lat + "," + lng + "." + image_format
    elif multi == 0:
        return name + "_" + lat + "," + lng + "." + image_format

# Return file destination(s)
def fileDestination(fileName, coolingType):
    destination = []
    for i in coolingType:
        destination.append(os.path.join("images", i, fileName))
    return destination
