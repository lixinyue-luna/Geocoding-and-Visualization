# US Power Plant Cooling Systems
*Written in Python v2.7.11. Please install [openpyxl](https://openpyxl.readthedocs.io/en/default/) library to read Excel. Please install [SQLite Browser](http://sqlitebrowser.org/) if you wish to view and modify the databases (optional).*

The `solution.py` does the following:

1. Reads Excel files and create databases of cooling types and geographic information for US power plants.
2. Create a folder for each cooling type.
3. Uses [Google Static Maps API](https://developers.google.com/maps/documentation/static-maps/intro) to find satellite images of the plants.
4. Save images in the folder of the corresponding cooling type.

Please run `solution.py` to retrieve images. You can change 'countLimit' to limit the number of queries per run. Please note that the with current API key, the number of free queries is rate limited 2500 per day.
