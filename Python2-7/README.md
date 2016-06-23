# Geocoding locations and visualizing on Google Map

*Written in Python v2.7.11. Please install [openpyxl](https://openpyxl.readthedocs.io/en/default/) library to read Excel. Please install [SQLite Browser](http://sqlitebrowser.org/) if you wish to view and modify the databases (optional).*

The mini project includes two cases representing two different ways of data entry:
1. Location(s) entered by user
2. Location(s) read from a file

Run *geocoding.py* to start the program. Please follow the instructions and choose a case by entering 1 or 2.

## Case 1: Location(s) entered by user
If you entered 1, you will be asked to enter a location, for example:

* 10 G St NE, Washington, DC 20002
* UCLA, Los Angeles

Please note that [this Google Geocoding service](https://developers.google.com/maps/documentation/geocoding/intro#Geocoding) is generally designed for geocoding static (known in advance) addresses. The street address to be geocoded should be in the format used by the national postal service of the country concerned. Additional address elements such as business names and unit, suite or floor numbers should be avoided. 

The program will first check if the location is already in the database. If yes, the program will continue to ask for a new location; if no, the program will consume [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro) to retrieve geocoded information of this location, and store the information in a database (*geodata.sqlite*). The Geocoding API is rate limited to 2500 requests per day. There is a counter you can use to limit the number of calls to the geocoding
API for each run.

After entering the locations, the program will retrieve the records in the database, and write location, latitude, and longitude into a file (*where.js*) as a JavaScript list of lists. To view the locations, you can open *where.html* in a browser. If you cannot see any data when you open the where.html file, you might want to check the JavaScript or developer console for your browser.

To start over, simply delete the *geodata.sqlite* database and re-run the program.

## Case 2: Location(s) read from a file
If you entered 2, the program will open the [EIA Form-860](https://www.eia.gov/electricity/data/eia860/) Excel file, and retrieve power plant names and corresponding latitude and longitude data. There are over 8,500 records in this file. You can limit the number of records to be shown on the map. The information will be written into the *where.js* file as executable JavaScript code. You can view the locations of the power plants by opening *where.html* in a browser. If you cannot see any data when you open the where.html file, you might want to check the JavaScript or developer console for your browser.  
